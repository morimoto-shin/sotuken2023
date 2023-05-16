import wikipediaapi
import requests
import itertools
from bs4 import BeautifulSoup
import csv
wiki_wiki = wikipediaapi.Wikipedia('ja')

def getHtmlElement(url: str):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  return soup

output = []

# first
url= "https://ja.wikipedia.org/wiki/Category:%E4%B8%BB%E9%A1%8C%E5%88%A5%E5%88%86%E9%A1%9E"
first_soup = getHtmlElement(url)
first_elms = first_soup.find_all('div', {'class': 'CategoryTreeItem'})
first_categories = []
for page_elms in first_elms:
  href = page_elms.find('a').get('href')
  title_elms = page_elms.find('span', {'class': 'CategoryTreeBullet'})
  title = str(title_elms).split('data-ct-title="')[1].split('"></span>')[0]
  obj = {
    'title': title,
    'href': href
  }
  first_categories.append(obj)
  
  output.extend([x.title for x in first_categories])

  for second in first_categories:
    second_url = f'https://ja.wikipedia.org/{second["href"]}'
    second_soup = getHtmlElement(second_url)
    second_categories_div = second_soup.find('div', id = 'mw-subcategories')
    second_pages_div = second_soup.find('div', id = 'mw-pages')
    second_categories_elms = second_categories_div.find_all('div', {'class': 'mw-category-group'})
    second_pages_elms = second_pages_div.find_all('div', {'class': 'mw-category-group'})
    second_categories = []
    second_pages = []

    for second_categories_elm, second_pages_elm in itertools.zip_longest(second_categories_elms, second_pages_elms, fillvalue = "<h3>*</h3>"):
      if "<h3>*</h3>" in str(second_categories_elm):
        second_pages_all_a = second_pages_elm.find_all('a')
        second_pages.extend(second_pages_all_a)
        continue
      if "<h3>*</h3>" in str(second_pages_elm):
        second_categories_all_a = second_categories_elm.find_all('a')
        second_categories.extend(second_categories_all_a)
        continue

      second_categories_all_a = second_categories_elm.find_all('a')
      second_categories.extend(second_categories_all_a)
      second_pages_all_a = second_pages_elm.find_all('a')
      second_pages.extend(second_pages_all_a)

    second_categories = [
      {
        "title": x.text,
        "href": x.get("href")
      } for x in second_categories]

    second_pages = [
      {
        "title": x.text,
        "href": x.get("href")
      } for x in second_pages]
    
    output.extend([x.title for x in second_pages])
    
    for third in second_categories:
      third_url = f'https://ja.wikipedia.org/{third["href"]}'
      third_soup = getHtmlElement(third_url)
      third_categories_div = third_soup.find('div', id = 'mw-subcategories')
      third_pages_div = third_soup.find('div', id = 'mw-pages')
      third_categories_elms = third_categories_div.find_all('div', {'class': 'mw-category-group'})
      third_pages_elms = third_pages_div.find_all('div', {'class': 'mw-category-group'})
      third_categories = []
      third_pages = []

      for third_categories_elm, third_pages_elm in itertools.zip_longest(third_categories_elms, third_pages_elms, fillvalue = "<h3>*</h3>"):
        if "<h3>*</h3>" in str(third_categories_elm):
          third_pages_all_a = third_pages_elm.find_all('a')
          third_pages.extend(third_pages_all_a)
          continue
        if "<h3>*</h3>" in str(third_pages_elm):
          third_categories_all_a = third_categories_elm.find_all('a')
          third_categories.extend(third_categories_all_a)
          continue

        third_categories_all_a = third_categories_elm.find_all('a')
        third_categories.extend(third_categories_all_a)
        third_pages_all_a = third_pages_elm.find_all('a')
        third_pages.extend(third_pages_all_a)

      third_categories = [
        {
          "title": x.text,
          "href": x.get("href")
        } for x in third_categories]

      third_pages = [
        {
          "title": x.text,
          "href": x.get("href")
        } for x in third_pages]
      
      output.extend([x.title for x in third_pages])


f = open('output.csv', 'w')
writer = csv.writer(f)
writer.writerow(output)
f.close()
