#!/usr/bin/env python3
"""
Agent Cost Guard - Core implementation
Tracks token usage, estimates costs, enforces budgets
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import argparse

# Model pricing (per 1M tokens)
MODEL_PRICING = {
    "claude-opus-4": {"prompt": 15, "completion": 75},
    "claude-sonnet-4": {"prompt": 3, "completion": 15},
    "claude-haiku-3.5": {"prompt": 0.80, "completion": 4},
    "gpt-4o": {"prompt": 2.50, "completion": 10},
    "gpt-4o-mini": {"prompt": 0.15, "completion": 0.60},
    "gemini-2.5-pro": {"prompt": 1.25, "completion": 10},
    "gemini-2.5-flash": {"prompt": 0.075, "completion": 0.30},
}

DEFAULT_CONFIG = {
    "dailyBudget": 10.0,
    "monthlyBudget": 200.0,
    "warnThreshold": 70,
    "stopThreshold": 100,
    "defaultModel": "claude-sonnet-4",
    "cheapModel": "claude-haiku-3.5",
    "premiumModel": "claude-opus-4",
    "trackCommands": True,
    "logFile": str(Path.home() / ".cost-guard" / "history.jsonl"),
}


class CostGuard:
    def __init__(self, config_path=None):
        self.config = self.load_config(config_path)
        self.log_file = Path(self.config["logFile"])
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def load_config(self, config_path):
        config = DEFAULT_CONFIG.copy()
        # Check for project-level config
        local_config = Path(".cost-guard.json")
        if local_config.exists():
            with open(local_config) as f:
                config.update(json.load(f))
        # Check for global config
        global_config = Path.home() / ".cost-guard" / "config.json"
        if global_config.exists():
            with open(global_config) as f:
                config.update(json.load(f))
        return config

    def estimate_tokens(self, text):
        """Estimate token count from text (rough: 1 token ≈ 4 chars)"""
        return len(text) // 4

    def calculate_cost(self, prompt_tokens, completion_tokens, model):
        """Calculate cost for a transaction"""
        pricing = MODEL_PRICING.get(model, MODEL_PRICING[self.config["defaultModel"]])
        prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]
        return prompt_cost + completion_cost

    def log_usage(self, prompt_tokens, completion_tokens, model, task_type="general"):
        """Log a usage event"""
        cost = self.calculate_cost(prompt_tokens, completion_tokens, model)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "model": model,
            "cost": round(cost, 4),
            "task_type": task_type,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def get_usage(self, period="day"):
        """Get total usage for a period"""
        now = datetime.now()
        if period == "day":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "month":
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start = datetime.min

        total_cost = 0
        total_tokens = 0
        by_model = {}
        by_task = {}

        if self.log_file.exists():
            with open(self.log_file) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        entry_time = datetime.fromisoformat(entry["timestamp"])
                        if entry_time >= start:
                            total_cost += entry["cost"]
                            total_tokens += entry.get("total_tokens", 0)
                            model = entry.get("model", "unknown")
                            by_model[model] = by_model.get(model, 0) + entry["cost"]
                            task = entry.get("task_type", "general")
                            by_task[task] = by_task.get(task, 0) + entry["cost"]
                    except (json.JSONDecodeError, KeyError):
                        continue

        return {
            "total_cost": round(total_cost, 2),
            "total_tokens": total_tokens,
            "by_model": {k: round(v, 2) for k, v in by_model.items()},
            "by_task": {k: round(v, 2) for k, v in by_task.items()},
        }

    def check_budget(self):
        """Check if we're within budget, return status"""
        daily = self.get_usage("day")
        daily_budget = self.config["dailyBudget"]
        daily_pct = (daily["total_cost"] / daily_budget) * 100 if daily_budget > 0 else 0

        status = "ok"
        if daily_pct >= self.config["stopThreshold"]:
            status = "exceeded"
        elif daily_pct >= self.config["warnThreshold"]:
            status = "warning"

        return {
            "status": status,
            "daily_used": daily["total_cost"],
            "daily_budget": daily_budget,
            "daily_pct": round(daily_pct, 1),
        }

    def get_recommendations(self):
        """Analyze usage and recommend optimizations"""
        usage = self.get_usage("week")
        recs = []

        # Check if using premium model for simple tasks
        if usage["by_task"].get("edit", 0) > 0:
            edit_cost = usage["by_task"]["edit"]
            potential_saving = edit_cost * 0.6  # Assume 60% could use cheaper model
            recs.append({
                "type": "model_switch",
                "message": f"Consider using {self.config['cheapModel']} for simple edits",
                "potential_saving": round(potential_saving, 2),
            })

        # Check for batching opportunity
        if usage["total_tokens"] > 100000:
            recs.append({
                "type": "batching",
                "message": "Batch similar queries to reduce context re-reads",
                "potential_saving": round(usage["total_cost"] * 0.1, 2),
            })

        return recs


