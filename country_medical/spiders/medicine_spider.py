# -*- coding: utf-8 -*-
from scrapy.http.request import Request
from fake_useragent import UserAgent
from scrapy.selector import Selector
from country_medical.items import CountryMedicalInsuranceItem
from scrapy_redis.spiders import RedisSpider
from country_medical.util.fileUtil import writeFile
from scrapy_splash.request import SplashRequest
ua = UserAgent()
import os

class MedicineSpider(RedisSpider):
    name = 'medicine_spider'
    allowed_domains = ['http://app1.sfda.gov.cn/']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604&curstart={}'
    start_urls = []
    for i in range(1, 2001):start_urls.append(url_pattern.format(i))#11111


    def parse(self, response):

       html = response.text
       select = Selector(text=html)
       url = response.url
       # if url.startswith("http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp"):
       a_el_list = select.xpath("/html/body/table[2]/tbody/tr/td/p/a/@href").extract()
       if a_el_list is None or len(a_el_list) == 0:
           writeFile(url=url,fileName="E:\spilder\country_medical\country_medical\exception-file\exception.txt")
       else:
           for a_el in a_el_list:
              u = "http://app1.sfda.gov.cn/datasearchcnda/face3/"+a_el.split(",")[1].replace("'", "")
              self.log("detail_url------------->>>{}".format(u))
              yield SplashRequest(url=u,callback=self.parse_item, dont_filter=True, args={"images": 0, 'timeout': 10, "wait": "5"})
       # else:
       #  self.parse_item(response)

    def start_requests(self):
        for url in self.start_urls: yield SplashRequest(url=url, dont_filter=True, args={"images": 0, 'timeout': 10, "wait": "5"})

    def parse_item(self, response):
        select = Selector(text=response.body.decode("utf-8"))
        texts = select.css("div>div>table:nth-child(1)>tbody>tr>td:nth-child(2)")
        textArr = []
        for k, p in enumerate(texts):
            if k > 12: break
            text = p._root.text
            textArr.append(text if text is not None else "")

        item = CountryMedicalInsuranceItem()
        item["info"] = textArr
        item["url"] = response.url
        yield item
