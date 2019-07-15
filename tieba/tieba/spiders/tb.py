# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from ..items import TiebaItem

class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/f?kw=%E7%94%B5%E8%A7%86%E5%89%A7&red_tag=u0117323856']

    def parse(self, response):
        div_list = response.xpath("//div[@class='threadlist_title pull_left j_th_tit ']")
        for div in div_list:
            item = TiebaItem()
            item['href'] = div.xpath("./a/@href").extract_first()
            item['title'] = div.xpath("./a/text()").extract_first()
            item['url']=[]
            if item['href'] is not None:
                item['href'] = urljoin(response.url, item['href'])
            yield scrapy.Request(
                item['href'],
                callback=self.parse_detail,
                meta={'item': item},
            )
        next_url = response.xpath("//a[text()='下一页>']/@href").extract_first()
        if next_url:
            url='http:'+next_url

            yield scrapy.Request(
                url,
                callback=self.parse,
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['url'].extend(response.xpath("//img[@class='BDE_Image']/@src").extract())
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            url = "http://tieba.baidu.com" + next_url
            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                meta={'item': item}
            )
        else:
            # print(item)
            yield item
