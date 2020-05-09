import scrapy


def isNotEmptyString(str):
    return len(str) > 0


class StejkaSpider(scrapy.Spider):
    name = "stejka"
    custom_settings = {
        'ITEM_PIPELINES': {
            'db_lab_1.pipelines.NewsXmlPipeline': 300,
        }
    }
    fields = {
        'img': '//img/@src',
        'text': '//*[not(self::script)][not(self::style)]/text()',
        'link': '//a/@href'
    }
    start_urls = [
        'https://stejka.com'
    ]
    allowed_domains = [
        'stejka.com'
    ]

    def parse(self, response):
        text = filter(isNotEmptyString,
                      map(lambda str: str.strip(),
                          [text.extract() for text in response.xpath(self.fields["text"])]))
        images = map(lambda url: ((response.url + url) if url.startswith('/') else url),
                     [img_url.extract() for img_url in response.xpath(self.fields["img"])])
        yield {
            'text': text,
            'images': images,
            'url': response.url
        }
        for link_url in response.xpath(self.fields['link']):
            link_url_str = link_url.extract()
            if link_url_str.find('mailto') == -1:
                yield response.follow(link_url_str, callback=self.parse)

