"""
promptfoo provider for the Deal Desk evals. It runs one case and returns the agent's
answer as `output`, and the judge's structured readout as `metadata.extraction`,
which the checks in grading.py read.

EVAL_MODE (set it on the command line, e.g. `EVAL_MODE=fake-oracle evals/pf eval`):
  live          default: run the real agent, then the readout        real money (capped)
  reuse         re-grade the last saved live run of each case/rep    $0 once readouts are cached
  oracle        grade the reference answers with the real judge      judge only, cents
  null          grade an empty answer with the real judge            judge only, cents
  fake-oracle   reference answers + perfect readouts, no API calls   $0: wiring check
  fake-null     empty answers + blank readouts, no API calls         $0: wiring check
"""

from __future__ import annotations

import contextlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]

import cases  # noqa: E402
import grading  # noqa: E402
import harness  # noqa: E402
import oracles  # noqa: E402


def call_api(prompt, options, context):
    with contextlib.redirect_stdout(sys.stderr):  # keep library chatter off promptfoo's channel
        return answer(context)


def answer(context: dict) -> dict:
    case = cases.BY_ID.get((context.get("vars") or {}).get("case_id"))
    if case is None:
        return {"error": f"[config] unknown case {(context.get('vars') or {}).get('case_id')!r}"}
    mode = os.environ.get("EVAL_MODE", "live")
    rep = int(context.get("repeatIndex") or 0)
    try:
        if mode == "live":
            run = harness.run(case)
            harness.save_run(case, rep, run)
        elif mode == "reuse":
            run = harness.load_run(case, rep)
        elif mode in ("oracle", "fake-oracle"):
            run = oracles.run(case)
        elif mode in ("null", "fake-null"):
            run = oracles.empty_run(case)
        else:
            raise harness.EvalError("config", f"unknown EVAL_MODE {mode!r}")

        if mode == "fake-oracle":
            readout, judge = grading.gold(case), {}
        elif mode == "fake-null":
            readout, judge = grading.blank(case), {}
        else:
            readout, judge = grading.extract(case, run["text"], run.get("agent_model", ""))
    except harness.EvalError as error:
        return {"error": f"[{error.failure_class}] {error}"}

    usage_in = (run.get("input_tokens") or 0) + (judge.get("usage") or {}).get("input_tokens", 0)
    usage_out = (run.get("output_tokens") or 0) + (judge.get("usage") or {}).get("output_tokens", 0)
    response = {
        "output": run["text"] or "(no answer)",
        "cost": (run.get("cost_usd") or 0) + (judge.get("cost_usd") or 0),
        "tokenUsage": {"prompt": usage_in, "completion": usage_out, "total": usage_in + usage_out},
        "metadata": {"mode": mode, "extraction": readout, "judge": judge,
                     "run": {k: v for k, v in run.items() if k != "text"}},
    }
    if run.get("latency_s"):
        response["latencyMs"] = int(run["latency_s"] * 1000)
    return response
