import scrapy


class MarketSpider(scrapy.Spider):
    name = "market"
    fields = {
        'link_pagination': '//ul[@class="pagination"]//a/@href',
        'link_category': '//li[@class="accordion-group"]/a/@href',
        'product': '//div[@class="product-block item-default clearfix"]',
        'price': './/span[@class="special-price"]/text()',
        'name': './/div[@class="product-meta-inner"]//h3[@class="name"]/a/text()',
        'img': './/img[@class="img-responsive"]/@src',
        'product_link': './/div[@class="product-meta-inner"]//h3[@class="name"]/a/@href',
    }
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ITEMCOUNT': 20
    }
    start_urls = [
        'https://mebli-lviv.com.ua/ua/dyvanu_pryami/'
    ]
    allowed_domains = [
        'mebli-lviv.com.ua'
    ]

    def parse(self, response):
        for product in response.xpath(self.fields["product"]):
            yield {
                'link': product.xpath(self.fields['product_link']).extract(),
                'price': product.xpath(self.fields['price']).extract(),
                'img': product.xpath(self.fields['img']).extract(),
                'name': ''.join(product.xpath(self.fields['name']).extract())
            }
        for a in response.xpath(self.fields["link_category"]):
            yield response.follow(a.extract(), callback=self.parse)
        for a in response.xpath(self.fields["link_pagination"]):
            yield response.follow(a.extract(), callback=self.parse)
