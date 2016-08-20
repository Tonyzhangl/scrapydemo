# -*- coding:utf-8 -*-
import json
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tutorial.items import TutorialItem


class DmozSpider(scrapy.Spider):

    name = "dmoz"
    allow_domain = ['lianjia.com']
    start_urls = [
        "http://su.fang.lianjia.com"
    ]

    def parse(self, response):
        # base_url = response.css(".wrapper").xpath("./div").css(".main-box")[0].css(".col-1")
        page_box = response.css(".wrapper").xpath("./div").css(".main-box")[0].css(".page-box")
        total_page = json.loads(page_box.xpath('@page-data').extract()[0]).get("totalPage")
        for n in xrange(1, total_page+1):
            url = response.urljoin('list/pg' + str(n))
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        base_url = response.css(".wrapper").xpath("./div").css(".main-box")
        item = TutorialItem()
        item['title'] = base_url.css(".col-1").xpath('./h2/a/text()').extract()
        item['where'] = [ where.strip() for where in base_url.css(".col-1").css('.where').xpath('./span/text()').extract()]
        item['area'] = [area.strip() for area in base_url.css('.area').xpath('./span/text()').extract()]
        ty_t = base_url.css(".type").xpath("./span/span/text()").extract()
        item['ty'] = [','.join(ty_t[i*4:i*4+3]) for i in xrange(len(ty_t)/4)]
        item['price'] = base_url.css(".col-2").css('.num').xpath('./text()').extract()
        yield item
