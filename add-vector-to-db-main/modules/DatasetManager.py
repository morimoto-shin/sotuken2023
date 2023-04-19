"""
DBから取ってきたテキストデータから、Doc2Vecのトレーニング用データを作る。
"""

import re
import string
import unicodedata
import MeCab
import requests

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk


class DatasetManager:
    """
    言語を指定して初期化: ja, en
    """

    def __init__(self, lang):
        self.lang = lang

    def preprocess(self, text):
        """
        改行コードの削除、数字を0に置換、記号の削除
        日本語、英語
        """
        new = ' '.join(text.splitlines())  # 改行コードを空白で置換
        new = re.sub(r'[0-9]+', "0", new)  # 数字を0に置換
        new = unicodedata.normalize("NFKC", new).translate(
            str.maketrans("", "", string.punctuation + "「」、。・"))  # 記号の削除
        return new

    def get_tokens_ja(self, text):
        """
        分かち書きしたリストを返す
        日本語
        """
        mecab = MeCab.Tagger("-Ochasen")
        lines = mecab.parse(text).splitlines()
        words = []
        for line in lines:
            chunks = line.split('\t')
            if len(chunks) > 3 and (chunks[3].startswith('動詞')
                                    or chunks[3].startswith('形容詞')
                                    or (chunks[3].startswith('名詞')
                                        )):

                word = chunks[0]
                words.append(word)
        return words

    def get_stopwords_ja(self):
        """
        日本語のstopwordsの入手
        """
        url = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
        r = requests.get(url)
        tmp = r.text.split('\r\n')
        stopwords = []
        for a in tmp:
            if len(a) < 1:
                continue
            stopwords.append(a)
        return stopwords

    def delete_words_ja(self, words):
        # ひらがな1文字削除
        newWords = [w for w in words if re.compile('[\u3041-\u309F]').fullmatch(w) == None]
        # カタカナ1文字削除
        newWords = [w for w in newWords if re.compile('[\u30A1-\u30FF]').fullmatch(w) == None]
        # 特定の単語削除
        stopwords_ja = self.get_stopwords_ja()
        newWords = [w for w in newWords if not (w in stopwords_ja)]
        return newWords

    def get_tokens_en(self, text):
        # 文字列から空白文字（スペース、タブ、改行）を削除する
        text = text.strip()
        # 文字列を単語（英字、数字、アンダースコア）で分割する
        text_tokens = word_tokenize(text)
        # delete stopwords
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words('english')]
        # ステミング用のオブジェクトを作成する
        stemmer = PorterStemmer()
        # 分割された単語をステミングし、空文字列を除去する
        stemmed_tokens = [stemmer.stem(token) for token in tokens_without_sw if token != '']

        return stemmed_tokens

    def generate_dataset(self, text):
        if self.lang == 'ja':
            preprocess_text = self.preprocess(text)
            tokens = self.get_tokens_ja(preprocess_text)
            dataset = self.delete_words_ja(tokens)
        elif self.lang == 'en':
            preprocess_text = self.preprocess(text)
            dataset = self.get_tokens_en(preprocess_text)
        else:
            raise Exception('language option error')
        return dataset
