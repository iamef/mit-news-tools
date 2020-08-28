import pandas as pd
import re

import datetime
import datefinder
from date_guesser import guess_date, Accuracy

# uncommented this because some newspapers like psychology today
# don't have the json format
def emily_datefind_html(article_html: str, url: str, map_file="datemap.csv"):  # rename to _html
    """
    Given the html and url of a news article,
    return the date published in isoformat or an empty string if date cannot be found
    """
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
    """
    Given the html of a news article,
    return a dictionary with keys that starts with date, if found, such as datePublished, dateModified, or dateCreated.
    The values of the dictionary should be in isoformat. If such keys are not found, it returns an empty dictionary.
    """
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
    """
    Given the html and the url of the url,
    return the publication date and the modification date in isoformat as a tuple.
    >>> # format is (date_published_iso, date_modified_iso)
    >>> ("2020-05-27T21:59:25+01:00", "2020-05-28T18:34:13+01:00")

    If either of the publication date or the modification date cannot be found, they will be a
    empty string in the tuple.
    For instance, here is the example if the modification date was not found
    >>> ("2020-05-27T21:59:25+01:00", "")

    How it works:
    1) Looks for date in a website's json.
    2) If date not found, look for date in url.
    3) If date still not found, look for date in html.
    4) Use media cloud's dateguesser.
    """
    # first try the json method
    datedict = emily_datefind_json(article_html)  # method name changed
    pubtime = datedict.get("datePublished", '')
    modtime = datedict.get("dateModified", "")

    print("Go JSON", datedict)  # add print statement

    # add html to try because some news sources like psychology today only has html way of scraping
    if pubtime == "":
        pubtime = emily_datefind_html(article_html, url)

        print("Go HTML", pubtime)  # add print statement

    # now, try to look at the url
    url_date = re.search(
        r"(19|20)\d{2}[/\-_]"  # year
        r"[0-1]?\d[/\-_]"  # month
        r"[0-3]?\d",  # day
        url)

    if url_date is not None:
        date_found = re.split(r"[/\-_]", url_date.group())
        year = int(date_found[0])
        month = int(date_found[1])
        day = int(date_found[2])
        pubtime = datetime.date(year, month, day).isoformat()

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