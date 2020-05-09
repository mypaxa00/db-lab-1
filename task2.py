from scrapy import cmdline
import os
from lxml import etree


def crawler():
    #remove if file already exist
    try:
        os.remove("results/market.xml")
    except OSError:
        print("results/market.xml not found")
    #crawling
    cmdline.execute("scrapy crawl market -o results/market.xml -t xml".split())


def xslt_parse():
    dom = etree.parse('results/market.xml')
    xslt = etree.parse('market.xslt')
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    with open('results/market.html', 'wb') as f:
        f.write(etree.tostring(newdom, pretty_print=True))


def task2():
    print("TASK 2")
    crawler()
    xslt_parse()
    print("TASK 2 END")
