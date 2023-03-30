# tut url: https://www.datacamp.com/tutorial/wordcloud-python
# dataset url: https://www.kaggle.com/datasets/zynicide/wine-reviews

# start with loading all neccessary libraries
# basic libs
import MeCab
import collections
import numpy as np
import pandas as pd
from os import path

from io import BytesIO
# import Image
from PIL import Image
'''from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True'''

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# visualization
import matplotlib.pyplot as plt
# % matplotlib inline
# warning
import warnings
warnings.filterwarnings("ignore")

# for ja (Japanese) lang

# function


def transform_format(val):
    # if (isinstance(val, collections.Iterable)):
    if (hasattr(val, '__iter__')):
        # print("IMPORTANT: val =", val)
        # if val <= 0:
        # if val == 0:
        # if all(val == 0):
        if all(val == 0):   # OPT: <=
            # print(f"return = {255}")
            return 255
        else:
            '''print(f"return = {val}")
            return val'''
            # # print(f"return = {1}")
            # print(f'val = {val}')
            # print(f'val[0] = {val[0]}')
            # print(f'val[1] = {val[1]}')
            # print(f'val[2] = {val[2]}')
            # assert (len(val) == 4) & (val[0] == val[1] == val[2])
            # return 1  # OPT: val[0], 1, 125
            """assert len(val) == 4   # DEBUG
            return (val[0] + val[1] + val[2] + val[3] / 4)"""
            """out = (val[0] + val[1] + val[2] + val[3] / 4)
            print(f"out = {out}")
            return out"""
            # return 63.75
            return val[0]
    else:
        if val == 0:
            return 255
        else:
            return val


def transform_format2(val):
    # print("val =", val)

    for ele in val:
        print("BFR: ele =", ele)
        ele = transform_format(ele)
        print("AFR: ele =", ele)


def get_text():
    # load in the dataframe
    # without index_col=0 -> read in row name (index)
    df = pd.read_csv("data/winemag-data-139k-v2.csv", index_col=0)

    # start with one review
    text = df.description[0]
    # print("text =", text)   # DEBUG
    return text


def get_word_cloud_from_text(text=get_text(), lang="en", min_font_size=4, max_font_size=None, prefer_horizontal=0.9):
    # create stopword list:
    stopwordSet = set(STOPWORDS)   # maybe can set at outer level
    if lang == "en":
        stopwordSet.update(["drink", "now", "wine", "flavor", "flavors"])
    elif lang == "ja":
        stopwordSet.update(['てる', 'いる', 'なる', 'れる', 'する', 'ある', 'こと', 'これ', 'さん', 'して',   # OPT: stopwords.update()
                            'くれる', 'やる', 'くださる', 'そう', 'せる', 'した',  '思う',
                            'それ', 'ここ', 'ちゃん', 'くん', '', 'て', 'に', 'を', 'は', 'の', 'が', 'と', 'た', 'し', 'で',
                            'ない', 'も', 'な', 'い', 'か', 'ので', 'よう', '', 'れ', 'さ', 'なっ'])
    # print("stopwordSet =", stopwordSet)

    # format text for ja
    # if lang == "en":
    #     text = get_text()   # dummy data
    if lang == "ja":
        # text = get_wordlist()   # dummy data
        # text = mecab_analysis(text)
        # convert array into string # WITHOUT THIS WILL CAUSE: TypeError: expected string or bytes-like object
        text = " ".join(text)

    # get font_path for ja
    if lang == "en":
        fpath = None
    elif lang == "ja":
        fpath = "fonts/ヒラギノ丸ゴ ProN W4.ttc"

    ####################################################################################

    # # unwrap outer array layer # OPT: "", 'img/wine_mask.png', "wine_mask.png", '/Users/zrhun/Desktop/Coding/Word Cloud from Twitter/img/wine_mask.png'   # CAN'T WORK
    # # wine_mask = np.array(Image.open("img/wine_mask.png"))[0]   // MAYBE GOT PROBLEM
    # wine_mask = np.array(Image.open("img/wine_mask.png"))
    # print("wine_mask =", wine_mask)
    # '''wine_mask = "img/wine_mask.png"   # OPT: "wine_mask.png", "cup.png", "cup.png"
    # with Image.open(wine_mask) as wine_mask:
    #     # wine_mask
    #     print("wine_mask =", wine_mask)'''

    # # transform your mask into a new one that will work with the function
    # transformed_wine_mask = np.ndarray(
    #     (wine_mask.shape[0], wine_mask.shape[1]), np.int32)

    # for i in range(len(wine_mask)):
    #     transformed_wine_mask[i] = list(map(transform_format, wine_mask[i]))

    # # check the expected result of your mask
    # # print("transformed_wine_mask =", transformed_wine_mask)
    # print("transformed_wine_mask =")
    # print(transformed_wine_mask)

    ####################################################################################
    # OPT: seo.jpg, wine_mask.png, star.jpeg, star.png, star2.png
    # TODO: chg wine to star / -
    wine_mask = np.array(Image.open("img/star3.png"))
    # print(f"wine_mask = {wine_mask}")   # DEBUG

    # transform your mask into a new one that will work with the function
    transformed_wine_mask = np.ndarray(
        (wine_mask.shape[0], wine_mask.shape[1]), np.int32)
    # print(f"transformed_wine_mask = {transformed_wine_mask}")   # DEBUG

    for i in range(len(wine_mask)):
        transformed_wine_mask[i] = list(map(transform_format, wine_mask[i]))
    # print(f"transformed_wine_mask = {transformed_wine_mask}")   # DEBUG
    ####################################################################################

    # create a word cloud image
    """wc = WordCloud(background_color="white", max_words=1000, mask=transformed_wine_mask,
                stopwords=stopwords, contour_width=3, contour_color='firebrick')"""
    wc = WordCloud(background_color="white",
                   # max_words=1000,
                   mask=transformed_wine_mask,
                   stopwords=stopwordSet,
                   contour_width=3,
                   contour_color='firebrick',
                   # width=800, height=400,
                   width=3000,
                   height=2000,
                   random_state=1,
                   colormap='Set2',
                   collocations=False,
                   font_path=fpath,
                   min_font_size=min_font_size,
                   max_font_size=max_font_size,
                   prefer_horizontal=prefer_horizontal)

    # DEBUG START
    print(f'fpath = {fpath}')
    print(f'stopwordSet = {stopwordSet}')
    print(f'text = {text}')
    print(f'wc = {wc}')
    # DEBUG END

    # generate a wordcloud
    wc.generate(text)   # TODO: chk in docs
    return wc

# for ja (japanese) lang


def mecab_analysis(text):
    t = MeCab.Tagger("-Owakati")   # Ochasen
    t.parse('')
    node = t.parseToNode(text)
    output = []
    while node:
        if node.surface != "":
            word_type = node.feature.split(",")[0]
            if word_type in ["形容詞", "動詞", "名詞", "副詞"]:
                output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output


def get_wordlist():
    file = open("testing/wakati.txt")
    text = file.read()
    file.close()
    return mecab_analysis(text)


# testing output
"""wc = getWordCloud()
# show
plt.figure(
    # [20, 10],
    figsize=(10, 10),
    facecolor="k"
)
plt.axis("off")
plt.tight_layout(pad=0)
plt.imshow(wc, interpolation='bilinear')
plt.show()"""
