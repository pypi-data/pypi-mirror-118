from typing import List

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.datasets import fetch_20newsgroups
from sklearn.pipeline import Pipeline
from vgram import VGramTokenizer, SplitLevel


class VGram:
    def __init__(self, size=10000, iter_num=10):
        self.tokenizer = VGramTokenizer(size, split_level=SplitLevel.LINE, verbose=True)
        self.iter_num = iter_num

    def fit(self, X: List[str], y: List = None, **kwargs):
        texts = [self.preprocess(text) for text in X]
        self.tokenizer.fit(texts)
        return self

    def transform(self, X: List, y: List = None, **kwargs):
        texts = [self.preprocess(text) for text in X]
        seqs = self.tokenizer.encode(texts)
        return [" ".join(str(id) for id in seq) for seq in seqs]

    @staticmethod
    def preprocess(text) -> str:
        res = ""
        for c in text.lower():
            if 'a' <= c <= 'z':
                res += c
        # text.lower().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        return res


def basic_cls():
    # fetch data
    train, test = fetch_20newsgroups(subset='train'), fetch_20newsgroups(subset='test')
    data = train.data + test.data

    # make vgram pipeline and fit it
    vgram = Pipeline([
        ("vgb", VGram(size=10000, iter_num=10)),
        ("vect", CountVectorizer())
    ])
    # it's ok, vgram fit only once
    # vgram.fit(data)

    # fit classifier and get score
    pipeline = Pipeline([
        ("vgram", VGram(size=10000, iter_num=10)),
        ("vect", CountVectorizer()),
        ('tfidf', TfidfTransformer(sublinear_tf=True)),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-4, max_iter=100, random_state=42))
    ])
    pipeline.fit(train.data, train.target)
    print("train accuracy: ", np.mean(pipeline.predict(train.data) == train.target))
    print("test accuracy: ", np.mean(pipeline.predict(test.data) == test.target))

    # show first ten elements of constructed vgram dictionary
    print("First 10 alphabet elements:", pipeline.named_steps["vgram"].tokenizer.get_vocab()[:10])


def main():
    basic_cls()


if __name__ == '__main__':
    main()

# original code
# train accuracy:  0.9926639561605091
# test accuracy:  0.8388210302708444
# other run
# train accuracy:  0.9927523422308644
# test accuracy:  0.8396176314391928
# ['f', 'ff', 'fforg', 'fforgpub', 'fferbertma', 'ffect', 'ffected', 'ffey', 'from', 'fromm',
#  'fromj', 'fromjmdcube', 'fromjakebony1bonycom', 'froma', 'fromk', 'fromc', 'fromthe', 'fromd', 'front', 'frontof']

# new impl
# train accuracy:  0.9916033233162453
# test accuracy:  0.8131970260223048

# preprocess texts = [text.lower().strip(' \n\r\t') for text in X]
# train accuracy:  0.9897472158387838
# test accuracy:  0.8158523632501328
# ['f', 'ff', 'ff ', 'ff dele', 'ffa', 'ffer', 'ffer ', 'ffer and', 'ff.', 'ffic ']

# text.lower().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
# train accuracy:  0.9812621530846739
# test accuracy:  0.8036378120021243
# First 10 alphabet elements: ['f', 'ff', 'ff.', 'ffer', 'ffering', 'ffered', 'ffect', 'ffectively', 'ffects', 'from']
