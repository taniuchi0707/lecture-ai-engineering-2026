# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'search_phrase': 'Amazon S3 versioning overview', 'topics': ['general']})
- 気づき・疑問：STEP 3 では、fetch のあとに頼んでいない glossary_search_glossary({'query': 'MCP'}) も呼ばれた（指示文の「用語は先に用語集を確認する」に従ったため。モデル応答 3 回・入力 10,670 tokens に増えた）。fetch は取得の前に robots.txt を読み、/ からの 307 のリダイレクトを追ってドキュメントの .md を取っていた。STEP 4 は質問を英語の検索語（Amazon S3 versioning overview）に直してから aws の検索を呼んでいた。ツールが 8 個に増えても、質問に合うツールが選ばれた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：実装
- やったこと：
  - 第3回で作った `make_quiz` を、`app/mcp_server.py` に `server.tool()(tools.make_quiz)` の 1 行で公開した（エージェント側の `app/mcp_servers.json`・`app/mcp_agent.py` は変えていない）。
  - 範囲外の回（用語集に無い回）では、例外にせず「第N回の用語は用語集にないため、確認問題を作れません。用語がある回: …」と、用語がある回の一覧を添えたメッセージを `return` で返す（判定は `tools.make_quiz` の中）。
  - 範囲外のメッセージが MCP 経由でモデルに戻ることを確かめる試験 `test_make_quiz_out_of_range_message_reaches_model` を `tests/test_mcp_server.py` に足した（TestModel が int に 0 を入れて呼ぶので、第0回で確かめる）。
  - 比べるために、一時的に範囲外で `raise ValueError(...)` する版にして同じ質問をした（確かめたあと `return` の版に戻した）。
- 結果：
  - `--list-tools` に `[glossary_make_quiz]`（引数: `{"lecture": {"title": "Lecture", "type": "integer"}}`）が増えた。
  - 「第2回のクイズを作って」→ `[tool call] glossary_make_quiz({'lecture': 2})`、`[tool return]` に問題と答えの JSON。モデルは問題（「過学習」の意味は？）だけを出し、答えは伏せた。
  - 「第99回のクイズを作って」（`return` の版）→ `[tool call] glossary_make_quiz({'lecture': 99})`、`[tool return] glossary_make_quiz -> 第99回の用語は用語集にないため、確認問題を作れません。用語がある回: 第1回, 第2回, 第3回, 第4回, 第6回`。モデルは「第1回、第2回、第3回、第4回、第6回のいずれかを指定してください」と、使える回を挙げて答えた。
  - 同じ質問（`raise` の版）→ `[tool error] glossary_make_quiz -> Error executing tool make_quiz`。モデルは「第99回は用語集に存在しないようです」と推測で答え、使える回は示せなかった。
  - `uv run pytest -q` は 22 件すべて通った。
- 気づき・疑問：
  - `raise` で書いたメッセージは、MCP サーバーのログ（標準エラー）にはトレースバックごと出るが、モデルには「Error executing tool make_quiz」という中身のない文しか届かなかった。予期しない例外の中身は外に出さないという、サーバー側の作りのためだと思う。直し方をモデルに伝えたい入力の誤りは、`return`（またはクライアントに見せる専用のエラー）で返す必要がある。
  - 講義の「ツールのエラーは人にも分かりやすく」は、MCP では「どの経路で返すか」まで含めて考えないと、モデルに届かないことが分かった。わざと見せるための `ToolError` のような例外なら中身が届くのかは、まだ試していない。
