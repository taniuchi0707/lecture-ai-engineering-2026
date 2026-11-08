# 第3回 宿題（基礎）の実行ログ

- モデル: `gemini-3.5-flash-lite`（既定の設定のまま。temperature などは変えていない）
- 実行: `PYTHONPATH=. uv run python scripts/lec03_basic.py`
- 各組み合わせを同じ質問で繰り返し実行し、ツール呼び出し・`requests`・回答の全文を残した

## まとめの表

| エージェント | 質問 | 回 | 応答時間 | requests | 入力 / 出力トークン | ツール呼び出し |
|---|---|---|---|---|---|---|
| `base` | AIE2026の講座の宿題にある「3レベル」とは何ですか？ | 1 | 3.4秒 | 2 | 1029 / 132 | `search_glossary({'query': '3レベル'})` |
| `base` | AIE2026の講座の宿題にある「3レベル」とは何ですか？ | 2 | 2.6秒 | 2 | 1029 / 121 | `search_glossary({'query': '3レベル'})` |
| `no-must-search` | AIE2026の講座の宿題にある「3レベル」とは何ですか？ | 1 | 5.8秒 | 2 | 981 / 129 | `search_glossary({'query': '3レベル'})` |
| `no-must-search` | AIE2026の講座の宿題にある「3レベル」とは何ですか？ | 2 | 2.3秒 | 2 | 981 / 123 | `search_glossary({'query': '3レベル'})` |
| `no-search-hint` | AIE2026の講座の宿題にある「3レベル」とは何ですか？ | 1 | 1.8秒 | 2 | 921 / 136 | `search_glossary({'query': '3レベル'})` |
| `no-search-hint` | AIE2026の講座の宿題にある「3レベル」とは何ですか？ | 2 | 2.1秒 | 2 | 921 / 116 | `search_glossary({'query': '3レベル'})` |
| `base` | LoRAとQLoRAの違いは？ | 1 | 3.4秒 | 2 | 1442 / 219 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})` |
| `base` | LoRAとQLoRAの違いは？ | 2 | 2.2秒 | 2 | 1442 / 201 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})` |
| `no-must-search` | LoRAとQLoRAの違いは？ | 1 | 1.9秒 | 2 | 1394 / 209 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})` |
| `no-must-search` | LoRAとQLoRAの違いは？ | 2 | 2.0秒 | 2 | 1394 / 176 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})` |
| `no-search-hint` | LoRAとQLoRAの違いは？ | 1 | 2.2秒 | 2 | 1334 / 202 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})` |
| `no-search-hint` | LoRAとQLoRAの違いは？ | 2 | 1.8秒 | 2 | 1334 / 203 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})` |
| `many-terms` | LoRAとQLoRAの違いは？ | 1 | 2.6秒 | 2 | 1137 / 173 | `search_glossary({'query': 'LoRA QLoRA'})` |
| `many-terms` | LoRAとQLoRAの違いは？ | 2 | 2.2秒 | 2 | 1137 / 271 | `search_glossary({'query': 'LoRA QLoRA'})` |
| `quiz-at-end` | LoRAとQLoRAの違いは？ | 1 | 2.9秒 | 3 | 2519 / 241 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})`<br>`make_quiz({'lecture': 2})` |
| `quiz-at-end` | LoRAとQLoRAの違いは？ | 2 | 2.0秒 | 2 | 1536 / 270 | `search_glossary({'query': 'LoRA'})`<br>`search_glossary({'query': 'QLoRA'})`<br>`make_quiz({'lecture': 1})` |

## 比べたエージェント

- `base`: 演習の状態（変更なし）
- `no-must-search`: INSTRUCTIONS から「必ず search_glossary で用語集を確認する」の行を消す
- `many-terms`: search_glossary の説明文の「1つだけ入れる」を「まとめて入れる」に変える
- `quiz-at-end`: INSTRUCTIONS の「回答の最後に、関係する回（第N回）を示す」を「回答の最後に、確認問題を1問出す」に変える
- `no-search-hint`: 追加の確認（2か所）：no-must-search に加えて、search_glossary の説明文の「…について答える前に使うこと。」も消す

## `base` / AIE2026の講座の宿題にある「3レベル」とは何ですか？ / 1回目

- 応答時間: 3.4秒
- usage: RunUsage(cost=Decimal('0.0006387'), details={'text_prompt_tokens': 1029}, input_text_tokens=1029, input_tokens=1029, output_tokens=132, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': '3レベル'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…`

