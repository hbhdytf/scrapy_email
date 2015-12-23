import re
import sys

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from dirbot.items import Website

reload(sys)
sys.setdefaultencoding('utf-8')


class StaffSogou(Spider):
    name = "staff_sogou"
    allowed_domains = ["sogou.com","ustc.edu.cn"]
    start_urls = [
        "https://www.sogou.com/web?query=site%3Astaff.ustc.edu.cn",
    ]
    url = 'http://www.sogou.com/web'

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//*[@id="main"]/div/div/div')


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
            try:
                meta["name"] = name.split('>')[1]
            except:
                meta["name"] = name
            yield Request(url, callback=self.crawl_baidu, meta={"meta": meta})
        # return items
        nextlink=sel.xpath('//*[@id="sogou_next"]/@href').extract()
        if nextlink:
            nextlink = self.url + nextlink[0]
            print nextlink
            yield Request(nextlink, callback=self.parse)

    def crawl_sogou(self,response):
        meta = response.meta["meta"]
        yield Request(response.url, callback=self.crawl_baidu, meta={"meta": meta})

    def crawl_baidu(self, response):
        """

        :param response:
        :return:
        """
        meta = response.meta["meta"]
        email=[]
        if "sogou.com" in response.url:
            sel=Selector(response)
            url=sel.xpath('//meta/@content').extract()[1].split('\\')[0].split('\'')[1]
        elif "staff.ustc.edu.cn" in response.url:
            url=response.url
        userid=url.split('/')[3]
        if len(userid)>0 and userid[0]=='~':
            email.append(userid[1:]+'@ustc.edu.cn')
        print email
        item = Website()
        item["name"] = meta["name"]
        item["url"] = response.url
        item["email"] = email
        yield item
