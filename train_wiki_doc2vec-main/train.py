from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import joblib
import sys
import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def main(lang):
    if lang == 'en':
        f = open("dataset/dataset_en_1_23.pkl", "rb")
        dataset = joblib.load(f)  # データセットの読み込み
        trainings = [TaggedDocument(doc, [i]) for i, doc in enumerate(dataset)]
        model = Doc2Vec(documents=trainings, vector_size=100,
                        dm=True, epochs=30, window=15, min_count=1, workers=15)
        model.build_vocab(trainings)
        model.save('models/en_wikiFA_dv.model')
    elif lang == 'ja':
        f = open("dataset/dataset_ja_1_23.pkl", "rb")
        dataset = joblib.load(f)  # データセットの読み込み
        trainings = [TaggedDocument(doc, [i]) for i, doc in enumerate(dataset)]
        model = Doc2Vec(documents=trainings, vector_size=100,
                        dm=True, epochs=30, window=15, min_count=1, workers=15)
        model.build_vocab(trainings)
        model.save('models/ja_wikiFA_dv.model')
    else:
        raise Exception("Usage: python train.py [language]")


if __name__ == "__main__":
    main(sys.argv[1])
