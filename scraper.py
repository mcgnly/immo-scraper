from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("BASE_URL")

def get_subscribers():
  list_of_house_data = []
  html = requests.get(BASE_URL).content
  soup = BeautifulSoup(html, features="html.parser")

  # initial page, find the section containing the listings
  # do this first because we also need the init page to get the number of other pages
  whole_list = soup.find_all(attrs={'class': 'result-list__listing'})

  # append the relevant data to the list
  scrape_contents(whole_list, list_of_house_data)

  # figure out how many more pages to load
  string_of_pages = soup.find_all(attrs={'aria-label':'Seitenauswahl'})[0].find_all('option').pop().contents[0]
  number_of_pages = int(string_of_pages)

  for i in range(2, number_of_pages+1):
    # https://www.immobilienscout24.de/Suche/S-T/ is the first part
    front = BASE_URL[:43]
    # the part that loads the additional pages
    middle = f'P-{i}/'
    # ?enteredFrom=result_list removed form original URL
    end_index = len(BASE_URL) - 24
    end = BASE_URL[43:end_index]
    next_url = front + middle + end

    loop_html = requests.get(next_url).content
    loop_soup = BeautifulSoup(loop_html, features="html.parser")

    # inside each page, find the section containing the listings
    loop_whole_list = loop_soup.find_all(attrs={'class': 'result-list__listing'})

    # append the relevant data to the list
    scrape_contents(loop_whole_list, list_of_house_data)

  return list_of_house_data


def scrape_contents(w_l, list_of_data):
    
  for i in w_l:
    house_features = i.find_all('dd')
    price_string = house_features[0].contents[0]
    price = ''.join(price_string.split())[:-1].replace('.', '').replace(',', '.')

    m2_string = house_features[1].contents[0]
    m2 = ''.join(m2_string.split())[:-2].replace('.', '').replace(',', '.')

    house_data = {
      i['data-id']:{
        'price': price,
        'm2': m2,
        'ppm2': round(float(price)/float(m2), 2),
        'rooms': house_features[2].find(attrs={'class':'onlyLarge'}).contents[0] ,
      }
    }
    list_of_data.append(house_data)

new_apartment_data = get_subscribers()
data_txt = open('data.txt', 'r+')
first_char = data_txt.read(1)

# deal with empty file
if first_char:
  print(first_char)
  old_apartment_data = json.load(data_txt)
  combo_data = {**old_apartment_data, **new_apartment_data}
else:
  combo_data = new_apartment_data

json.dump(combo_data, data_txt)