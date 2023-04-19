from modules.DatasetManager import DatasetManager
from modules.dbManager import DBManager
from gensim.models.doc2vec import Doc2Vec

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "shin"
DB_PASS = "postgres"
DB_NAME = "wiki_fa"

db_manager = DBManager(hostname=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
data_manager_en = DatasetManager('en')
data_manager_ja = DatasetManager('ja')
model_en = Doc2Vec.load("models/en_wikiFA_dv.model")
model_ja = Doc2Vec.load("models/ja_wikiFA_dv.model")


def main():
    table_name = 'articles'
    query = f"SELECT page_id, en_text, ja_text FROM {table_name} ORDER BY page_id ASC"
    pages = db_manager.select(query)
    for page in pages:
        if page[2] == '':  # 日本語テキストが空ならスキップ
            continue
        page_id = page[0]
        en_text = page[1]
        ja_text = page[2]

        # Doc2Vecの計算
        en_vec = model_en.infer_vector(data_manager_en.generate_dataset(en_text))
        en_vec = en_vec.tolist()
        ja_vec = model_ja.infer_vector(data_manager_ja.generate_dataset(ja_text))
        ja_vec = ja_vec.tolist()

        # ベクトルの格納
        query = f"UPDATE {table_name} SET en_docvec = ARRAY{en_vec}, ja_docvec = ARRAY{ja_vec} WHERE page_id = {page_id}"
        db_manager.execute(query)

        print(f"{table_name}:{page_id}")

if __name__ == "__main__":
    main()
