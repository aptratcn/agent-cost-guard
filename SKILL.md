# Agent Cost Guard 💰

> Track, budget, and optimize AI agent spending. Stop surprise bills before they happen.

## Problem

You're using AI coding agents. They're burning tokens. You have no idea how much you've spent until the invoice arrives.

**Real pain points:**
- "I spent $400 this month on Claude Code but don't know what for"
- "My agent ran a 2-hour debug session and I only found out later it cost $50"
- "I'd use cheaper models for simple tasks but never remember to switch"
- "Team budgets? What team budgets?"

**free-claude-code trending with 9K+ stars proves this is a top concern.**

## Solution

Agent Cost Guard is a lightweight skill that:
1. **Tracks** token usage per session/project/task
2. **Budgets** Sets spending limits with alerts before you overspend
3. **Optimizes** Suggests cheaper models for appropriate tasks
4. **Reports** Shows exactly where your money went

## Installation

```bash
# Clone to your skills directory
git clone https://github.com/aptratcn/agent-cost-guard.git ~/.agent-skills/agent-cost-guard
```

Or add to your AGENTS.md:
```markdown
## Skills
- agent-cost-guard: ~/.agent-skills/agent-cost-guard
```

## Quick Start

```bash
# Check current session cost
cost-status

# Set daily budget
cost-budget --daily 10

# Set project budget (per project)
cost-budget --project 50

# View spending history
cost-history --7d

# Get model recommendations
cost-optimize
```

## Features

### 1. Real-Time Cost Tracking

Automatically estimates costs based on:
- Token count (prompt + completion)
- Current model pricing
- Task type (chat, edit, debug, etc.)

```
┌─────────────────────────────────────┐
│ 💰 Session Cost: $2.34              │
│ ├─ Claude Opus 4: $1.87 (80%)      │
│ └─ Claude Sonnet 4: $0.47 (20%)    │
│                                     │
│ 📊 Today: $5.12 / $10.00 budget    │
│ ⚠️  Budget: 51% used               │
└─────────────────────────────────────┘
```

### 2. Budget Alerts

Set limits and get warnings:
- `--warn`: Alert at 70% budget
- `--stop`: Refuse non-essential tasks at 100%
- `--hard`: Block all AI calls at limit

```bash
# Warn at $7, stop at $10
cost-budget --daily 10 --warn 70 --stop 100
```

### 3. Model Recommendations

Analyzes your task patterns and suggests:
- Tasks where cheaper models suffice (quick edits, comments)
- Tasks needing premium models (complex debugging, architecture)
- Potential savings per week

```
💡 Optimization Suggestions:

1. Use Claude Haiku for documentation tasks
   → Saves ~$15/week (23 tasks identified)

2. Switch to Claude Sonnet for simple refactors
   → Saves ~$8/week (45 tasks identified)

3. Batch similar queries together
   → Reduces context re-read costs ~$5/week

Total potential savings: $28/week ($112/month)
```

### 4. Cost Reports

Breakdown by:
- Project
- Task type
- Time period
- Model used

```bash
cost-report --this-month --by-project
cost-report --last-week --by-task
```

## Configuration

Create `.cost-guard.json` in your project root:

```json
{
  "dailyBudget": 10,
  "projectBudget": 100,
  "warnThreshold": 70,
  "defaultModel": "claude-sonnet-4",
  "cheapModel": "claude-haiku-3.5",
  "premiumModel": "claude-opus-4",
  "trackCommands": true,
  "logFile": "~/.cost-guard/history.jsonl"
}
```

## Model Pricing (2026-04)

Model pricing used for estimates (update in config):

| Model | Prompt/1M | Completion/1M |
|-------|-----------|---------------|
| Claude Opus 4 | $15 | $75 |
| Claude Sonnet 4 | $3 | $15 |
| Claude Haiku 3.5 | $0.80 | $4 |
| GPT-4o | $2.50 | $10 |
| GPT-4o-mini | $0.15 | $0.60 |

## How It Works

1. **Token Estimation**: Counts tokens in prompts + completions
2. **Cost Calculation**: Applies current pricing
3. **Budget Enforcement**: Checks limits before processing
4. **Recommendations**: Analyzes patterns, suggests optimizations

## Integration Points

Works with:
- Claude Code
- Cursor
- Codex CLI
- Gemini CLI
- OpenClaw
- Any agent with AGENTS.md support

## Why This Skill?

- **free-claude-code**: 9K+ stars — cost is #1 pain point
- **context-mode**: 9.8K stars — context optimization
- **claude-mem**: 67K stars — memory systems

Cost control is proven demand. This skill provides a **lightweight, agent-agnostic** solution.

## Use Cases

1. **Solo developers**: Track personal spending, set weekly limits
2. **Teams**: Enforce project budgets, see who's spending what
3. **Startups**: Predict AI costs before they surprise you
4. **Agencies**: Bill AI costs to clients accurately

## Philosophy

- **Zero dependencies**: Pure Bash/Python, no npm bloat
- **Privacy-first**: All data stays local
- **Agent-agnostic**: Works with any AI coding agent
- **Actionable**: Not just reports, but recommendations

## Related Skills

- `skill-token-analyzer`: Deep token analysis
- `skill-model-router`: Auto-route to best model
- `skill-health-monitor`: General agent health

## License

MIT

## Author

aptratcn — Practical AI agent skills
