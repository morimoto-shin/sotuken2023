# add-vector-to-db
[wikipedia-Data_to_DB](https://github.com/satabie/wikipedia-Data_to_DB)および
[train_wiki_doc2vec](https://github.com/satabie/train_wiki_doc2vec)
の続き

en_docvecカラムおよびja_docvecカラムが空になっているので、ここに対応するテキストの文書ベクトルを求めて格納する。

# Requirements
Python:3.10.0

各自仮想環境を作り、以下を実行する。
```bash
$ pip install -r requirements.txt
```
# Usage
[train_wiki_doc2vec](https://github.com/satabie/train_wiki_doc2vec)で作成した英語、日本語のdoc2vecモデルをmodelsディレクトリ配下に置く。
全体のディレクトリ構造は次のようになる。
```
.
├── README.md
├── add-vector.py
├── models
│   ├── en_wikiFA_dv.model
│   └── ja_wikiFA_dv.model
├── modules
│   ├── DatasetManager.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── DatasetManager.cpython-310.pyc
│   │   ├── __init__.cpython-310.pyc
│   │   ├── dbManager.cpython-310.pyc
│   │   └── manage_dataset.cpython-310.pyc
│   └── dbManager.py
└── requirements.txt
```

add-vector.pyを実行する
```bash
$ python add-vector.py
```

# Result
![スクリーンショット_20221210_203435](https://user-images.githubusercontent.com/74339912/206854949-0a6a0dfe-40b7-427f-8024-35c45af910eb.png)