回答:

> AIエンジニアリング講座（AIE2026）における「3レベル」とは、各回の宿題の構成を指しています。具体的には以下の3つの段階に分かれています。
>
> 1. **基礎**：講義内容の確認
> 2. **実装**：自分でコードを書く
> 3. **発展**：調査や試行
>
> いずれか1つのレベルに取り組めば、その回の宿題は完了となります。なお、原則として採点は行われません。
>
> 第1回（第1回の講義）

## `base` / AIE2026の講座の宿題にある「3レベル」とは何ですか？ / 2回目

- 応答時間: 2.6秒
- usage: RunUsage(cost=Decimal('0.0006112'), details={'text_prompt_tokens': 1029}, input_text_tokens=1029, input_tokens=1029, output_tokens=121, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': '3レベル'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…`

回答:

> AIE2026の講座における「3レベル」とは、宿題の構成（段階）のことです。
>
> 宿題には以下の3つのレベルが用意されており、受講者はどれか1つに取り組めばその回の宿題完了となります。原則として採点も行われません。
>
> 1. **基礎**：講義内容の確認
> 2. **実装**：自分でコードを書く
> 3. **発展**：調査や試行
>
> （第1回）

## `no-must-search` / AIE2026の講座の宿題にある「3レベル」とは何ですか？ / 1回目

- 応答時間: 5.8秒
- usage: RunUsage(cost=Decimal('0.0006168'), details={'text_prompt_tokens': 981}, input_text_tokens=981, input_tokens=981, output_tokens=129, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': '3レベル'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…`

回答:

> AIE2026の宿題における「3レベル」とは、宿題の構成を示す以下の3段階のことです。
>
> 1. **基礎**：講義内容の確認
> 2. **実装**：自分でコードを書く
> 3. **発展**：調査や試行
>
> どれか1つのレベルに取り組めば、その回の宿題は完了となります。原則として採点は行われません。ご自身の理解度や目的に合わせて選んで取り組んでみてください。
>
> 関連する回：第1回

## `no-must-search` / AIE2026の講座の宿題にある「3レベル」とは何ですか？ / 2回目

- 応答時間: 2.3秒
- usage: RunUsage(cost=Decimal('0.0006018'), details={'text_prompt_tokens': 981}, input_text_tokens=981, input_tokens=981, output_tokens=123, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': '3レベル'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…`

回答:

> 「3レベル」とは、AIE2026の宿題の構成のことです。
>
> 宿題には以下の3段階（レベル）が用意されています。
>
> 1. **基礎**：講義内容の確認
> 2. **実装**：自分でコードを書く
> 3. **発展**：調査や試行
>
> どれか1つのレベルに取り組めば、その回の宿題は完了となります。なお、原則として宿題の採点は行われません。
>
> （第1回）

## `no-search-hint` / AIE2026の講座の宿題にある「3レベル」とは何ですか？ / 1回目

- 応答時間: 1.8秒
- usage: RunUsage(cost=Decimal('0.0006163'), details={'text_prompt_tokens': 921}, input_text_tokens=921, input_tokens=921, output_tokens=136, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': '3レベル'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…`

回答:

> AIE2026における「3レベル」とは、宿題の構成を示す言葉です。
>
> 宿題は以下の3段階（レベル）に分かれており、**どれか1つに取り組めばその回の宿題は完了**となります。自分の興味や理解度に合わせて選んで取り組むことができます。
>
> 1. **基礎**：講義内容の確認
> 2. **実装**：自分でコードを書く
> 3. **発展**：調査や試行
>
> ※ 原則として採点は行いません。
>
> 関係する回：第1回

## `no-search-hint` / AIE2026の講座の宿題にある「3レベル」とは何ですか？ / 2回目

- 応答時間: 2.1秒
- usage: RunUsage(cost=Decimal('0.0005663'), details={'text_prompt_tokens': 921}, input_text_tokens=921, input_tokens=921, output_tokens=116, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': '3レベル'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…`

回答:

> AIE2026の宿題における「3レベル」とは、宿題の構成のことで、以下の3段階に分かれています。
>
> 1. **基礎**：講義内容の確認
> 2. **実装**：自分でコードを書く
> 3. **発展**：調査や試行
>
> どれか1つに取り組めば、その回の宿題は完了となります。なお、原則として採点は行われません。
>
> （第1回）

## `base` / LoRAとQLoRAの違いは？ / 1回目

- 応答時間: 3.4秒
- usage: RunUsage(cost=Decimal('0.0009801'), details={'text_prompt_tokens': 1442}, input_text_tokens=1442, input_tokens=1442, output_tokens=219, requests=2, tool_calls=2)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`

回答:

> LoRAとQLoRAの主な違いは、**ベースモデルの重みの保持方法（量子化するかどうか）**にあります。
>
> * **LoRA（Low-Rank Adaptation）**
>   * 事前学習済みの重みはそのまま（通常は16ビットなどの精度）固定し、追加の小さな低ランク行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習パラメータやストレージ容量を大幅に削減できます。
> * **QLoRA（Quantized LoRA）**
>   * LoRAの仕組みをベースにしつつ、**ベースモデルの重みを4ビットなどに量子化**してメモリ消費を極限まで抑えたうえでLoRAの学習を行います。これにより、より大きなモデルを比較的小さなGPUでも効率よく学習できるようになります。
>
> （関連回：第2回）

## `base` / LoRAとQLoRAの違いは？ / 2回目

- 応答時間: 2.2秒
- usage: RunUsage(cost=Decimal('0.0009351'), details={'text_prompt_tokens': 1442}, input_text_tokens=1442, input_tokens=1442, output_tokens=201, requests=2, tool_calls=2)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`

回答:

> **LoRA**と**QLoRA**の主な違いは、ベースモデルの重みを量子化するかどうか、そして必要なGPUメモリの量にあります。
>
> * **LoRA（Low-Rank Adaptation）**
>   * 事前学習済みの重み（通常は16ビットなど）はそのまま固定し、追加の小さな低ランク行列（アダプタ）だけを学習して効率化を図る手法です。
> * **QLoRA（Quantized LoRA）**
>   * LoRAの仕組みをベースにしつつ、ベースモデルの重みを **4ビットなどに量子化** してメモリ消費を大幅に削る手法です。これにより、限られたGPUメモリでもさらに大きなモデルを学習できるようになります。
>
> （関連回：第2回）

## `no-must-search` / LoRAとQLoRAの違いは？ / 1回目

- 応答時間: 1.9秒
- usage: RunUsage(cost=Decimal('0.0009407'), details={'text_prompt_tokens': 1394}, input_text_tokens=1394, input_tokens=1394, output_tokens=209, requests=2, tool_calls=2)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`

回答:

> **LoRA**と**QLoRA**の主な違いは、ベースモデルの重みを量子化するかどうか、そして必要なメモリ量にあります。
>
> * **LoRA（Low-Rank Adaptation）**
>   * 事前学習済みの重みはそのまま（通常の精度で）固定し、追加の小さな低ランク行列（アダプタ）だけを学習して効率よくファインチューニングを行う手法です。
> * **QLoRA（Quantized LoRA）**
>   * LoRAの仕組みに加えて、ベースモデルの重みを4ビットなどに**量子化（圧縮）**してから固定します。これにより、LoRAよりもさらにVRAM（GPUメモリ）の消費量を大幅に抑えることができ、限られたハードウェアでもより大きなモデルを学習できるようになります。
>
> （第2回）

## `no-must-search` / LoRAとQLoRAの違いは？ / 2回目

- 応答時間: 2.0秒
- usage: RunUsage(cost=Decimal('0.0008582'), details={'text_prompt_tokens': 1394}, input_text_tokens=1394, input_tokens=1394, output_tokens=176, requests=2, tool_calls=2)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`

回答:

> LoRAとQLoRAの主な違いは、**ベースモデルの重みの量子化（ビット数の削減）を行うかどうか**です。
>
> * **LoRA**: 事前学習済みの重みは固定したまま（元のビット数のまま）、重みの更新分を表す小さな低ランク行列（アダプタ）だけを追加して学習する手法です。
> * **QLoRA**: ベースモデルの重みを4ビットなどに量子化（圧縮）してメモリ消費を大幅に抑えたうえで、LoRAによるファインチューニングを行う手法です。これにより、より小さなGPUでも大きなモデルを扱えるようになります。
>
> 関係する回：第2回

## `no-search-hint` / LoRAとQLoRAの違いは？ / 1回目

- 応答時間: 2.2秒
- usage: RunUsage(cost=Decimal('0.0009052'), details={'text_prompt_tokens': 1334}, input_text_tokens=1334, input_tokens=1334, output_tokens=202, requests=2, tool_calls=2)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`

回答:

> LoRAとQLoRAの違いは、ベースモデルの重みをそのまま使うか、量子化してメモリを節約するかにあります。
>
> - **LoRA**: 事前学習済みの重みは固定したまま、重みの更新分を2つの小さな低ランク行列で表し、その部分だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習パラメータや保存ファイルを大幅に削減できます。
> - **QLoRA**: LoRAの仕組みに加えて、ベースモデルの重みを4ビットなどに**量子化**（ビット数を減らして軽量化）してからLoRAを適用する手法です。これにより、さらにメモリ消費を抑え、より大きなモデルを小さなGPU環境でも動かせるようになります。
>
> （第2回）

## `no-search-hint` / LoRAとQLoRAの違いは？ / 2回目

- 応答時間: 1.8秒
- usage: RunUsage(cost=Decimal('0.0009077'), details={'text_prompt_tokens': 1334}, input_text_tokens=1334, input_tokens=1334, output_tokens=203, requests=2, tool_calls=2)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`

回答:

> **LoRA**と**QLoRA**の主な違いは、ベースモデルの重みをそのまま使うか、量子化してメモリを大幅に節約するかという点にあります。
>
> それぞれの定義は以下の通りです。
>
> * **LoRA**: 事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法です。学習するパラメータが少なく、学習結果も小さなファイルで保存できます。
> * **QLoRA**: ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法です。これにより、より大きなモデルを小さなGPUで扱うことが可能になります。
>
> （第2回）

## `many-terms` / LoRAとQLoRAの違いは？ / 1回目

- 応答時間: 2.6秒
- usage: RunUsage(cost=Decimal('0.0007736'), details={'text_prompt_tokens': 1137}, input_text_tokens=1137, input_tokens=1137, output_tokens=173, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`

回答:

> LoRAとQLoRAの主な違いは、**ベースモデルの重みをそのまま使うか、量子化して圧縮するか**にあります。
>
> * **LoRA（Low-Rank Adaptation）**
>   事前学習済みの重みを固定したまま、追加の小さな低ランク行列（アダプタ）だけを学習して効率的にファインチューニングを行う手法です。
> * **QLoRA（Quantized LoRA）**
>   ベースモデルの重みを4ビットなどに量子化（低精度化）してメモリ使用量を大幅に削減した状態で、LoRAによる学習を行う手法です。これにより、より大きなモデルをより少ないGPUメモリで効率よく学習できるようになります。
>
> 関係する回：第2回

## `many-terms` / LoRAとQLoRAの違いは？ / 2回目

- 応答時間: 2.2秒
- usage: RunUsage(cost=Decimal('0.0010186'), details={'text_prompt_tokens': 1137}, input_text_tokens=1137, input_tokens=1137, output_tokens=271, requests=2, tool_calls=1)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA QLoRA'})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`

回答:

> LoRA（Low-Rank Adaptation）とQLoRA（Quantized LoRA）は、どちらも大規模言語モデル（LLM）などを効率的にファインチューニング（追加学習）するためのPEFT（Parameter-Efficient Fine-Tuning）と呼ばれる手法ですが、大きな違いは**「ベースモデルの重みを量子化するかどうか」**にあります。
>
> ### LoRA
> - **仕組み**: 事前学習済みの重みを固定したまま、更新分となる少数のパラメータ（低ランクの小さな行列）だけを追加して学習します。
> - **特徴**: 学習するパラメータ数を大幅に減らせるため、メモリ消費を抑えながら効率よく学習できます。本講座では主にこちらの手法をベースに演習を行います。
>
> ### QLoRA
> - **仕組み**: LoRAの考え方に加え、**ベースモデルの重みを4ビットなどの低ビットに量子化（圧縮）**してから学習を行います。
> - **特徴**: 巨大なモデルであっても、必要なVRAM（GPUメモリ）をさらに劇的に削減できるため、より少ない計算資源（コンシューマー向けのGPUなど）で大きなモデルの学習が可能になります。
>
> ---
> 関連する回：第2回

## `quiz-at-end` / LoRAとQLoRAの違いは？ / 1回目

- 応答時間: 2.9秒
- usage: RunUsage(cost=Decimal('0.0013582'), details={'text_prompt_tokens': 2519}, input_text_tokens=2519, input_tokens=2519, output_tokens=241, requests=3, tool_calls=3)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
  - `make_quiz({'lecture': 2})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`
  - `make_quiz -> {"lecture": 2, "question": "「ランク（LoRAのr）」の意味は？", "answer": "LoRAで使う低ランク行列の大きさを決めるハイパーパラメータ。大きいほど表現力が上がるが、学習するパラメータとメモリも増…`

回答:

> 講座の用語集によると、LoRAとQLoRAの違いは以下のとおりです。
>
> * **LoRA**
>   事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータが少なく、学習結果（アダプタ）も小さいファイルで保存できます。
>
> * **QLoRA**
>   ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法です。より大きなモデルを小さなGPUで扱えるようにします。
>
> （これらはどちらも第2回で扱う内容です。）
>
> ---
>
> **【第2回の確認問題】**
> Q. 「ランク（LoRAのr）」とはどのようなハイパーパラメータですか？

## `quiz-at-end` / LoRAとQLoRAの違いは？ / 2回目

- 応答時間: 2.0秒
- usage: RunUsage(cost=Decimal('0.0011358'), details={'text_prompt_tokens': 1536}, input_text_tokens=1536, input_tokens=1536, output_tokens=270, requests=2, tool_calls=3)
- ツール呼び出し:
  - `search_glossary({'query': 'LoRA'})`
  - `search_glossary({'query': 'QLoRA'})`
  - `make_quiz({'lecture': 1})`
- ツールの戻り値（先頭120文字）:
  - `search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…`
  - `search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…`
  - `make_quiz -> {"lecture": 1, "question": "「プルリクエスト（PR）」の意味は？", "answer": "あるブランチの変更を別のブランチへ取り込むよう依頼する仕組み。差分の確認、コメント、自動テストの結果表示ができる。本講座…`

回答:

> LoRAとQLoRAの違いについて、講座の用語集を基に解説します。
>
> * **LoRA（Low-Rank Adaptation）**
>   事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータが少なく、学習結果（アダプタ）も小さいファイルで保存できます。
>
> * **QLoRA（Quantized LoRA）**
>   ベースモデルの重みを4ビットなどに**量子化**してメモリを節約したうえで、LoRAによるファインチューニングを行う手法です。LoRAの仕組みに量子化を組み合わせることで、より大きなモデルをより小さなGPUメモリで扱えるようにします。
>
> ---
>
> ### 第1回の確認問題
> 学習の定着度を確認するための問題です。ぜひ考えてみてください。
>
> **Q. 「プルリクエスト（PR）」の意味は何でしょうか？**

