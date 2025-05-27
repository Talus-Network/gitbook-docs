# Leader

## Sequence diagram

High-level sequence diagram describing the duties of the Leader.

```mermaid
sequenceDiagram
    participant RG as [On-chain] Registry
    participant WF as [On-chain] Workflow
    participant LD as [Off-chain] Leader
    participant DB as [Off-chain] Indexer
    participant TL as [Either] Tool

    critical initialize service
        LD-->>LD: load env, global objects, secret mnemonics
        LD->>WF: request leader caps and gas coins
        LD->>DB: establish a connection to indexer
    end

    loop listen for RequestWalkExecutionEvent
        WF->>LD: event incoming
        LD->>DB: save event in indexer
        Note over LD,DB: id, digest, json, retried, error, status: Queued
    end

    loop iterate over `status: Queued` events
        LD->>DB: update to `status: Active`
        LD->>RG: load tool definition from event payload
        Note over LD,RG: This definition should be cached
        LD->>WF: request input data for tool
        LD-->>LD: verify input data based on schema from tool def
        LD->>+TL: invoke tool
        TL->>-LD: tool finished and returned output data
        LD-->>LD: verify output data based on schema from tool def
        LD->>LD: wait for open channel
    end

    loop channel listening
        LD-->>LD: determine execution outcome

        alt successful
            LD->>WF: submit execution result TX
            LD->>DB: update `status: Successful`
        else failed
            alt retriable
                LD->>DB: update `status: Queued, retried++`
            else fatal
                LD->>WF: submit execution result TX
                LD->>DB: update `status: Dead`
            end
        end
    end

    loop iterate over `status: Active, updated_at < N` events
        LD->>WF: submit execution result TX over a channel
        LD->>DB: update `status: Dead`
        Note over LD, DB: We should aim to avoid this alotgether
    end
```

## Processes

There are multiple processes running in parallel in the leader node. These are as follows:

1. **`RequestWalkExectuionEvent` listener**

- This process repeatedly queries Sui RPC for new events coming from the Workflow. It then saves these events on the Indexer.
- It persists the last visited cursor, a pointer to the event it has written to our Indexer last. This way we ensure no events are lost in case the Leader goes down.

2. **`Queued` events execution engine**

- This part of the Leader queries `status: Queued` events in order to invoke Tools specified on the event.
- Communicates with the Workflow to fetch input data for Tools.
- Communicates with the Tool Registry to fetch Tool schemas in order to validate its input data.
- Invokes Tools with the verified input data.
- Verifies output data from Tools based on its output schemas.
- Finally, it halts until a channel is open to send a TX back to Workflow (this can happen at any point during the execution if it errors).

3. **Workflow communication channel**

- N channels can run in parallel where N is the number of `leader_cap`s the Leader has available.
- Receives messages from the execution engine and evaluates the result. Depending on this, multiple outcomes can happen:
  - (a) `Successful` - TX to Workflow is sent and status is updated in Indexer to `Successful`. If TX fails, we have to block the channel for 24h.
  - (b.i) `Failed.Retriable` - Status is updated back to `Queued` and retires are incremented in Indexer.
  - (b.ii) `Failed.Fatal` - TX to Workflow is sent and status is updated in Indexer to `Dead`. If TX fails, we have to block the channel for 24h.

4. **Stale `Active` events disposal**

- Events that are still `Active` after a configured time has passed should be disposed of and marked as `Dead`.
- This should also notify Workflow via a TX.

## High integrity channel

Some parts of the Leader service use a custom channel implementation that handles indexing of messages sent over this channel, as well as retries and sweeps of stale messages.

Notably, the event listener<>event executor and the event executor<>merchant processes communicate via this channel.

The following state diagrams should highlight the functionality of the channel.

{% hint style="info" %}
Note that this channel "assumes" it has a stable Redis connection. There are edge cases, where dropping events is very unlikely, but possible. One such edge case is if sending a message over this channel fails due to Redis being unavailable but the Sui event listener successfully saves the next page cursor to Redis. This can in the future be improved by handling Redis errors within the channel differently (by for example, halting).
{% endhint %}

### High integrity channel receiver and sender

```mermaid
stateDiagram-v2
    state HighIntegrityChannel {
        state if_successful <<choice>>
        [*] --> Receiver: Start
        Receiver --> ReceiveMessage: recv
        ReceiveMessage --> MoveToActiveSet
        MoveToActiveSet --> ProcessMessage
        ProcessMessage --> if_successful
        if_successful --> NackMessage: Err
        if_successful --> AckMessage: Ok
        NackMessage --> MoveBackToQueued
        AckMessage --> RemoveMessage
        MoveBackToQueued --> [*]
        RemoveMessage --> [*]

        --

        [*] --> Sender: Start
        state if_exists <<choice>>
        state if_channel_capacity <<choice>>
        Sender --> CheckMessageExists
        CheckMessageExists --> if_exists
        if_exists --> [*]: Exists
        if_exists --> SaveMessageData: NotExists
        SaveMessageData --> CheckChannelCapacity
        CheckChannelCapacity --> if_channel_capacity
        if_channel_capacity --> [*]: Full
        if_channel_capacity --> SendMessage: NotFull
        SendMessage --> [*]: send
    }
```

### Retrier and sweeper processes

```mermaid
stateDiagram-v2
    state RetrierAndSweeper {
        state if_retry_count <<choice>>
        state if_message_exists <<choice>>
        [*] --> Retrier: Start
        Retrier --> FetchRandomQueuedMessage
        FetchRandomQueuedMessage --> if_message_exists
        if_message_exists --> CheckRetryCount: MessageExists
        if_message_exists --> [*]: NoMessage
        CheckRetryCount --> if_retry_count
        if_retry_count --> DropMessage: MaxRetriesReached
        if_retry_count --> ResendMessage: RetriesRemaining
        ResendMessage --> [*]: resend
        DropMessage --> [*]

        --

        [*] --> Sweeper: Start
        state if_stale <<choice>>
        Sweeper --> CheckStaleMessages
        CheckStaleMessages --> if_stale
        if_stale --> MoveBackToQueuedSet: Stale
        if_stale --> [*]: NotStale
        MoveBackToQueuedSet --> [*]
    }
```

