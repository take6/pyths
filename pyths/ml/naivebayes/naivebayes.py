# -*- coding: utf-8 -*-
import math
import pickle
import sys
# Yahoo! 形態素解析
from . import morphological


def getwords(doc):
    words = [s.lower() for s in morphological.split(doc)]
    return tuple(w for w in words)


class NaiveBayes(object):
    def __init__(self):
        self._machine = NaiveBayesCore()

    def train(self, dataframe):
        summary = dataframe['Summary']  # Summary column
        category = dataframe['Suspense']  # Suspense flag column
        for doc, cat in zip(summary, category):
            self._machine.train(doc, cat)

    def export_model(self, filename):
        self._machine.export_model(filename)

    def load_model(self, filename):
        self._machine.load_model(filename)


class NaiveBayesModel(object):
    @classmethod
    def load_model(cls, filename):
        with open(filename, 'rb') as f:
            name, attr = pickle.load(f)

        assert name == cls.__name__
        model = cls()
        for k, v in attr.items():
            setattr(model, k, v)

        return model

    def __init__(self):
        # 単語の集合
        self.vocabularies = set()

        # カテゴリ毎のword count
        self.wordcount = {}

        # カテゴリ毎の文章数
        self.catcount = {}

    def export_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(
                (self.__class__.__name__, self.__dict__),
                f
            )


class NaiveBayesCore(object):
    @property
    def vocabularies(self):
        return self._model.vocabularies

    @property
    def wordcount(self):
        return self._model.wordcount

    @property
    def catcount(self):
        return self._model.catcount

    def __init__(self):
        self._model = NaiveBayesModel()

    def export_model(self, filename):
        self._model.export_model(filename)

    def load_model(self, filename):
        return NaiveBayesModel.load_model(filename)

    def wordcountup(self, word, cat):
        catdict = self.wordcount.setdefault(cat, {})
        catdict.setdefault(word, 0)
        catdict[word] += 1
        self.vocabularies.add(word)

    def catcountup(self, cat):
        self.catcount.setdefault(cat, 0)
        self.catcount[cat] += 1

    def train(self, doc, cat):
        word = getwords(doc)
        print(word)
        for w in word:
            self.wordcountup(w, cat)
        self.catcountup(cat)

    def priorprob(self, cat):
        # P(cat) を求める
        return float(self.catcount[cat]) / sum(self.catcount.values())

    def incategory(self, word, cat):
        # カテゴリcatの中にwordが登場した回数を返す
        # return self.wordcount[cat].get(word, 0)
        if word in self.wordcount[cat]:
            return float(self.wordcount[cat][word])
        return 0.0

    def additive_smoothing(self, wordcount):
        # 加算スムージング
        return wordcount + 1

    def wordprob(self, word, cat):
        # P(word|cat) を求める
        # numerator = self.additive_smoothing(
        #     self.incategory(word, cat)
        # )
        # denominator = sum(self.wordcount[cat].values()) \
        #     + sum(map(self.additive_smoothing, [0 for _ in self.vocabularies]))
        # return numerator / denominator
        prob = \
            (self.incategory(word, cat) + 1.0) / \
            (sum(self.wordcount[cat].values()) +
                len(self.vocabularies) * 1.0)

        return prob

    def score(self, word, cat):
        # アンダーフローを避けるためにかけ算を対数の和で評価する
        score = math.log(self.priorprob(cat))
        # score += sum(map(
        #     lambda x: math.log(self.wordprob(x, cat)),
        #     word
        # ))
        for w in word:
            score += math.log(self.wordprob(w, cat))
        return score

    def classifier(self, doc):
        bestcat = None
        maxscore = - sys.maxsize
        word = getwords(doc)

        # カテゴリ毎に確率の対数を求める
        for cat in self.catcount.keys():
            prob = self.score(word, cat)
            print('{}: prob={}'.format(cat, prob))
            if prob > maxscore:
                maxscore = prob
                bestcat = cat

        return bestcat


# テストコード
# if __name__ == '__main__':
#     nb = NaiveBayes()

#     nb.train(
#         u'''Python（パイソン）は，オランダ人のグイド・ヴァンロッサムが開発したオープンソースのプログラミング言語。
# オブジェクト指向スクリプト言語の一種であり，Perlとともに欧米で広く普及している。イギリスのテレビ局 BBC が製作したコメディ番組『空飛ぶモンティパイソン』にちなんで名付けられた。
# Python は英語で爬虫類のニシキヘビの意味で，Python言語のマスコットやアイコンとして使われることがある。Pythonは汎用の高水準言語である。プログラマの生産性とコードの信頼性を重視して設計されており，核となるシンタックスおよびセマンティクスは必要最小限に抑えられている反面，利便性の高い大規模な標準ライブラリを備えている。
# Unicode による文字列操作をサポートしており，日本語処理も標準で可能である。多くのプラットフォームをサポートしており（動作するプラットフォーム），また，豊富なドキュメント，豊富なライブラリがあることから，産業界でも利用が増えつつある。''', 'Python'
#     )

#     nb.train(
#         u'''Ruby（ルビー）は，まつもとゆきひろ（通称Matz）により開発されたオブジェクト指向スクリプト言語であり，従来 Perlなどのスクリプト言語が用いられてきた領域でのオブジェクト指向プログラミングを実現する。Rubyは当初1993年2月24日に生まれ， 1995年12月にfj上で発表された。名称のRubyは，プログラミング言語Perlが6月の誕生石であるPearl（真珠）と同じ発音をすることから，まつもとの同僚の誕生石（7月）のルビーを取って名付けられた。''', 'Ruby'
#     )

#     nb.train(
#         u'''豊富な機械学習（きかいがくしゅう，Machine learning）とは，人工知能における研究課題の一つで，人間が自然に行っている学習能力と同様の機能をコンピュータで実現させるための技術・手法のことである。ある程度の数のサンプルデータ集合を対象に解析を行い，そのデータから有用な規則，ルール，知識表現，判断基準などを抽出する。データ集合を解析するため，統計学との関連も非常に深い。
# 機械学習は検索エンジン，医療診断，スパムメールの検出，金融市場の予測，DNA配列の分類，音声認識や文字認識などのパターン認識，ゲーム戦略，ロボット，など幅広い分野で用いられている。応用分野の特性に応じて学習手法も適切に選択する必要があり，様々な手法が提案されている。それらの手法は， Machine Learning や IEEE Transactions on Pattern Analysis and Machine Intelligence などの学術雑誌などで発表されることが多い。''', u'機械学習'
#     )

#     def print_result(nb, words):
#         print(u'{} => 推定カテゴリ: {}'.format(
#             words,
#             nb.classifier(words)
#         ))

#     # Python category
#     words = u'ヴァンロッサム氏によって開発されました'
#     print_result(nb, words)

#     words = u'豊富なドキュメントや豊富なライブラリがあります'
#     print_result(nb, words)

#     # Ruby category
#     words = u'純粋なオブジェクト指向言語です'
#     print_result(nb, words)

#     words = u'まつもとゆきひろ氏（通称Matz）により開発されました'
#     print_result(nb, words)

#     # 機械学習カテゴリ
#     words = u'「機械学習はじめよう」が始まりました'
#     print_result(nb, words)

#     words = u'検索エンジンや画像検索に利用されています'
#     print_result(nb, words)