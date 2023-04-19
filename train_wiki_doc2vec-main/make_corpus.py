from modules.DatasetManager import DatasetManager
from modules.dbManager import DBManager
import gc
import joblib
import os

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "wikipedia_featured_articles"

db_manager = DBManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)


def main():
    """
    DBからテキストの読み込みを行う
    """
    # os.mkdir("dataset")
    # english
    text_list_en = get_FAtext('en')
    data_maker_en = DatasetManager('en')
    dataset_en = list(map(data_maker_en.generate_dataset, text_list_en))
    print(f"英語記事の総数：{len(dataset_en)}")
    with open('dataset/dataset_en.pkl', 'wb') as f:
        joblib.dump(dataset_en, f)
    # メモリの解放
    del dataset_en
    del text_list_en
    gc.collect()

    # japanese
    # text_list_ja = get_FAtext('ja')
    # data_maker_ja = DatasetManager('ja')
    # dataset_ja = list(map(data_maker_ja.generate_dataset, text_list_ja))
    # print(f"日本語記事の総数：{len(dataset_ja)}")
    # with open('dataset/dataset_ja.pkl', 'wb') as f:
    #     joblib.dump(dataset_ja, f)


def get_FAtext(lang):
    table_names = fetch_tablenames()
    text_list = []
    for table_name in table_names:
        if lang == 'en':
            # 変更点
            query = f"SELECT en_text FROM {table_name} WHERE ja_text != '' ORDER BY page_id ASC"
            text_taple = db_manager.select(query)
        elif lang == 'ja':
            # 変更点
            query = f"SELECT ja_text FROM {table_name} WHERE ja_text != '' ORDER BY page_id ASC"
            text_taple = db_manager.select(query)
        else:
            raise Exception('language option error')

        for text in text_taple:
            text = text[0]
            text_list.append(text)
    return text_list


def fetch_tablenames():
    table_names = db_manager.fetch_tablenames()
    table_names = [table_name[0] for table_name in table_names]
    table_names.sort()  # 辞書順にソート
    return table_names


if __name__ == "__main__":
    main()
