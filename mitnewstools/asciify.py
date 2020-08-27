"""
purpose:
    Get rid of all nonascii characters in the text, title, and author names
usage:
    python asciify.py [input files or folders] [1 output folder]

author: emilyfan
last edited: 7/1
"""
import os
from confusables import normalize
import pandas as pd
import sys


def faster_normalize(text: str):
    retstr = ""

    numconvchar = 0
    numfailedchar = 0

    for char in text:
        if not char.isascii():
            newchar = normalize(char, prioritize_alpha=True)[0]

            # attempts to make newchar ascii
            if not newchar.isascii():
                if newchar == '—':
                    newchar = '--'
                    # print("YAY: " + char + " -> "+ newchar)
                else:
                    for posschar in normalize(char):
                        # print(char)
                        if posschar.isascii():
                            newchar = posschar
                            # print("YAY: " + char + " -> "+ newchar)
                            break

            if not newchar.isascii():
                # print("RIP this char cannot be processed: " + char + " -> "+ newchar)

                # print(char.encode('raw_unicode_escape'))
                # print(newchar.encode('raw_unicode_escape'))

                newchar = " "

                numfailedchar+=1

            else:
                numconvchar+=1
            # elif newchar not in ["'", '"', "...", '-']:
            # print("YAY: " + char + " -> "+ newchar)
            retstr += newchar
        else:
            retstr += char

    # print(str(numconvchar) + ' characters conversted to ASCII | ' + str(numfailedchar) + " failed")

    return retstr


def clean_through_folder(input_folder: str, output_folder: str):
    """
    Make sure input_folder and output have the slash
    """
    # labels = ['URL','time', 'author', 'title', 'keywords', 'ML-summary', 'text', "col8", 'col9']
    if input_folder[-1] != '/':
        input_folder+='/'

    for newsfile in os.listdir(input_folder):
        if "articles_" in newsfile:
            print(newsfile)
            clean_file(input_folder + newsfile, output_folder)


def clean_file(filepath: str, output_folder: str):
    if output_folder[-1] != '/':
        output_folder+='/'

    filename = filepath.split(sep='/')[-1]

    labels = ['URL', 'time', 'author', 'title', 'keywords', 'ML-summary', 'text', "imageurl", 'timescraped']

    articlesdf = pd.read_csv(filepath, sep='\t', header=None)
    articlesdf.set_axis(labels[:len(articlesdf.columns)], axis='columns', inplace=True)
    articlesdf['text'] = articlesdf['text'].map(faster_normalize, na_action='ignore')
    articlesdf['title'] = articlesdf['title'].map(faster_normalize, na_action='ignore')
    articlesdf['author'] = articlesdf['title'].map(faster_normalize, na_action='ignore')

    articlesdf.to_csv(output_folder + filename, sep='\t', index=False, header=False)


filenames = sys.argv[1:-1]
outfolder = sys.argv[-1]


for f in filenames:
    if os.path.isdir(f):
        clean_through_folder(f, outfolder)
    else:
        clean_file(f, outfolder)