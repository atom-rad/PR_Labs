import requests
from bs4 import BeautifulSoup
import re
import os
import json

from homework import *

def scanPages(url: str, init_num: int, page_num: int, urls: [], max_num_pages=None):
    response = requests.get(url)
    if response.status_code == 200:
        url = re.sub(r'&page=\d+', '', url)

        if max_num_pages != None:
            if page_num == init_num + max_num_pages:
                return urls
        
        parser = BeautifulSoup(response.content, features='lxml')
        parser.prettify()

        advertisements = set()
        links = parser.findAll('a', href=True)
        nextPageUrl = findNextPage(url, links, page_num)

        if nextPageUrl == '':
            return urls
        
        for link in links:
            if re.match(r"/ro/[0-9]+", link['href']) and link['href'] not in advertisements:
                advertisements.add('https://999.md' + link['href'])

        urls.append(advertisements)
        page_num += 1

        scanPages(nextPageUrl, init_num, page_num, urls, max_num_pages)
        
    else:
        print(f"Request failed: {response.status_code}")


def findNextPage(url: str, links, page_num: int):
    for link in links:
        if f'page={page_num+1}' in link['href']:
            return f'{url}&page={page_num+1}'
    return ''


def main():
    site_url = 'https://999.md/ro/list/transport/cars?applied=1&aof=1&hide_duplicates=no&o_2029_593=18668&o_290_7=12900&o_4_151=24&r_6_2_unit=eur&ef=1%2C260%2C6%2C5%2C4%2C3%2C4112%2C2029%2C1279%2C1275&o_3_102=18&o_5_101=16&r_6_2_to=&o_1279_775=18592&o_260_1=776&o_1275_108=17&show_all_checked_childrens=no&r_6_2_from='
    list_of_urls = []
    
    p_n = 0
    i_n = 0
    if 'page' in site_url:
        p = re.split(r"&(page=[0-9]+)", site_url)[1]
        p_n = int(re.split(r"=", p)[1])
        i_n = p_n
    else:
        p_n = 1
        i_n = p_n
       
    scanPages(site_url, i_n, p_n, list_of_urls, max_num_pages=2)
    

    option = 'x'
    if os.path.exists('cars.json'):
        option = 'w'

    cars_json = {}
    list_of_cars = []
    for page_set in list_of_urls:
        for car_url in page_set:
            list_of_cars.append(scanAdvertisement(car_url))

    cars_json['cars'] = list_of_cars

    with open('cars.json', option) as car:
        car.write(json.dumps(cars_json, ensure_ascii=False, indent=4))
    
    '''
    option = 'x'
    if os.path.exists('links.txt'):
        option = 'w'

    with open('links.txt', option) as links:
        for url_set in list_of_urls:
            links.write(f'Page {i_n}\n')
            for url in url_set:
                links.write(url + '\n')
            links.write('\n\n\n')
            i_n += 1
    '''
            

if __name__ == '__main__':
    main()