from lxml import etree
from scrapy import cmdline


def task1():
    print("TASK 1")
    cmdline.execute("scrapy crawl stejka".split())
    root = None
    with open('results/stejka.xml', 'r') as file:
        root = etree.parse(file)
    links = root.xpath('//page/@url')
    print('List of hyperlinks: ')
    print(links)
    print("TASK 1 END")
