import sys
import os
import requests
from bs4 import BeautifulSoup
from collections import Counter
from requests.exceptions import HTTPError
from aiohttp import ClientSession
from user_agent import generate_user_agent
import random
import string
import re
import time
import socks
import socket
import json
import datetime


class parser:
    """doc"""

    def __init__(self,links):
        self.proxies_list = [{'http': 'http://' + i} for i in ['99.79.100.105:8080',
                                                               '64.20.74.24:45554', '62.37.237.101:8080',
                                                               '180.234.206.77:8080',
                                                               '78.11.85.13:8080', '109.188.81.101:8080',
                                                               '97.77.49.151:45554',
                                                               '139.59.17.113:8080', '191.179.147.46:11421',
                                                               '111.76.129.223:808',
                                                               '111.68.99.42:8080', '80.241.219.66:3128',
                                                               '189.16.249.114:8080',
                                                               '201.20.94.106:8080', '216.229.120.173:45554',
                                                               '116.58.247.31:3128', '103.9.115.142:3128',
                                                               '82.164.99.193:10200', '80.188.79.138:8080',
                                                               '36.75.113.224:8080', '1.20.204.163:8080',
                                                               '178.54.44.24:8080', '65.182.136.153:45554',
                                                               '203.142.81.205:8080', '42.202.35.185:8118',
                                                               '66.162.122.24:8080']]
        self.flagma_ads = {}
        self.waste_list_d_flagma = []
        socks.set_default_proxy(socks.SOCKS5,"localhost",9150)
        socket.socket = socks.socksocket
        self.flagma_parse_data_name = ""
        self.flagma_parse_log_name = "flagma_parse_" + str(datetime.datetime.now()).replace(' ', '_') + ".log"
        self.current_link = ""
        self.current_link_page = ""
        self.current_index_page = 0
        self.index_page_begin = 0
        self.links = links

    def generate_header_request(self):
        self.proxie = self.proxies_list[random.randint(0, 25)]
        token_ya = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        token_ya1 = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
        token_ys1 = ''.join(random.choice(string.digits) for _ in range(16))
        token_ys2 = ''.join(random.choice(string.digits) for _ in range(24))
        token_ys3 = ''.join(random.choice(string.digits) for _ in range(4))
        token_ys4 = ''.join(random.choice(string.digits) for _ in range(10))

        self.cookie = 'yandex_login=' + token_ya + '; ' \
                                                   'ys_fp=form-requestid%3D' + token_ys1 + '-' + token_ys2 + '-sas1-' + token_ys3 + '; ' \
                                                                                                                                    'yandex_gid=' + token_ys3 + '; ' \
                                                                                                                                                                'yandexuid=' + token_ys1 + '; yabs-frequency=/3/' + token_ya1 + '/; yp=' + token_ys4 + '.sp;'

    # парсинг страницы цайта flagma.ru с объявлениями
    def parce_list_ads_flagma(self, link):
        self.generate_header_request()
        waste_links_l = list()
        try:
            req = requests.get(link, headers={'User-Agent': generate_user_agent(), 'Cookie': self.cookie},
                               proxies=self.proxie)
            html = BeautifulSoup(req.text, "html.parser")
            html_tags = html.find_all('div', attrs={'class': ['page-list-item-info']})
            assert (len(html_tags) > 0), "web site flagma.ru was rewriten and this parser is not actual now"
            for i in html_tags:
                waste_links_l.append(i.find('a')["href"])
            return waste_links_l
        except requests.exceptions.ConnectionError:
            time.sleep(random.uniform(0.5, 1.0))
            self.index_page_begin = self.current_index_page
            self.links = self.links[self.links.index(link):len(self.links)]
            self.write_log("flagma", "error connection (run tor, please)")
            self.parce_flagma()


    # парсинг одного объявления c сайта flagma.ru
    def parse_ads_flagma(self, link):
        self.generate_header_request()
        ad_dict = {}
        try:
            req = requests.get(link, headers={'User-Agent': generate_user_agent(), 'Cookie': self.cookie},
                            proxies=self.proxie)
        except requests.exceptions.ConnectionError:
            time.sleep(random.uniform(0.5, 1.0))
            self.index_page_begin = self.current_index_page
            self.links = self.links[self.links.index(self.current_link):len(self.links)]
            self.write_log("flagma", "error connection (run tor, please)")
            self.parce_flagma()
            return {}
        self.write_log("flagma", self.current_IP())
        self.write_log("flagma", "processing ad: " + link)
        html = BeautifulSoup(req.text, "html.parser")
        if len(html) > 0:
            return {}
        html_tag = html.find('div', attrs={'id': ['main-center-left-wrapper']})  # тело всего объявления
        if len(html_tag) > 0:
            return {}
        try:
            img = html_tag.find('img')["src"]
            if img is not None:
                ad_dict['picture'] = img
        except TypeError:
            pass
        header = html_tag.find('div', attrs={'class': ['header-container']})  # заголовок объявления
        if header is not None:
            head = header.find('h1').contents[0]
            if head is not None:
                ad_dict['header'] = head

        description = html_tag.find('div', attrs={'id':['description-box']}) # описание объявления
        if description is not None:
            desc = description.find('p').contents[0]
            if desc is not None:
                ad_dict['description'] = desc

        offers = html_tag.find('div', attrs={'itemprop': ['offers']})  # ссодержимое объявления
        if offers is not None:
            price = offers.find('div', attrs={'id': ['price-v2']})
            if price is not None:
                tr = price.find_all('tr')  # таблица цен
            unit = ''
            if len(tr) > 0:
                for t in tr:  # пробегаем по строкам таблицы с ценами
                    tr_span = t.find('span').contents
                    unit = tr_span[-1]
                    opt = t.find(text='оптом')
                    price_min = price.find('span', attrs={'itemprop': ['minPrice']})
                    price_max = price.find('span', attrs={'itemprop': ['maxPrice']})
                    price_nom = price.find('span', attrs={'itemprop': ['price']})
                    price_currency = price.find('span', attrs={'itemprop': ['priceCurrency']})
                    if opt is not None:  # если указана оптовая цена, заполняем соответствующие поля
                        if price_min is not None:
                            ad_dict['price_min_opt'] = price_min.contents[0]
                        if price_max is not None:
                            ad_dict['price_max_opt'] = price_max.contents[0]
                        if price_nom is not None:
                            ad_dict['price_nom_opt'] = price_nom.contents[0]
                        if price_currency is not None:
                            str1 = ""
                            try:
                                str1 = price_currency.contents[0] + unit  # указание объема
                                ad_dict['price_volume_opt'] = str1
                            except TypeError:
                                pass
                    else:  # иначе указываем обычные цены
                        if price_min is not None:
                            ad_dict['price_min'] = price_min.contents[0]
                        if price_max is not None:
                            ad_dict['price_max'] = price_max.contents[0]
                        if price_nom is not None:
                            ad_dict['price_nom'] = price_nom.contents[0]
                        if price_currency is not None:
                            str1 = ""
                            try:
                                str1 = price_currency.contents[0] + unit
                                ad_dict['price_volume'] = str1
                            except TypeError:
                                pass

            company = offers.find('div', attrs={'id': ['company-link']})  # поле с указанием компании и города
            if company is not None:
                company1 = company.find('span', attrs={'itemprop': ['memberOf']})
                if company1 is not None:
                    ad_dict['company'] = company1.contents[0]  # название компании
                city = company.contents
                ad_dict['city'] = city[-1]  # последний элемент списка из поля - указание названия города
                name = html.find('div', attrs={'id': ['contacts']})  # поле с указанием фио представителя компании
                if name is not None:
                    name1 = name.find('span', attrs={'itemprop': ['name']})
                    if name1 is not None:
                        ad_dict['name'] = name1.contents[0]
                    try:
                        jobTitle = name.find('span', attrs={'itemprop': ['jobTitle']}).contents[0]
                        if jobTitle is not None:
                            ad_dict['jobTitle'] = jobTitle
                    except IndexError:
                        pass
        # else:
        #     offers = html_tag.find('dif', attrs={'class': ['company-infoblock']})  # содержимое объявления
        #     if offers is not None:

        return ad_dict

    def parce_flagma(self):
        waste_list = list()
        for link in self.links:
            self.current_link = link
            self.flagma_parse_data_name = "flagma_" + re.search(r"([\-A-Za-z0-9_]+)\-s", self.current_link).group(0).replace('-s', '') + ".json"
            self.generate_header_request()
            try:
                req = requests.get(link, headers={'User-Agent': generate_user_agent(), 'Cookie': self.cookie},
                                  proxies=self.proxie)
                html = BeautifulSoup(req.text, "html.parser")
                assert (len(html) > 0), "web site flagma.ru was rewriten and this parser is not actual now"
                html_tag = html.find('div', attrs={'id': ['paginator']})
                count_web_str = 0
                if html_tag is not None:
                    count_web_str = html.find('li', attrs={'class': ['page notactive']}).contents[0].contents[0]

                for i in range(self.index_page_begin, int(count_web_str)):
                    self.current_index_page = i
                    link1 = re.sub(r"\-([A-Za-z0-9_]+)\.", "-" + str(i) + ".", link)
                    self.write_log("flagma", "processing link with ads: " + link1)
                    waste_list = self.parce_list_ads_flagma(link1)
                    random.shuffle(waste_list)
                    for waste in waste_list:
                        time.sleep(random.uniform(0.5, 1.0))
                        waste_d = {}
                        waste_d = self.parse_ads_flagma(waste)
                        if waste_d is not None:
                            waste_d['link'] = waste
                            self.write_data("flagma", waste_d)
                            self.waste_list_d_flagma.append(waste_d)
                self.index_page_begin = 0
            except requests.exceptions.ConnectionError:
                time.sleep(random.uniform(0.5, 1.0))
                self.index_page_begin = self.current_index_page
                self.links = self.links[self.links.index(link):len(self.links)]
                self.write_log("flagma","error connection (run tor, please)")
                self.parce_flagma()


    def current_IP(self):
        ip = requests.get('http://checkip.dyndns.org').content
        soup = BeautifulSoup(ip, 'html.parser')
        return soup.find('body').text

    def write_log(self,web_site, string):
        if (web_site == "flagma"):
            with open(self.flagma_parse_log_name, 'a') as f:
                f.write(string)
                f.write(os.linesep)

    def write_data(self,web_site,data_d):
        if (web_site == "flagma"):
            with open(self.flagma_parse_data_name,'a') as f:
                json.dump(data_d, f)
                f.write(os.linesep)



