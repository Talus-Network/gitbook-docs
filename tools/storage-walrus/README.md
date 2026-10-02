# `xyz.taluslabs.storage.walrus.upload-json@1`

Standard Nexus Tool that uploads a JSON file to Walrus and returns the blob ID.

## Input

**`json`: [`String`]**

The JSON data to upload.

_opt_ **`publisher_url`: [`Option<String>`]** _default_: [`None`]

The Walrus publisher URL. Must be a public `https` endpoint with no query, fragment or credentials. If not provided, the default Walrus configuration will be used. See [Endpoint targets](#endpoint-targets).

_opt_ **`aggregator_url`: [`Option<String>`]** _default_: [`None`]

The Walrus aggregator URL. Must be a public `https` endpoint with no query, fragment or credentials. If not provided, the default Walrus configuration will be used. See [Endpoint targets](#endpoint-targets).

_opt_ **`epochs`: [`u64`]** _default_: [`1`]

Number of epochs to store the data.

_opt_ **`send_to_address`: [`Option<String>`]** _default_: [`None`]

Optional address to which the created Blob object should be sent.

## Output Variants & Ports

**`newly_created`**

A new blob was created and uploaded successfully.

- **`newly_created.blob_id`: [`String`]** - The unique identifier for the uploaded blob
- **`newly_created.end_epoch`: [`u64`]** - The epoch at which the blob will expire
- **`newly_created.sui_object_id`: [`String`]** - Sui object ID of the newly created blob

**`already_certified`**

The blob was already certified in the blockchain.

- **`already_certified.blob_id`: [`String`]** - The unique identifier for the blob
- **`already_certified.end_epoch`: [`u64`]** - The epoch at which the blob will expire
- **`already_certified.tx_digest`: [`String`]** - Transaction digest of the certified blob

**`err`**

The blob upload failed.

- **`err.reason`: [`String`]** - A detailed error message describing what went wrong
- **`err.kind`: [`UploadErrorKind`]** - Type of error that occurred
  - Possible kinds:
    - `network` - Error during HTTP requests or network connectivity issues
    - `validation` - Invalid JSON input or data validation failures
- **`err.status_code`: [`Option<u16>`]** - HTTP status code if available (for network errors)

---

# `xyz.taluslabs.storage.walrus.upload-file@1`

Standard Nexus Tool that uploads a file to Walrus and returns the blob ID.

## Input

**`file_path`: [`String`]**

The path of the file to upload, relative to `WALRUS_UPLOAD_ROOT`. Uploading from a local path is **disabled** unless that variable is set. See [Local file uploads](#local-file-uploads).

_opt_ **`publisher_url`: [`Option<String>`]** _default_: [`None`]

The Walrus publisher URL. Must be a public `https` endpoint with no query, fragment or credentials. If not provided, the default Walrus configuration will be used. See [Endpoint targets](#endpoint-targets).

_opt_ **`epochs`: [`u64`]** _default_: [`1`]

Number of epochs to store the file.

_opt_ **`send_to`: [`Option<String>`]** _default_: [`None`]

Optional address to which the created Blob object should be sent.

## Output Variants & Ports

**`newly_created`**

A new blob was created and uploaded successfully.

- **`newly_created.blob_id`: [`String`]** - The unique identifier for the uploaded blob
- **`newly_created.end_epoch`: [`u64`]** - The epoch at which the blob will expire
- **`newly_created.sui_object_id`: [`String`]** - Sui object ID of the newly created blob

**`already_certified`**

The blob was already certified in the blockchain.

- **`already_certified.blob_id`: [`String`]** - The unique identifier for the blob
- **`already_certified.end_epoch`: [`u64`]** - The epoch at which the blob will expire
- **`already_certified.tx_digest`: [`String`]** - Transaction digest of the certified blob

**`err`**

The file upload failed.

- **`err.reason`: [`String`]** - A detailed error message describing what went wrong
- **`err.kind`: [`UploadErrorKind`]** - Type of error that occurred
  - Possible kinds:
    - `network` - Error during HTTP requests or network connectivity issues
    - `validation` - Invalid file data or file validation failures

# `xyz.taluslabs.storage.walrus.read-json@1`

Standard Nexus Tool that reads a JSON file from Walrus and returns the JSON data. The tool can also validate the JSON data against a provided schema.

## Input

**`blob_id`: [`String`]**

The blob ID of the JSON file to read.

_opt_ **`aggregator_url`: [`Option<String>`]** _default_: [`None`]

The Walrus aggregator URL. Must be a public `https` endpoint with no query, fragment or credentials. If not provided, the default Walrus configuration will be used. See [Endpoint targets](#endpoint-targets).

_opt_ **`json_schema`: [`Option<WalrusJsonSchema>`]** _default_: [`None`]

Optional JSON schema to validate the data against.

### WalrusJsonSchema Structure

- **`name`: [`String`]** - The name of the schema. Must match `[a-zA-Z0-9-_]`, with a maximum length of 64.
- **`schema`: [`schemars::Schema`]** - The JSON schema for the expected output.
- **`description`: [`Option<String>`]** - A description of the expected format.
- **`strict`: [`Option<bool>`]** - Whether to enable strict schema adherence when validating the output.

## Output Variants & Ports

**`ok`**

The JSON data was read successfully.

- **`ok.json`: [`Value`]** - The JSON data as a structured value

**`err`**

The JSON read operation failed.

- **`err.reason`: [`String`]** - A detailed error message describing what went wrong
- **`err.kind`: [`ReadErrorKind`]** - Type of error that occurred
  - Possible kinds:
    - `network` - Error during HTTP requests or network connectivity issues
    - `validation` - Invalid JSON data format or parsing failures
    - `schema` - Error validating the JSON against the provided schema
- **`err.status_code`: [`Option<u16>`]** - HTTP status code if available (for network errors)

---

# `xyz.taluslabs.storage.walrus.read-file@1`

Standard Nexus Tool that reads a file from Walrus and returns its content as bytes.

## Input

**`blob_id`: [`String`]**

The unique identifier of the blob to read.

_opt_ **`aggregator_url`: [`Option<String>`]** _default_: [`None`]

The Walrus aggregator URL. Must be a public `https` endpoint with no query, fragment or credentials. If not provided, the default Walrus configuration will be used. See [Endpoint targets](#endpoint-targets).

## Output Variants & Ports

**`ok`**

The file was read successfully.

- **`ok.bytes`: [`Vec<u8>`]** - The file content as a byte array

**`err`**

The file read operation failed.

- **`err.reason`: [`String`]** - A detailed error message describing what went wrong
- **`err.kind`: [`ReadErrorKind`]** - Type of error that occurred
  - Possible kinds:
    - `network` - Error during HTTP requests or network connectivity issues
- **`err.status_code`: [`Option<u16>`]** - HTTP status code if available (for network errors)

---

# `xyz.taluslabs.storage.walrus.verify-blob@1`

Standard Nexus Tool that verifies a blob in Walrus.

## Input

**`blob_id`: [`String`]**

The ID of the blob to verify.

_opt_ **`aggregator_url`: [`Option<String>`]** _default_: [`None`]

The Walrus aggregator URL. Must be a public `https` endpoint with no query, fragment or credentials. If not provided, the default Walrus configuration will be used. See [Endpoint targets](#endpoint-targets).

## Output Variants & Ports

**`verified`**

The blob exists and is verified.

- **`verified.blob_id`: [`String`]** - The ID of the verified blob

**`unverified`**

The blob does not exist or could not be verified.

- **`unverified.blob_id`: [`String`]** - The ID of the unverified blob

**`err`**

An error occurred during verification.

- **`err.reason`: [`String`]** - A detailed error message describing what went wrong
- **`err.kind`: [`UploadErrorKind`]** - Type of error that occurred
  - Possible kinds:
    - `server` - Server-side errors during verification
- **`err.status_code`: [`Option<u16>`]** - HTTP status code if available (for API errors)

---

# Configuration

## Endpoint targets

`publisher_url` and `aggregator_url` are caller-supplied. Pointing them at an
aggregator of your own is the point of having them, so any **public** `https`
endpoint is accepted, on any port. What is refused is `http` and the private side
of the network: the cloud metadata server, the container's own loopback, and the
VPC the tool sits in.

That is enforced in two places, because refusing `169.254.169.254` and
`metadata.google.internal` by name is a one-line bypass away from useless — any
public name can carry a private address:

- While the input is deserialized: a non-public IP literal, an internal domain
  suffix (`.internal`, `.local`, `.localhost`, `.home.arpa`, `.arpa`), or a
  single-label name. The last one matters because a bare `metadata` resolves
  through the container's DNS search list, which on GCE ends at
  `google.internal`.
- While the client is built: the host is resolved, refused unless every address
  it answers with is public, and then **pinned** onto the HTTP client. Pinning
  is what makes the check binding — without it the connection does its own
  lookup, and a name with alternating records passes the check and then connects
  to the private address.

**Redirects are refused, not followed.** A DNS pin binds only the host it names,
so a redirect is the one way a request can leave the host that was checked. A
validated public endpoint answering `302 Location: http://127.0.0.1/…` would
otherwise be fetched and its body handed back. Walrus publishers and aggregators
serve their blob routes directly, so nothing legitimate needs a redirect; one
surfaces as an API error carrying the 3xx status.

A URL must also carry no query, fragment or credentials. The SDK builds request
URLs by concatenation (`{base}/v1/blobs/{id}`), so a base ending in `#` or `?`
swallows everything appended to it and turns a blob read into a request for the
host's root. A path is fine and concatenates as expected, so an aggregator
served under a prefix works.

Community aggregators that are only reachable over `http` cannot be used. Blob
contents and blob IDs would otherwise cross the network in the clear, and a
plaintext hop is a place for someone to substitute what the tool reads.

Only values passed through the input ports are checked. `WALRUS_PUBLISHER_URL`
and `WALRUS_AGGREGATOR_URL` are deployment configuration, and an operator
pointing the tool at a publisher inside their own network is a legitimate setup.

## Local file uploads

`upload-file`'s `file_path` is confined to one directory, named by
**`WALRUS_UPLOAD_ROOT`**. The path is interpreted relative to that directory and
cannot leave it: absolute paths and `..` are refused outright, and containment is
re-checked after symlink resolution.

With `WALRUS_UPLOAD_ROOT` unset — the default, and how the hosted tools run —
`file_path` is refused entirely. A hosted instance has its toolkit signing key on
a mounted volume and nothing a caller would legitimately want published, so a
local-read port there is only useful for exfiltrating secrets into public
storage. Turn it on deliberately, pointed at a directory that holds the files you
mean to publish, and nothing else.

Callers that want to publish content they supply themselves should use
`upload-json`, which takes the bytes inline.
