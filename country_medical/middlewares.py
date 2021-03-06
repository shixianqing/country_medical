# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class CountryMedicalInsuranceSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

import country_medical.util.fileUtil as fileUtil
class CountryMedicalInsuranceDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):

        if response is not None and response.status is not None and response.status != 200:
            spider.log(message="url------->>{}请求出问题".format(response.url))
            fileUtil.writeFile(response.url,"D:\workspace\country_medical\country_medical\exception-file\exception.txt")

        print("进入自定义中间件中了")
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        url = request.meta["splash"]["args"]["url"]
        spider.log(message="url------->>{}响应异常".format(url))
        fileUtil.writeFile(url, "D:\workspace\country_medical\country_medical\exception-file\exception.txt")
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import time

class CustomDownloaderMiddleware(object):
    def process_request(self, request, spider):
        url = request.url
        try:
            spider.browser.get(url)
        except TimeoutException as e:
            print('超时')
            self.writeFile(url, "time_out_url1.txt")
            # spider.browser.execute_script('window.stop()')
        time.sleep(2)
        html = spider.browser.page_source
        # spider.browser.close()
        return HtmlResponse(url=url, body=html, encoding="utf-8",
                            request=request)

    def process_response(self, request, response, spider):
        self.writeFile(response.url, "req_url.txt")
        return response


    def writeFile(self,url,fileName):
        with open(file=fileName, mode="a", encoding="utf-8") as file:
            file.write(url)
            file.write("\n")
