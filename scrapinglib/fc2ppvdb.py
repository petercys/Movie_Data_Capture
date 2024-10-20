# -*- coding: utf-8 -*-

import re
import json
import config
from lxml import etree
from .httprequest import request_session
from .parser import Parser

from bs4 import BeautifulSoup


class Fc2ppvdb(Parser):
    source = 'fc2ppvdb'

    expr_fc2_num = r"(?:FC|fc).*?(?:PPV|ppv)?[\-\_]?\s*([1-9][\d]{5,6})"

    def extraInit(self):
        self.imagecut = 4
        self.uncensored = True

    def search(self, number: str):
        try:
            if re.search(self.expr_fc2_num, number.strip().upper()):
                self.number = re.search(self.expr_fc2_num, number.strip().upper()).group(1)
            else:
                self.number = number.lower().replace('fc2-ppv-', '').replace('fc2-', '')
            
            # self.cookies = {"age": "off"}
            self.detailurl = 'https://fc2ppvdb.com/articles/' + self.number
            print(self.detailurl)
            session = request_session(cookies=self.cookies, proxies=self.proxies, verify=self.verify)
            htmlcode = session.get(self.detailurl).text
            
            soup = BeautifulSoup(htmlcode, 'lxml')
            
            extracted_title_ele = soup.select_one('div.container h2 > a[href]')
            extracted_title_text = extracted_title_ele.text.strip() if extracted_title_ele else ''

            extracted_studio_ele = soup.select_one('div.container a[href*="writers/"]')
            extracted_studio_text = extracted_studio_ele.text.strip() if extracted_studio_ele else ''
            
            extracted_actors = []
            for actor in soup.select('div.container > div span a[href*="actresses/"]'):
                extracted_actors.append(actor.text.strip())

            extracted_release_date = ""
            extracted_release_year = ""
            re_release_date = re.search(r">\s*(\d{4}-\d{1,2}-\d{1,2})\s*</span", htmlcode)
            if re_release_date:
                extracted_release_date = re_release_date.group(1).strip()
                extracted_release_year = extracted_release_date[:4]

            extracted_tags = []
            for tag in soup.select('div.container > div span a[href*="tags/"]'):
                extracted_tags.append(tag.text.strip())
            
            extracted_cover_ele = soup.select_one('main div img[alt]')
            extracted_cover_text = ''
            try:
                extracted_cover_text = extracted_cover_ele['src'].strip() if extracted_cover_ele else ''
            except Exception as e:
                pass

            dic = {
                'number': 'FC2-' + self.number,
                'title': extracted_title_text,
                'studio': extracted_studio_text,
                'release': extracted_release_date,
                'year': extracted_release_year,
                'outline': '',
                'runtime': '',
                'director': extracted_studio_text,
                'actor': extracted_actors,
                'actor_photo': '',
                'cover': extracted_cover_text,
                'cover_small': '',
                'extrafanart': '',
                'trailer': '',
                'tag': extracted_tags,
                'label': '',
                'series': '',
                'userrating': '',
                'uservotes': '',
                'uncensored': True,
                'website': self.detailurl,
                'source': self.source,
                'imagecut': 1,
            }
            dic = self.extradict(dic)
        except Exception as e:
            if config.getInstance().debug():
                print(e)
            dic = {"title": ""}

        js = json.dumps(dic, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        
        return js
