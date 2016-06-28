# -*- coding: utf-8 -*-

import logging
import re
import requests
import time

from bs4 import BeautifulSoup

from exception.burgerking import BurgerKingException

class NextRequestPayload():
    def __init__(self, response):
        logging.error(response.text)
        self.payload = dict()
        self.c_num_re = re.compile('(\?|;)c=(?P<c_num>\d+)')
        self.soup = BeautifulSoup(response.text, 'html.parser')
        self.c_num = self._get_c_num(response.text)
        self.payload = self._get_payload(response.text)

    def _get_c_num(self, response_text):
        try:
            return self.c_num_re.search(response_text).group('c_num')
        except:
            raise BurgerKingException('fail to find c_num')
    
    def _get_payload(self, response_text):
        self._fill_ionf_payload()
        self._fill_posted_fns_payload()
        self._fill_radio_payload()
        self._fill_textarea_payload()
        self._fill_checkbox_payload()
        
        logging.error(self.payload)

        return self.payload

    def _fill_ionf_payload(self):
        ionf_input = self.soup.find('input', {'name': 'IoNF'})
        if ionf_input:
            self.payload['IoNF'] = int(ionf_input.get('value'))
        
    def _fill_posted_fns_payload(self):
        posted_fns = self.soup.find('input', {'name': 'PostedFNS'})
        if posted_fns:
            self.payload['PostedFNS'] = posted_fns.get('value')

    def _fill_radio_payload(self):
        radio_value_dict = dict()
        for input in self.soup.find_all('input', {'type':'radio'}):
            current_value = radio_value_dict.get(input.get('name'))
            if current_value:
                new_value = int(input.get('value'))
                if current_value < new_value:
                    radio_value_dict[input.get('name')] = new_value
            else:
                radio_value_dict[input.get('name')] = int(input.get('value'))

        for radio_name, highest_value in radio_value_dict.iteritems():
            self.payload[radio_name] = highest_value

    def _fill_textarea_payload(self):
        textarea_value_dict = dict()
        for textarea in self.soup.find_all('textarea'):
            textarea_value_dict[textarea.get('name')] = ''
        
        for textarea_name, value in textarea_value_dict.iteritems():
            self.payload[textarea_name] = value
        
    def _fill_checkbox_payload(self):
        latest_checkbox_name = None
        latest_checkbox_value = None
        for checkbox in self.soup.find_all('input', {'type': 'checkbox'}):
            latest_checkbox_name = checkbox.get('name')
            latest_checkbox_value = checkbox.get('value')
        
        if latest_checkbox_name:
            self.payload[latest_checkbox_name] = latest_checkbox_value

    def __repr__(self):
        return '<NextRequestPayload c_num:{}, payload:{}>'.format(self.c_num, self.payload)

class BurgerKingCouponGenerator():
    HTTP_PREFIX = 'http://kor.tellburgerking.com'
    HTTPS_PREFIX = 'https://kor.tellburgerking.com'
    INDEX_PAGE_URL = HTTP_PREFIX    
    COOKIE_ENABLE_PAGE_URL_FORMAT = HTTPS_PREFIX + '/Index.aspx?c={}'
    INPUT_RECEIPT_NUM_PAGE_URL_FORMAT = HTTPS_PREFIX + '/Survey.aspx?c={}'
    SURVEY_URI_FORMAT = HTTPS_PREFIX + '/Survey.aspx?c={}'
    END_SURVEY_URI_FORMAT = HTTPS_PREFIX + '/Finish.aspx?c={}'
    FINISH_INDICATOR = 'PostFinish.aspx'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
                'host': 'kor.tellburgerking.com',
                'origin': self.HTTPS_PREFIX,
                'referer': self.HTTPS_PREFIX,
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
                })
        self.coupon_re = re.compile('(?P<coupon_num>\d{8})</p>')
        
    def generate(self, receipt_num):
        self._check_valid_receipt_num(receipt_num)
        nrp = NextRequestPayload(self._index_page())
        nrp = NextRequestPayload(self._cookie_enable_page(nrp))
        response = self._input_receipt_num_page(receipt_num, nrp)
        for i in range(30):
            nrp = NextRequestPayload(response)
            if self._is_finished(response):
                break
            response = self._survey_page(nrp)
        coupon_num = self._end_survey_page(nrp)
        return coupon_num
    
    # 마지막 get request
    # 여기서 버거킹 할인번호 추출
    def _end_survey_page(self, nrp):
        r = self.session.get(self.END_SURVEY_URI_FORMAT.format(nrp.c_num))
        self._check_exception(r, 'exception in end survey page')
        return self._get_coupon_num(r.text)

    def _survey_page(self, nrp):
        r = self.session.get(self.SURVEY_URI_FORMAT.format(nrp.c_num), data=nrp.payload)
        self._check_exception(r, 'exception in where page')
        return r

    def _input_receipt_num_page(self, receipt_num, nrp):
        payload = dict(
            JavaScriptEnabled = 1,
            FIP = True,
            CN1 = receipt_num[0:3],
            CN2 = receipt_num[3:6],
            CN3 = receipt_num[6:9],
            CN4 = receipt_num[9:12],
            CN5 = receipt_num[12:15],
            CN6 = receipt_num[15:16],
            NextButton = '시작',
            )
        r = self.session.get(self.INPUT_RECEIPT_NUM_PAGE_URL_FORMAT.format(nrp.c_num), data=payload)
        self._check_exception(r, 'exception in input receipt num page')
        return r

    def _cookie_enable_page(self, nrp):
        payload = dict(
            JavaScriptEnabled = 1,
            FIP = 'True',
            AcceptCookies = 'Y',
            NextButton = '계속'
            )
        r = self.session.get(self.COOKIE_ENABLE_PAGE_URL_FORMAT.format(nrp.c_num), data=payload)
        self._check_exception(r, 'exception in cookie enable page')
        return r

    def _index_page(self):
        r = self.session.get(self.INDEX_PAGE_URL)
        self._check_exception(r, 'exception in index page')
        return r

    def _get_coupon_num(self , response_text):
        print response_text
        try:
            return self.coupon_re.search(response_text).group('coupon_num')
        except:
            raise BurgerKingException('fail to find coupon num')

    def _is_finished(self, response):
        return self.FINISH_INDICATOR in response.text

    def _check_exception(self, response, msg):
        if not response.status_code == 200:
            raise BurgerKingException(msg)

    def _check_valid_receipt_num(self, receipt_num):
        RECEIPT_NUM_LENGTH = 16
        if not receipt_num.isdigit():
            raise BurgerKingException('receipt num is not a number')
        if not len(receipt_num) == RECEIPT_NUM_LENGTH:
            raise BurgerKingException('receipt num length not match')
            
