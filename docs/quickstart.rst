===========
Quick Start
===========

Installation
============

Install the package with pip::

    $ pip install mit-news-tools

Usage
=====

Extracting news urls from the news homepage::

    import mitnewstools

    # first download the html of the article, for instance, with newspaper3k
    from newspaper import Article
    homepage_url = "https://www.nytimes.com/"
    art = Article(homepage_url)
    art.download()

    art_html = art.html

    # extracting news urls
    url_list = extract_urls(art.html, homepage_url)  # extracting all urls from the homepage
    news_url_list = filter_news_urls(url_list, homepage_url)  # extracting only news articles

Note that news_url_list will only contain articles from the New York Times.
(Similarly if the homepage_url is https://www.washingtonpost.com/, then news_url_list will only contain articles
from the Washington Post.)



Finding dates from a news article::

    import mitnewstools

    # first download the html of the article, for instance, with newspaper3k
    from newspaper import Article
    art_url = "https://www.nytimes.com/2020/08/11/us/politics/pompeo-state-inspector-general-saudi-weapons-civilian-casualties.html"
    art = Article(art_url)
    art.download()

    art_html = art.html


    date_published, date_modified = get_dates(art_html, art_url)



Removing accents or other non-ASCII characters in the article text::

    import mitnewstools

    # first download the text of the article, for instance, with newspaper3k
    from newspaper import Article
    art_url = "https://www.nytimes.com/2020/08/11/us/politics/pompeo-state-inspector-general-saudi-weapons-civilian-casualties.html"
    art = Article(art_url)
    art.download()

    art_text = art.text


    ascii_article = asciify(art_text)
