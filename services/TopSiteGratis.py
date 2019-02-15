from model.Servicemodel import ServiceRecord
from scrapy import Spider, Request


from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class TopSiteGratis(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(TopSiteGratis,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []



        for node in response.xpath(
                "//div[@class='reviews product-reviews']/div[@class='item']/p[@class='excerpt']"):
            reviews.append(node.xpath('string()').extract());
        ratings = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/div[@class='right-block']/div[@class='ratings']/span[@class='rate_False']/span").extract()
        dates = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/meta[@itemprop='datePublished']/@content").extract()
        authors = response.xpath("//div[@class='reviews product-reviews']/div[@class='item']/div[@class='author-info']/a/text()").extract()
        img_src = response.xpath(
            "//div[@class='row product']/div[@class='col-md-3 text-center']/img[@class='log_img']/@src").extract()
        # headings = response.xpath("//div[@class='pr-review-wrap']/div[@class='pr-review-rating-wrapper']/div[@class='pr-review-rating']/p[@class='pr-review-rating-headline']/text()").extract()
        website_name = response.xpath("//div[@class='col-md-6 text-right addReviewDiv']/a[@class='btn btn-warning btn-goto']/@href").extract()[0]

        website_name = 'http://topsitegratis.com.br'+website_name
        print("Reviews ", len(reviews))
        print("Authors ", len(authors))
        print("Rating ", len(ratings))
        print("Dates ", len(dates))
        print("img_src ", len(img_src))
        print("websites ", len(website_name), website_name)
        for item in range(0, len(reviews)):
            servicename1 = ServiceRecord(response.url, ratings[item], None, dates[item], authors[item], self.category,
                                         self.servicename, reviews[item], img_src[0], website_name)
            self.save(servicename1)
        self.pushToServer()





