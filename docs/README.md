# Documentation map

Welcome to the **Resume Job Match Agent field manual**. It is written as a hands-on tutorial with 50 numbered Mermaid diagrams (40 across the first four chapters, plus 10 troubleshooting diagrams) and an original four-character developer squad to make the workflow easier to scan.

![Senpai, Kōhai, QA-chan, and Byte-kun](assets/dev-squad.webp)

## Read in order

| Chapter | Best for | Visuals |
|---|---|---:|
| [01 · Getting Started](01-getting-started.md) | Install Python, download the project, launch Streamlit, run your first analysis | 01–12 |
| [02 · Claude Integration](02-claude-integration.md) | Configure Claude Desktop or Claude Code and use all three MCP tools | 13–24 |
| [03 · Analysis Playbook](03-analysis-playbook.md) | Understand scoring, inspect evidence, improve a resume truthfully | 25–38 |
| [04 · Developer Guide](04-architecture-and-contributing.md) | Architecture, source files, vocabulary, scoring changes, tests, contributions | 39–40 |
| [05 · Troubleshooting](05-troubleshooting.md) | Fix Python, Streamlit, document, Claude, MCP, and scoring problems | 41–50 |

All 50 diagrams are written in Mermaid and render natively on GitHub.

## Character cast

- **Senpai:** system architecture and code review.
- **Kōhai:** beginner setup and command-line guidance.
- **QA-chan:** test discipline, evidence, and truthfulness.
- **Byte-kun:** Claude/MCP connections and tool calls.

These characters are original project mascots and do not represent dependencies or contributors.

## How to use this manual

1. Start with Chapter 01 if you are new to the repository.
2. Read Chapter 02 only when connecting Claude.
3. Use Chapter 03 whenever you need to interpret a report.
4. Use Chapter 04 before changing the code.
5. Jump to Chapter 05 when something breaks.

## Documentation conventions

- Commands are written for Windows PowerShell unless marked `bat`.
- Replace placeholders such as `YOUR_NAME` with your own values.
- Copy only commands that match your shell and current directory.
- A **match** is a text/vocabulary detection, not proof of proficiency.
- A **priority** is inferred from nearby job-description wording, not an authoritative classification.
- Never invent experience, qualifications, responsibilities, or metrics to improve a report.

## External references

- [Model Context Protocol — overview](https://modelcontextprotocol.io/docs/)
- [Official MCP Python SDK](https://py.sdk.modelcontextprotocol.io/)
- [MCP Python SDK — running a server](https://py.sdk.modelcontextprotocol.io/run/)
- [Claude Code MCP guide](https://code.claude.com/docs/en/mcp)
- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-usage)