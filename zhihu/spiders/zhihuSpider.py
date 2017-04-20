# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.http import FormRequest
from scrapy.selector import Selector
class ZhihuspiderSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = ['http://www.zhihu.com/']

    headers = {
    	'Host':'www.zhihu.com',
    	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
    	'Accept':'*/*',
    	'X-Xsrftoken':'f7c8cb2c8e8bbcfba671f88a6279a2ae',
    	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    	'Accept-Encoding':'gzip, deflate, br',
    	'Referer':'http://www.oschina.net',
    	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    	'X-Requested-With':'XMLHttpRequest',
    	'Referer':'https://www.zhihu.com/',
    	'Connection':'keep-alive',
    	#'Content-Length':'95',
    	'Cookie':'aliyungf_tc=AQAAAKvXwBV3wAkAswF2dTT1/iEbb85r; q_c1=9f3fa6b3dff545ed92b22ac58e0a104b|1488884857000|1488884857000; _xsrf=f7c8cb2c8e8bbcfba671f88a6279a2ae; r_cap_id="YTQ3NmQ0NmFlMTg4NDZlZGFmYjNhZjZiNzdlMDQxZGU=|1488886684|277979f114fafc728df3cbd0d4e0eee7a25cf3da"; cap_id="OWJmOGM3MTAyYTkwNDI1NWIzMGNiZmUwY2RkMmIwNWE=|1488886684|76561fd1e29d1bba13a6bb48d82a46fdfe60bdc3"; d_c0="ABDCC6swaguPTg1uskn3EsjcR4yUm-Md-UQ=|1488884858"; nweb_qa=heifetz; __utma=51854390.1611718347.1488884861.1488884861.1488884861.1; __utmb=51854390.0.10.1488884861; __utmc=51854390; __utmz=51854390.1488884861.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100--|2=registration_date=20161014=1^3=entry_date=20161014=1; _zap=67aa0ebd-d4f2-4b94-a608-3cfec67db566; z_c0=Mi4wQUpEQXFfSkFzQW9BRU1JTHF6QnFDeGNBQUFCaEFsVk5xQ2ptV0FBenNIc3NqWmQwbFZoSmk5T1FwV3JPWTFWcmNB|1488886715|83b1e10048a595eb5ee052c4d4122a69167c0c64'
    	#'Upgrade-Insecure-Requests':'1'
    }

    def start_requests(self):

    	return [scrapy.Request(
    		"https://www.zhihu.com/#signin",
    		meta={'cookiejar':1},
    		callback = self.post_login
    		)]

    def post_login(self,response):
    	open('e:\hanhan\\zhihuq.txt', 'w+').write(response.body)

    	sel = Selector(response)
    	_xsrf = sel.xpath('//input[@name="_xsrf"]/@value').extract_first()
    	print _xsrf
    	logging.info('_xsrf:' + _xsrf)
    	return [scrapy.FormRequest.from_response(response,
    											url='https://www.zhihu.com/login/phone_num',
    											meta={'cookiejar':response.meta['cookiejar']},
    											headers=self.headers,
    											formdata={
    												'_xsrf':_xsrf,
    												'password':'guang1302',
    												'captcha_type':'cn',
    												'phone_num':'18310381978'
    											},
    											callback=self.after_login,
    											dont_filter=True
    											)]

    def after_login(self,response):
    	print 'after login ...'
    	print response.url 
    	open('e:\hanhan\\zhihu1.txt', 'w+').write(response.body)
    	#open('e:\hanhan\\zhihu.txt', 'w+').write(response.body)
    	for url in self.start_urls:

    		yield scrapy.Request(url,meta={'cookiejar':response.meta['cookiejar']},dont_filter=True,callback=self.parse_page)
    def parse_page(self,response):
    	print response.url
    	open('e:\hanhan\\zhihu.txt', 'w+').write(response.body)


    def _requests_to_follow(self, response):
        """重写加入cookiejar的更新"""
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = Request(url=link.url, callback=self._response_downloaded)
                # 下面这句是我重写的
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])
                yield rule.process_request(r)
