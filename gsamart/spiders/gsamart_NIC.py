# -*- coding: utf-8 -*-
import scrapy
from math import ceil

# Scrape data from testmart.com for the search string "National Instruments Corporation"
class GsamartNicSpider(scrapy.Spider):
	name = 'gsamart_nic' 
	allowed_domains = ['search.testmart.com']	
	url = "https://search.testmart.com/search/sitesearch.cfm"
	
	# This header was taken from Chrome code inspect tool
	request_header = {"q": "National Instruments Corporation", 
					"frommonth": "1", 
					"fromdate": "1", 
					"fromyear": "2000",								
					"searchquote": "y"}

	def start_requests(self):
		# Send a POST with search parameters
		# OBS: The returned object must be a iterable 
		return [scrapy.http.FormRequest(self.url, formdata=self.request_header, 
										dont_filter=True, callback=self.parse)]
	
	# Parse the response
	def parse(self,response):
		
		# Number of search results 
		n_results = int(response.xpath("//*[@class='top-controls']//span/text()").extract_first().replace(',',''))

		# Each page show 50 results, then the number of page is:
		n_pages = ceil(n_results/50)

		# Extract the pagination link
		pagination = response.xpath("//*[@class='pagination']//@href").extract_first()
		
		# Generate the link for each page
		for n in range(n_pages):
			page_number = n+1
			self.log("Scraping Page {} of {}".format(page_number, n_pages))
			page = pagination.replace('page=2','page={}'.format(page_number))

			yield scrapy.http.Request(page, self.parse_page, dont_filter=True)

	def parse_page(self,response):
		# Get all the products links in this page
		list_of_links = response.xpath('//*[@class="description"]/@onclick').extract()

		for link in list_of_links:
			# Clean the link
			link_to_scrape = link.replace("self.location='",'').replace('\'','')
			
			# Send a Request to the link and extract the infomation
			yield scrapy.http.Request(link_to_scrape, self.parse_link, dont_filter=True)

	# Extract the information
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
