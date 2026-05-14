# Runnable subagents

This folder holds the thin runnable subagent wrappers. Each one delegates to a *persona file* that lives inside the monitor it serves — that's where the substance lives. Update the persona, not the wrapper.

## Wiring

```
.claude/agents/m01-orchestrator.md      →  monitors/monitor-01/agents/00-orchestrator.md
.claude/agents/m01-regulations.md       →  monitors/monitor-01/agents/01-regulations.md
.claude/agents/m01-sourcing.md          →  monitors/monitor-01/agents/02-sourcing-connecting.md
.claude/agents/m01-workflow.md          →  monitors/monitor-01/agents/03-static-workflow.md
.claude/agents/m01-legal-reasoning.md   →  monitors/monitor-01/agents/04-legal-reasoning.md
.claude/agents/m01-adjudicator.md       →  monitors/monitor-01/agents/05-adjudicator.md
.claude/agents/m02-orchestrator.md      →  monitors/monitor-02-eu-competition/agents/00-orchestrator.md
.claude/agents/m02-regulations.md       →  monitors/monitor-02-eu-competition/agents/01-regulations.md
.claude/agents/m02-sourcing.md          →  monitors/monitor-02-eu-competition/agents/02-sourcing-connecting.md
.claude/agents/m02-workflow.md          →  monitors/monitor-02-eu-competition/agents/03-static-workflow.md
.claude/agents/m02-legal-reasoning.md   →  monitors/monitor-02-eu-competition/agents/04-legal-reasoning.md
.claude/agents/m02-adjudicator.md       →  monitors/monitor-02-eu-competition/agents/05-adjudicator.md
.claude/agents/clipper-ingest.md        →  monitor-scoped Sourcing & Connecting (auto-detects which monitor's inbox to sweep)
```

## How to invoke

From Claude in this repo, ask Claude to invoke the subagent by name. For example:

> Run the M01 weekly cycle.
> Run M02 Sourcing & Connecting against this week's inbox.
> Sweep the clipper inbox.
> Have the M02 Adjudicator produce this week's brief draft.

Claude picks the right subagent from the description. The subagent reads its persona file and follows it.

## When to edit a wrapper vs a persona

- **Edit the persona** when you want to change *how* the agent thinks — its mission, inputs, process, output schema, failure modes.
- **Edit the wrapper** only when you want to change *what tools* the agent is allowed to use or *when* Claude should auto-select it (the `description` field). Wrappers should rarely change.
