"""第1回 宿題（基礎）: 同じ質問を、モデルを変えて3回ずつ実行して比べる。

使い方:
    PYTHONPATH=. uv run python scripts/lec01_basic.py

結果は lectures/01/basic_runs.md に書き出す（回答の全文・トークン数・応答時間）。
gemini-3.8-flash は無料枠のレート制限が厳しいため、1回ごとに15秒待つ。
"""

import time
from pathlib import Path

from google import genai
from google.genai import errors

from app.ask import DEFAULT_QUESTION
from app.config import api_error_message, get_api_key

MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
RUNS = 3
WAIT_SECONDS = 15
OUTPUT = Path(__file__).resolve().parent.parent / "lectures" / "01" / "basic_runs.md"


def main() -> None:
    client = genai.Client(api_key=get_api_key())
    lines = ["# 第1回 宿題（基礎）実行ログ", "", f"質問: {DEFAULT_QUESTION}", ""]

    for model in MODELS:
        lines += [f"## {model}", ""]
        for i in range(1, RUNS + 1):
            print(f"[{model}] {i}/{RUNS} ...", flush=True)
            start = time.perf_counter()
            try:
                response = client.models.generate_content(model=model, contents=DEFAULT_QUESTION)
            except errors.APIError as e:
                lines += [f"### {i}回目", "", f"エラー: {api_error_message(e.code, e.message)}", ""]
            else:
                elapsed = time.perf_counter() - start
                usage = response.usage_metadata
                tokens = (
                    f"入力 {usage.prompt_token_count} / 出力 {usage.candidates_token_count}"
                    if usage is not None
                    else "取得できず"
                )
                lines += [
                    f"### {i}回目（{elapsed:.1f}秒、トークン {tokens}）",
                    "",
                    response.text or "（空の応答）",
                    "",
                ]
            time.sleep(WAIT_SECONDS)

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"書き出しました: {OUTPUT}")


if __name__ == "__main__":
    main()
