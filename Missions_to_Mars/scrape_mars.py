import datetime as dt
import time

import pandas as pd

from pprint import pprint

from splinter import Browser
from bs4 import BeautifulSoup as bs


def scrape():
    executable_path = {"executable_path": "C:\Program Files\chromedriver_win32\chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    data = {
        'news_title': mars_news(browser)[0],
        'news_paragraph': mars_news(browser)[1],
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': mars_hemis(browser),
        'last_modified': dt.datetime.now()
    }
    browser.quit()

    # pprint(data)
    # print(type(data))

    return data


def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[0].text

    p_results = soup.find_all('div', class_='article_teaser_body')
    news_p = p_results[0].text

    return news_title, news_p


def featured_image(browser):
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    res = soup.find("a", class_="showimg fancybox-thumbs")['href']
    featured_image_url = url + res

    return featured_image_url


def mars_facts():
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[1]
    # print(mars_facts)

    mars_facts.columns = ["Category", "Measurement"]

    return mars_facts.to_html()


def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    # print(soup.prettify())

    hemisphere_image_urls = []

    results = soup.find_all("div", class_="description")
    mars_dict = {}

    for result in results:
        link = result.find_all('a', class_='itemLink product-item')

        href = link[0]['href']

        url1 = "https://marshemispheres.com/" + href
        #     print(url1)

        browser.visit(url1)
        html = browser.html

        hemi_soup = bs(html, 'html.parser')

        title = hemi_soup.find('h2', class_='title').text
        #     print(title)
        img_url = hemi_soup.find('li').a.get('href')
        #     print(img_url)

        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)

        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":
    scrape()