def cmd_status(args):
    guard = CostGuard()
    budget_status = guard.check_budget()
    usage = guard.get_usage("day")

    print("💰 Agent Cost Guard — Status")
    print("=" * 40)
    print(f"\n📊 Today's Usage: ${usage['total_cost']:.2f} / ${budget_status['daily_budget']:.2f}")
    print(f"   Progress: {budget_status['daily_pct']:.1f}% of daily budget")

    if budget_status["status"] == "exceeded":
        print("   🛑 DAILY BUDGET EXCEEDED")
    elif budget_status["status"] == "warning":
        print("   ⚠️  Approaching daily limit")

    if usage["by_model"]:
        print("\n💵 By Model:")
        for model, cost in sorted(usage["by_model"].items(), key=lambda x: -x[1]):
            pct = (cost / usage["total_cost"] * 100) if usage["total_cost"] > 0 else 0
            print(f"   • {model}: ${cost:.2f} ({pct:.0f}%)")

    recs = guard.get_recommendations()
    if recs:
        print("\n💡 Recommendations:")
        for rec in recs:
            print(f"   • {rec['message']}")
            print(f"     Potential saving: ${rec['potential_saving']:.2f}")


def cmd_budget(args):
    guard = CostGuard()
    config_path = Path.home() / ".cost-guard" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    updates = {}
    if args.daily:
        updates["dailyBudget"] = float(args.daily)
    if args.monthly:
        updates["monthlyBudget"] = float(args.monthly)
    if args.warn:
        updates["warnThreshold"] = int(args.warn)
    if args.stop:
        updates["stopThreshold"] = int(args.stop)

    if updates:
        config = guard.config.copy()
        config.update(updates)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"✅ Budget updated:")
        for key, value in updates.items():
            print(f"   {key}: {value}")
    else:
        print("Current Budget Settings:")
        print(f"   Daily: ${guard.config['dailyBudget']}")
        print(f"   Monthly: ${guard.config['monthlyBudget']}")
        print(f"   Warn at: {guard.config['warnThreshold']}%")
        print(f"   Stop at: {guard.config['stopThreshold']}%")


def cmd_history(args):
    guard = CostGuard()

    if args.days:
        usage = guard.get_usage(f"last_{args.days}d")
    else:
        usage = guard.get_usage("month")

    print(f"📊 Cost History ({args.days or 30} days)")
    print("=" * 40)
    print(f"\n💵 Total: ${usage['total_cost']:.2f}")
    print(f"📊 Total Tokens: {usage['total_tokens']:,}")

    if usage["by_model"]:
        print("\nBy Model:")
        for model, cost in sorted(usage["by_model"].items(), key=lambda x: -x[1]):
            print(f"  {model}: ${cost:.2f}")

    if usage["by_task"]:
        print("\nBy Task Type:")
        for task, cost in sorted(usage["by_task"].items(), key=lambda x: -x[1]):
            print(f"  {task}: ${cost:.2f}")


def cmd_optimize(args):
    guard = CostGuard()

    print("💡 Optimization Suggestions")
    print("=" * 40)

    recs = guard.get_recommendations()
    if not recs:
        print("\nNo specific recommendations yet.")
        print("Use agent more to generate usage patterns.")
        return

    total_saving = sum(r["potential_saving"] for r in recs)

    for i, rec in enumerate(recs, 1):
        print(f"\n{i}. [{rec['type'].upper()}] {rec['message']}")
        print(f"   Potential saving: ${rec['potential_saving']:.2f}/week")

    print(f"\n💰 Total potential savings: ${total_saving:.2f}/week (${total_saving * 4:.2f}/month)")


def main():
    parser = argparse.ArgumentParser(description="Agent Cost Guard")
    subparsers = parser.add_subparsers(dest="command")

    # status command
    status_parser = subparsers.add_parser("status", help="Show current cost status")
    status_parser.set_defaults(func=cmd_status)

    # budget command
    budget_parser = subparsers.add_parser("budget", help="Set or view budget")
    budget_parser.add_argument("--daily", help="Daily budget in $")
    budget_parser.add_argument("--monthly", help="Monthly budget in $")
    budget_parser.add_argument("--warn", help="Warn threshold %")
    budget_parser.add_argument("--stop", help="Stop threshold %")
    budget_parser.set_defaults(func=cmd_budget)

    # history command
    history_parser = subparsers.add_parser("history", help="View cost history")
    history_parser.add_argument("--days", type=int, default=7, help="Days to show")
    history_parser.set_defaults(func=cmd_history)

    # optimize command
    optimize_parser = subparsers.add_parser("optimize", help="Get optimization suggestions")
    optimize_parser.set_defaults(func=cmd_optimize)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
