import spacy


def analyze(content):
    nlp = spacy.load('ja_ginza')
    doc = nlp(content)

    for sent in doc.sents:
        for token in sent:
            info = [
                token.i,  # トークン番号
                token.text,  # テキスト
                token.lemma_,  # 基本形
                token.pos_,  # 品詞
                token.tag_,  # 品詞詳細
            ]
            if token.tag_.__contains__('人名'):
                print(info)

    for ent in doc.ents:
        if ent.label_.__eq__('Person'):
            print(
                ent.text + ',' +  # テキスト
                ent.label_ + ',' +  # ラベル
                str(ent.start_char) + ',' +  # 開始位置
                str(ent.end_char)  # 終了位置
            )


if __name__ == '__main__':
    analyze('恵比寿にあるあのイタリアンには太郎とよく行く。美味しいんだ。')