if __name__ == '__main__':
    links = ["https://flagma.ru/s1/othody-pnd-so243064-179-1.html",
             "https://flagma.ru/s1/othody-pnd-so243064-170-1.html",
             "https://flagma.ru/s1/othody-pnd-so243064-140-1.html",
             "https://flagma.ru/s1/othody-pnd-so243064-238-1.html",
             "https://flagma.ru/s1/othody-pnd-so243064-63-1.html"]

    parse = parser(links)
    parse.parce_flagma()

    # link = "https://smolensk.flagma.ru/othody-prozrachnyh-pnd-pvd-stretch-plyonki-pod-o4172673.html"
    # waste_d = parse.parse_ads_flagma(link)
    # waste_d['link'] = link

    # filename = "flagma_othody-pnd-trub.json"
    # files = ["flagma_parse_data2019-05-06_20:30:06.076071.json",
    #          "flagma_parse_data2019-05-06_21:26:25.704135.json",
    #          "flagma_parse_data2019-05-06_22:28:16.229994.json",
    #          "flagma_parse_data2019-05-06_22:38:36.746754.json"]
    # content = []
    # for f in files:
    #     with open(f, 'r') as file:
    #         content = file.readlines()
    #     with open(filename, 'a') as f:
    #             f.writelines(content)
