# Agent Cost Guard 💰

> Stop surprise AI bills. Track, budget, and optimize your agent spending.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-green.svg)]()
[![Skill](https://img.shields.io/badge/type-agent--skill-blue.svg)]()

## The Pain

**You're spending money. You don't know how much.**

- "How much did today's 6-hour coding session cost?"
- "Why is my Claude bill $200 this month?"
- "I'd use cheaper models for simple tasks but always forget"
- "My team blew through the AI budget in week one"

**free-claude-code trending at 13.7K★ (+1.7K today) proves cost is the #1 AI agent pain point.**

mattpocock/skills (24K★, +2.5K today) shows practical skills beat concepts — cost tracking is pure utility.

## The Solution

Agent Cost Guard gives you **visibility and control**:

```
💰 This Session: $3.47
├─ Claude Opus 4: $2.81 (81%)
└─ Claude Sonnet 4: $0.66 (19%)

📊 Today: $7.23 / $10 daily budget
⚠️  Alert: 72% of budget used
💡 Tip: 12 simple edits could use Haiku → Save $4.20
```

## Quick Start

```bash
# Install
git clone https://github.com/aptratcn/agent-cost-guard.git ~/.agent-skills/

# Check status
cost-status

# Set daily budget ($10)
cost-budget --daily 10

# See history
cost-history --7d

# Get recommendations
cost-optimize
```

## Features

| Feature | What it Does | Why It Matters |
|---------|--------------|----------------|
| **Real-time tracking** | Estimates cost per task | Know before the bill |
| **Budget alerts** | Warn at 70%, stop at 100% | Never overspend again |
| **Model recommendations** | "Use Haiku for this" | Save 60-80% on simple tasks |
| **Cost reports** | By project, task, time | Track where money goes |

## Example Session

```bash
$ cost-status

┌──────────────────────────────────────────────┐
│ 💰 Agent Cost Guard — Session Summary        │
├──────────────────────────────────────────────┤
│ Session Time: 2h 34m                         │
│ Tasks Completed: 23                          │
│                                              │
│ 💵 Cost Breakdown:                           │
│ ├─ Complex Debug (Opus 4): $4.12 (60%)      │
│ ├─ Code Review (Sonnet): $1.87 (27%)        │
│ └─ Quick Edits (Sonnet): $0.89 (13%)        │
│ Total: $6.88                                 │
│                                              │
│ 📊 Budget Status:                            │
│ Daily: $6.88 / $10.00 (69%) ⚠️              │
│ Monthly: $143.21 / $200.00 (72%)             │
│                                              │
│ 💡 This Session Insights:                    │
│ • 8 quick edits could use Haiku (-$2.10)    │
│ • Batch 3 similar queries (-$0.80)          │
│ Potential savings: $2.90                     │
└──────────────────────────────────────────────┘
```

## How It Helps

### Before Cost Guard
```
月末看账单：$347
你："？？？怎么花了这么多？"
Agents: 🤷‍♂️
```

### After Cost Guard
```
每天：预算 $10，已用 $7.23，收到提醒
周报：本周 $48，建议省 $12（用 Haiku 替代简单任务）
你：心中有数，主动优化
```

## Model Pricing Reference

| Model | Prompt ($/1M) | Completion ($/1M) | Best For |
|-------|--------------|-------------------|----------|
| Claude Opus 4 | $15 | $75 | Complex debug, architecture |
| Claude Sonnet 4 | $3 | $15 | Most coding tasks |
| Claude Haiku 3.5 | $0.80 | $4 | Simple edits, comments |
| GPT-4o | $2.50 | $10 | General tasks |
| GPT-4o-mini | $0.15 | $0.60 | Quick queries |

**Rule of thumb:** Haiku for tasks you'd trust a junior dev, Opus for problems that need a principal engineer.

## Why Not Other Solutions?

| Solution | Problem |
|----------|---------|
| Check billing dashboard | After the fact, no prevention |
| Set API limits | Hard cutoffs, no visibility |
| Use cheaper models manually | Easy to forget |
| **Agent Cost Guard** | Prevention + visibility + recommendations |

## Configuration

`.cost-guard.json`:
```json
{
  "dailyBudget": 10,
  "monthlyBudget": 200,
  "warnThreshold": 70,
  "stopThreshold": 100,
  "defaultModel": "claude-sonnet-4",
  "cheapModel": "claude-haiku-3.5",
  "premiumModel": "claude-opus-4"
}
```

## Real Savings

Typical developer using AI agents 4 hours/day:
- Without optimization: ~$200/month
- With Cost Guard recommendations: ~$120/month
- **Savings: $80/month = $960/year**

**Team scenario (10 devs): $9,600/year saved**

## Installation

```bash
# Option 1: Clone to skills directory
git clone https://github.com/aptratcn/agent-cost-guard.git ~/.agent-skills/

# Option 2: Add to AGENTS.md
echo "- agent-cost-guard: ~/.agent-skills/agent-cost-guard" >> AGENTS.md
```

## Related Projects

- [context-mode](https://github.com/mksglu/context-mode) — Context window optimization
- [claude-mem](https://github.com/thedotmack/claude-mem) — Session memory
- [free-claude-code](https://github.com/Alishahar1/free-claude-code) — Free Claude Code access

## License

MIT

---

**Stop guessing. Start tracking.** 📊
