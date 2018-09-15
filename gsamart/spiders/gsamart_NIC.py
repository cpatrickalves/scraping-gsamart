# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser

class GsamartNicSpider(scrapy.Spider):
	name = 'gsamart_NIC'
	allowed_domains = ['search.testmart.com/search/']
	start_urls = ['https://search.testmart.com/search/sitesearch.cfm']

	def parse(self, response):
		url = "https://search.testmart.com/search/sitesearch.cfm"

		# This header was taken from Chrome code inspect tool
		request_header = {"q": "National Instruments Corporation", 
						"frommonth": "1", 
						"fromdate": "1", 
						"fromyear": "2000",								
						"searchquote": "y"}

		yield scrapy.http.FormRequest(url, formdata=request_header, dont_filter=True, callback=self.parse_search_results)		

	def parse_search_results(self,response):
		#open_in_browser(response)
		# Get all the links to the detail description of results
		list_of_links = response.xpath('//*[@class="description"]/@onclick').extract()

		for link in list_of_links:
			# Clean the link
			link_to_scrape = link.replace("self.location='",'').replace('\'','')
			# Send a Request to the link and extract the infomation
			yield scrapy.http.Request(link_to_scrape, self.parse_link, dont_filter=True)

	def parse_link(self,response):
		name = response.xpath("//*[@id='purchaseinfo']/h1/text()").extract_first()
		other_infos = response.xpath("//*[@id='purchaseinfo']/p/text()").extract()
		
		warranty = other_infos[0].replace("\r\n\t\t\t\t\t\t","").split(":")[1].strip()
		shipping = other_infos[1].replace("\r\n\t\t\t\t\t\t","").split(":")[1].strip()
		ships_in = other_infos[2].replace("\r\n\t\t\t\t\t\t","").split(":")[1].strip()
		country_of_origin = other_infos[3].replace("\r\n\t\t\t\t\t\t","").split(":")[1].strip()
		sin = other_infos[4].replace("\r\n\t\t\t\t\t\t","").split(":")[1].strip()
		part_no = other_infos[5].replace("\r\n\t\t\t\t\t\t","").split(":")[1].strip()
		
		temp = response.xpath("//*[@id='purchaseinfo']/p/text()").extract()[6].replace("\r\n\t\t\t\t\t\t","").split(":")[1:3]
		gsa_schedule = " ".join(temp).replace("\r\n\t\t\t\t\t","").strip()

		#description = "".join(response.xpath("//*[@class='productDescription']//text()").extract()).replace("  \r\n\t\t","").replace("\r\n\t\t\t\r\n\t\t\t","").replace("\n","")

		yield { "name":name,
				"warranty":warranty,
				"shipping":shipping,
				"ships_in":ships_in,
				"country_of_origin":country_of_origin,
				"sin":sin,
				"part_no":part_no,
				"gsa_schedule":gsa_schedule
				#"description":description
				}

