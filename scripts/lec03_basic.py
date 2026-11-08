"""第3回 宿題（基礎）: INSTRUCTIONS とツールの説明文を1か所ずつ変え、同じ質問でのふるまいを比べる。

app/agent.py と app/tools.py のファイルは書き換えず、同じ指示・同じツールから
「1か所だけ違うエージェント」をこのスクリプトの中で組み立てて実行する。

使い方:
    uv run python scripts/lec03_basic.py                 # 全部の組み合わせを実行して lectures/03/basic_runs.md に書く
    uv run python scripts/lec03_basic.py --repeat 1      # 各組み合わせを1回ずつ
"""

import argparse
import time
from pathlib import Path

from pydantic_ai import Agent, Tool
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.messages import ToolCallPart, ToolReturnPart

from app import tools
from app.agent import INSTRUCTIONS, build_model
from app.config import MODEL

OUT = Path(__file__).resolve().parent.parent / "lectures" / "03" / "basic_runs.md"

MUST_SEARCH = "- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。\n"
ONE_TERM = 'query には調べたい用語を1つだけ入れる（例: "LoRA"）。'
MANY_TERMS = 'query には調べたい用語をまとめて入れる（例: "LoRA QLoRA"）。'

SEARCH_DOC = tools.search_glossary.__doc__
assert MUST_SEARCH in INSTRUCTIONS and ONE_TERM in SEARCH_DOC, "元の指示・説明文が想定と違う"


def build(instructions: str = INSTRUCTIONS, search_doc: str = SEARCH_DOC) -> Agent:
    """演習のエージェント（app/agent.py）と同じ3つのツールで組み立てる。変えるのは引数で渡した1か所だけ。"""
    return Agent(
        instructions=instructions,
        tools=[
            Tool(tools.search_glossary, description=search_doc),
            Tool(tools.get_lecture_summary),
            Tool(tools.make_quiz),
        ],
    )


VARIANTS = {
    "base": ("演習の状態（変更なし）", build()),
    "no-must-search": (
        "INSTRUCTIONS から「必ず search_glossary で用語集を確認する」の行を消す",
        build(instructions=INSTRUCTIONS.replace(MUST_SEARCH, "")),
    ),
    "many-terms": (
        "search_glossary の説明文の「1つだけ入れる」を「まとめて入れる」に変える",
        build(search_doc=SEARCH_DOC.replace(ONE_TERM, MANY_TERMS)),
    ),
}

Q_LEVELS = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
Q_LORA = "LoRAとQLoRAの違いは？"

PLAN = [
    ("base", Q_LEVELS),
    ("no-must-search", Q_LEVELS),
    ("base", Q_LORA),
    ("many-terms", Q_LORA),
    ("no-must-search", Q_LORA),
]


def run_once(agent: Agent, question: str):
    for attempt in range(3):
        try:
            start = time.perf_counter()
            result = agent.run_sync(question, model=build_model())
            return result, time.perf_counter() - start
        except ModelHTTPError as e:
            if e.status_code in (429, 503) and attempt < 2:
                print(f"  {e.status_code}: 60秒待って再試行")
                time.sleep(60)
                continue
            raise


def describe(result) -> tuple[list[str], list[str]]:
    calls, returns = [], []
    for message in result.all_messages():
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                calls.append(f"{part.tool_name}({part.args})")
            elif isinstance(part, ToolReturnPart):
                returns.append(f"{part.tool_name} -> {str(part.content)[:120]}…")
    return calls, returns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeat", type=int, default=2)
    parser.add_argument("--wait", type=float, default=8.0, help="実行の間に待つ秒数（無料枠のレート制限よけ）")
    args = parser.parse_args()

    lines = [
        "# 第3回 宿題（基礎）の実行ログ",
        "",
        f"- モデル: `{MODEL}`（既定の設定のまま。temperature などは変えていない）",
        "- 実行: `uv run python scripts/lec03_basic.py`",
        "- 各組み合わせを同じ質問で繰り返し実行し、ツール呼び出し・`requests`・回答の全文を残した",
        "",
        "## 比べたエージェント",
        "",
    ]
    for key, (label, _) in VARIANTS.items():
        lines.append(f"- `{key}`: {label}")
    lines.append("")

    rows = []
    for key, question in PLAN:
        label, agent = VARIANTS[key]
        for n in range(1, args.repeat + 1):
            print(f"[{key}] {question} ({n}回目)")
            result, seconds = run_once(agent, question)
            calls, returns = describe(result)
            usage = result.usage
            rows.append((key, question, n, seconds, usage.requests, usage.input_tokens, usage.output_tokens, calls))
            lines += [
                f"## `{key}` / {question} / {n}回目",
                "",
                f"- 応答時間: {seconds:.1f}秒",
                f"- usage: {usage}",
                "- ツール呼び出し:" + ("" if calls else " なし"),
                *[f"  - `{c}`" for c in calls],
                "- ツールの戻り値（先頭120文字）:" + ("" if returns else " なし"),
                *[f"  - `{r}`" for r in returns],
                "",
                "回答:",
                "",
                *[f"> {line}" if line else ">" for line in str(result.output).splitlines()],
                "",
            ]
            time.sleep(args.wait)

    summary = [
        "## まとめの表",
        "",
        "| エージェント | 質問 | 回 | 応答時間 | requests | 入力 / 出力トークン | ツール呼び出し |",
        "|---|---|---|---|---|---|---|",
    ]
    for key, question, n, seconds, requests, tin, tout, calls in rows:
        called = "<br>".join(f"`{c}`" for c in calls) or "なし"
        summary.append(f"| `{key}` | {question} | {n} | {seconds:.1f}秒 | {requests} | {tin} / {tout} | {called} |")
    summary.append("")

    head, body = lines[:lines.index("## 比べたエージェント")], lines[lines.index("## 比べたエージェント"):]
    OUT.write_text("\n".join(head + summary + body) + "\n", encoding="utf-8")
    print(f"書き出し: {OUT}")


if __name__ == "__main__":
    main()
