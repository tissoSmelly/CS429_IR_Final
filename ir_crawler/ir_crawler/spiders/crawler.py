import scrapy
import os

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["iit.edu"]
    start_urls = ["https://iit.edu"]

    ### later make these part of initilization/calling of this script so it is not hard coded
    max_pages_to_download = 75
    downloaded_pages_count = 0
    max_depth = 10 ## max depth
    current_depth = 0
    seen_pages = set()

    def parse(self, response):
        self.seen_pages.add(response.url) ## keep track of the URL so we don't revisit down the line

        if self.downloaded_pages_count > self.max_pages_to_download:
            self.logger.info(f'Reached the maximum limit of {self.max_pages_to_download} pages.')
            return ## break out of recursion if we are at the max number of pages

        else: ## otherwise not at max pages then keep going
            self.download_page(response) ## download the page we are seeing
            self.downloaded_pages_count += 1  ## add 1
            self.logger.info(f'Number of downloaded pages {self.downloaded_pages_count}')

            links = response.css('a::attr(href)').getall() ## get links from current response page
                                ## now we will visit each link and send it to be parsed while we haven't reached the max depth
                                ## get all links from current response while we aren't too deep keep going
            depth_count = 0 ## count for number of pages we've jumped to
            current_link = 0 ## increment for looking at the next page
            while depth_count < self.max_depth and self.downloaded_pages_count < self.max_pages_to_download:
                next_url = response.urljoin(links[current_link])  ## create absolute URL for the next page to visit

                if next_url not in self.seen_pages:
                    depth_count += 1 ## so actually count as an increase depth if we are going to visit that page
                    self.logger.info(f'Next unseen URL to visit: {next_url}')
                    self.logger.info(f'Current Depth {depth_count}')
                    yield scrapy.Request(next_url, callback = self.parse) ## send the url to parse for recursive calling and processing
                else:
                    self.logger.info(f'Skipping already downloaded URL: {next_url}')

                current_link += 1
    def download_page(self, response):
        output_directory = 'directory_' + self.allowed_domains[0] ## name directory as start url

        if not os.path.exists(output_directory): ## if it doesn't exist yet we make it
            os.makedirs(output_directory)

        filename = os.path.join(output_directory, f'page_{response.url.split("/")[-1]}.html')

        # write response content to file in the directory
        with open(filename, 'wb') as f:
            f.write(response.body)

        # write to logger we have saved the given file
        self.logger.info(f'Downloaded: {response.url}')
