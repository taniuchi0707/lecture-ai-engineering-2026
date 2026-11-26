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

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
