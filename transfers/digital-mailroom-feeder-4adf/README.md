# Temporary transfer: Digital-Mailroom feeder-import bundle

Ephemeral object for
[`LLM-Mailroom-Services/Digital-Mailroom`](https://github.com/LLM-Mailroom-Services/Digital-Mailroom)
branch `cursor/feeder-pull-dojo-sandbox-4adf`.

The Digital-Mailroom origin token used by this cloud agent cannot push
(`cursor[bot]` 403). The GitHub MCP identity (Exios66) can create the
branch and open the PR, so the commit objects are published here as a
`git bundle` (base64) and applied by a one-shot Actions workflow on
that Digital-Mailroom branch.

- Bundle of `origin/main..04794b34` (feeder overlays + v0.19.1 pins + vendor refresh).
- Prerequisites already on Digital-Mailroom `main`: `6fd28f43`, `15a9c706`, `08cd80ca`.
- Delete this directory after the Digital-Mailroom PR is opened and the
  workflow has fast-forwarded the PR branch.
