import scrapy


class GetDataSpider(scrapy.Spider):
    name = 'get_data'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/list_basic/']

    def parse(self, response):
        all_items = response.xpath("//div[@class='card']")
        for item in all_items:
            name = item.xpath(".//div/h4/a/text()").get()
            price = item.xpath(".//div/h5/text()").get()
            image = response.urljoin(item.xpath(".//a/img/@src").get())
            item_link = response.urljoin(item.xpath(".//a/@href").get())

            item_dict = {
                "name": name,
                "price": price,
                "image": image
            }
            yield scrapy.Request(
                url=item_link,
                callback=self.parse_item,
                meta={'item_dict': item_dict}
            )

        next_page = response.xpath("//nav/ul/li/a[contains(text(), 'Next')]/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse
            )

    def parse_item(self, response):
        item_dict = response.meta['item_dict']
        item_dict['description'] = response.xpath("//p[@class='card-text']/text()").get()
        item_dict['item_url'] = response.url
        yield item_dict
