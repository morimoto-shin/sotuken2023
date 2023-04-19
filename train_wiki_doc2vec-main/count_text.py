from modules.dbManager import DBManager

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_NAME = "wikipedia_featured_articles"


def main():
    """
    英語の記事に対して日本語の記事が空となることがあるので、
    全ての行、英語の記事、日本語の記事の数を全て数える。
    """
    db_manager = DBManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
    table_names = db_manager.fetch_tablenames()  # tablenameの取得

    row_count_ja = row_count_en = 0
    for table_taple in table_names:
        table_name = table_taple[0]
        # 日本語の記事の数を数える
        query = f"SELECT page_id FROM {table_name} WHERE ja_text != '';"  # 注意
        row_count_ja += len(db_manager.select(query))

        # 英語の記事の数（DBの行の総数）を調べる
        query = f"SELECT page_id FROM {table_name} WHERE en_text != '';"
        row_count_en += len(db_manager.select(query))
    db_manager.close()

    print(f"ja_text_count / en_text_count = {row_count_ja} / {row_count_en}")


if __name__ == "__main__":
    main()
