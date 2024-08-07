# movie1/begin.py
from scrapy import cmdline

# cmdline.execute("scrapy crawl movie1 -a key=乌克兰".split())
cmdline.execute("scrapy crawl movie".split())
