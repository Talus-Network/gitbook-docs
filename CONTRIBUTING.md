# Contributing to Talus Network Documentation

Thank you for your interest in contributing to the Talus documentation! This repository serves as the source for our Gitbook documentation, and we welcome contributions to improve our documentation.

## Branching Strategy

- The default branch is `staging`
- All pull requests should target the `staging` branch
- We use feature branches directly in this repository (no forks)
- Branch naming convention: `feature/your-feature-name` or `fix/your-fix-name`

## Contribution Workflow

1. Create a new branch from `staging`
2. Make your changes
3. Commit your changes with clear, descriptive commit messages
4. Push your branch and create a pull request targeting `staging`
5. Wait for review and address any feedback
6. Once approved, your changes will be merged into `staging`

## Gitbook Requirements

This documentation is rendered using Gitbook, so all contributions must follow Gitbook's syntax and structure rules:

- Use Markdown syntax as specified in the [Gitbook documentation](https://docs.gitbook.com/editing-content/markdown)
- Follow the existing directory structure and file naming conventions
- Ensure proper heading hierarchy (H1, H2, H3, etc.)
- Use Gitbook-specific features like callouts, tabs, and code blocks appropriately
- Test your changes in the Gitbook preview before submitting

## Important Note About Synced Content

This documentation repository is a hybrid of:
- Directly maintained content (either in this repo or via Gitbook web editor)
- Synced content from source repositories

### Synced Content Sections

The following sections are synced from their respective source repositories and should **NOT** be modified directly in this repository:

- `nexus-next/` - Synced from private repository
- `nexus-sdk/` - Synced from [nexus-sdk](https://github.com/talus-network/nexus-sdk)

For these sections, please contribute directly to the `/docs` folder in their respective source repositories (provided they are public). This ensures that your changes are properly tracked and maintained in the original source.

## Getting Help

If you have any questions about contributing or need help with your contribution, please:
1. Check existing issues and discussions
2. Create a new issue if your question hasn't been addressed
3. Reach out to the maintainers

## Code of Conduct

Please be respectful and considerate of others when contributing. We expect all contributors to follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

Thank you for contributing to making our documentation better! 