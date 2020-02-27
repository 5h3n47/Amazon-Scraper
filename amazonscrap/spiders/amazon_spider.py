# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import AmazonscrapItem
import pandas
import csv

# shirts link = "https://www.amazon.in/s?k=shirt&i=apparel&bbn=1571272031&rh=n%3A1571271031%2Cn%3A1571272031%2Cn%3A1968024031&dc&page=106&qid=1579882676&rnid=1571272031&ref=sr_pg_106"

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    #DOWNLOAD_DELAY = 5.0
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'test.csv'
    }
    #allowed_domains = ['amazon.com']
    start_urls = [
    'https://www.amazon.in/s?bbn=1968511031&rh=n%3A1571271031%2Cn%3A%211571272031%2Cn%3A1953602031%2Cn%3A11400137031%2Cn%3A15330094031%2Cn%3A1968511031%2Cp_n_feature_nineteen_browse-bin%3A11301357031&dc&fst=as%3Aoff&qid=1582124541&rnid=11301356031&ref=lp_1968511031_nr_p_n_feature_nineteen_0',
    ]

    def parse(self, response):
        #items = AmazonscrapItem()
        #tuple(items)
        
        product_brand = response.css('.s-line-clamp-1 .a-color-base::text').extract()
        product_name = response.css('.a-color-base.a-text-normal::text').extract()
        product_url = response.css('.a-link-normal.a-text-normal::attr(href)').extract()
        product_price = response.xpath(".//span[@class='a-offscreen']/text()").extract()
        #'product_price' : response.css('.a-offscreen span::text').css('::text').extract(),
        product_dprice = response.css('.a-price-whole').css('::text').extract()
        product_rating = response.xpath(".//span[@class='a-icon-alt']/text()").extract()
        #'product_rating' : response.css('.a-icon-row.a-spacing-small.a-padding-none::text').extract(),
        #'product_rating' : response.css('.a-text-price span::text').extract(),
        product_imagelink = response.css('.s-image::attr(src)').extract()

        X = [list(e) for e in zip(product_brand, product_name, product_url,product_price,product_dprice,product_rating,product_imagelink)]
        
        for i, temp in enumerate(X):
            yield{'brand': temp[0], 'product_name': temp[1], 
                'product_url': 'https://www.amazon.in'+str(temp[2]), 'product_price': temp[3], 'product_dprice': temp[4],
                'product_rating': temp[5], 'product_imagelink': temp[6]
                }

        next_page = 'https://www.amazon.in/s?i=apparel&bbn=1968511031&rh=n%3A1571271031%2Cn%3A1571272031%2Cn%3A1953602031%2Cn%3A11400137031%2Cn%3A15330094031%2Cn%3A1968511031%2Cp_n_feature_nineteen_browse-bin%3A11301357031&dc&page='+str(AmazonSpiderSpider.page_number) +'&fst=as%3Aoff&qid=1582124561&rnid=11301356031&ref=sr_pg_2'
        if AmazonSpiderSpider.page_number <= 24:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
        