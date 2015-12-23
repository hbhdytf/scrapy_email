import re
import sys

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from dirbot.items import Website

reload(sys)
sys.setdefaultencoding('utf-8')


class StaffBaidu(Spider):
    name = "staff_baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com/s?wd=site%3Astaff.ustc.edu.cn&pn=00&oq=site%3Astaff.ustc.edu.cn&tn=baiduhome_pg&ie=utf-8",
    ]
    url = 'http://www.baidu.com'

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//div[@id="content_left"]/div')


        #        items = []

        for site in sites:
            #            item = Website()
            #            item['name'] = site.xpath('h3/a/text()').extract()
            #            item['url'] = site.xpath('h3/a/@href').extract()
            #            item['description'] = site.xpath('h3/*').re("(?<=\>)(.*)\<\/a\>")[0].replace("<em>","").replace("</em>","")
            #            items.append(item)
            try:
                url = site.xpath('h3/a/@href').extract()[0]
            except:
                continue
            name = site.xpath('h3/*').re("(?<=\>)(.*)\<\/a\>")[0].replace("<em>", "").replace("</em>", "")
            meta = {}
            meta["url"] = url
            meta["name"] = name
            yield Request(url, callback=self.crawl_baidu, meta={"meta": meta})
        # return items
        if sel.xpath('//div[@id="page"]/a[1]/@class').extract():  # not first page
            nextlink = sel.xpath('//div[@id="page"]/a[11]/@href').extract()
        else:
            nextlink = sel.xpath('//div[@id="page"]/a[10]/@href').extract()

        if nextlink:
            nextlink = self.url + nextlink[0]
            print nextlink
            yield Request(nextlink, callback=self.parse)

    def crawl_baidu(self, response):
        """

        :param response:
        :return:
        """
        meta = response.meta["meta"]

        email = []
        userid=response.url.split('/')[3]
        if len(userid)>0 and userid[0]=='~':
            email.append(userid[1:]+'@ustc.edu.cn')
        print email
        item = Website()
        item["name"] = meta["name"]
        item["url"] = response.url
        item["email"] = email
        yield item
