import pandas as pd
import re

import datetime
import datefinder
from date_guesser import guess_date, Accuracy

# added this code because it was missing and there were bugs
def find_html_in_between(articlehtml: str, keyhtml: str):
    if keyhtml not in articlehtml:
        return None

    startindex = articlehtml.index(keyhtml)
    dateindex = 0

    numopen = 1
    endindex = -1

    for i in range(startindex + len(keyhtml) - 1, min(startindex + 1000, len(articlehtml))):
        if dateindex == 0 and articlehtml[i] == '>':
            dateindex = i + 1

        if articlehtml[i] == '<' and i + 1 < len(articlehtml):
            # print('numopen ' + str(numopen))
            # print('art i+1: ' + articlehtml[i + 1])
            if articlehtml[i + 1] == '/':
                numopen -= 1
            else:
                numopen += 1

        if numopen == 0:
            endindex = i
            break

    return articlehtml[dateindex: endindex]


# uncommented this because some newspapers like psychology today
# don't have the json format
def emily_datefind_html(article_html: str, url: str, map_file="datemap.csv"):  # rename to _html
    datemap = pd.read_csv(map_file, index_col=0)

    html_pattern = datemap['htmlparent'][datemap['domain'].apply(lambda domain: domain in url)]

    if html_pattern.size == 1:
        html_pattern = html_pattern.iloc[0]
        dateraw = find_html_in_between(article_html, html_pattern)
        # print(dateraw, newscuesdf[newssource][0])  for debugging purposes
        try:
            dateparsed = next(datefinder.find_dates(dateraw))
            return dateparsed.isoformat()
        except:
            return ""

    return ""  # add this so that it is guaranteed to return something


# Returns a dictionary in the form
# {'datePublished': '2020-06-29T18:51:27-04:00', 'dateModified': '2020-06-29T19:52:56-04:00'}
def emily_datefind_json(article_html):  # rename to _json
    retval = re.findall(r"[\"\']date\w+[\"\']:\s*[\"\'][\w\-:\.\+]+[\"\']", article_html)
    if len(retval) == 0:
        return {}
    # format so items compatible with pandas DataFrame:
    retval = list(map(lambda s: re.split(r'[\"\'\s]+', s)[1::2], retval))
    retval = pd.DataFrame(retval)
    retval = retval.sort_values(1).drop_duplicates(0).set_index(
        0)  # sort by dates in old-new order and keep oldest dates
    retval = retval.to_dict()[1]
    return retval


def get_dates(article_html, url):
    # first try the json method
    datedict = emily_datefind_json(article_html)  # method name changed
    pubtime = datedict.get("datePublished", '')
    modtime = datedict.get("dateModified", "")

    print("Go JSON", datedict)  # add print statement

    # add html to try because some news sources like psychology today only has html way of scraping
    if pubtime == "":
        pubtime = emily_datefind_html(article_html)

        print("Go HTML", pubtime)  # add print statement

    # add date-guesser
    if pubtime == "":
        guess = guess_date(url=arts.iloc[i, 0], html=article.html)
        if guess.accuracy == Accuracy.DATE or guess.accuracy == Accuracy.DATETIME:
            pubtime = guess.date.isoformat()
            # print(guess.date.isoformat()[:19], guess.method)
            print("Go dateguesser", pubtime, guess.method)
        elif guess.accuracy == Accuracy.PARTIAL:
            pubtime = guess.date.isoformat()[:7]
            print("Go dateguesser", pubtime, guess.method)
            # print(guess.accuracy, guess.method, guess.date.isoformat()[:7])
        # else:
        # print(guess.accuracy, guess.method, guess.date)

    return pubtime, modtime

if __name__ == "__main__":
    url = "https://www.psychologytoday.com/us/blog/understanding-nootropics/202008/how-nootropics-boost-mental-clarity-and-focus"
    # import requests
    # page = requests.get(url)
    # emily_datefind_html(page.text, url)

    from newspaper import Article
    art = Article(url)
    art.download()
    print(emily_datefind_html(art.html, url))