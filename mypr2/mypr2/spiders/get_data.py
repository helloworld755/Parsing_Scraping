import scrapy
from scrapy_splash import SplashRequest

class GetDataSpider(scrapy.Spider):
    name = 'get_data'
    allowed_domains = ['scrapingclub.com']
    # start_urls = ['https://scrapingclub.com/exercise/detail_sign/']

    script = '''
    function main(splash, args)
        url = args.url
        assert(splash:go(url))
        assert(splash:wait(1))
        return {
          html = splash:html()
        }
    end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://scrapingclub.com/exercise/detail_sign/',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        items = response.xpath("//div[@class='card mt-4 my-4']")
        for item in items:
            yield {
                'image': response.urljoin(item.xpath(".//img[@class='card-img-top img-fluid']/@src").get()),
                'name': item.xpath(".//div[@class='card-body']/h4[@class='card-title']/text()").get(),
                'price': item.xpath(".//div[@class='card-body']/h4[@class='card-price']/text()").get(),
                'description': item.xpath(".//div[@class='card-body']/p[@class='card-description']/text()").get()
            }
