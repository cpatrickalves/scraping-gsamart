# Scraping products from testmart.com

This project Scrape GSAMART equipment from testmart.com using Scrapy Web Crawling Framework.

At the moment, the project has only one spider (python script) able to scrape the data of all equipment of the National Instruments corporation type.

The scraped data is available in the project ***data/*** directory.

# How to use

You will need Python 3.x to run the scripts.
Python can be downloaded [here](https://www.python.org/downloads/).

You have to install ***scrapy*** framework:
* In command prompt/Terminal: *pip install scrapy*
* If you are using [Anaconda Python distribution](https://anaconda.org/anaconda/python): *conda install -c conda-forge scrapy*

Once you have installed *scrapy* framework, just clone/download this project, access the folder in command prompt/Terminal and run the following command:

*scrapy crawl gsamart_nic -o equipaments.csv*

You can change the output format to JSON or XML by change the output file extension (ex: *equipaments.json*).
