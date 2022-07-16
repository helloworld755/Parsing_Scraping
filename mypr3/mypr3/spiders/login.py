import scrapy
from scrapy import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/basic_login']

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrfmiddlewaretoken']/@value").get()

        yield FormRequest.from_response(
            response,
            formxpath="//form[@method='post']",
            formdata={
                'name': 'scrapingclub',
                'password': 'scrapingclub',
                'csrfmiddlewaretoken': csrf_token
            },
            callback=self.after_login
        )

    def after_login(self, response):
        yield {'result': response.xpath("//div[@class='row']/div[1]/div[2]/p/text()").get()}
