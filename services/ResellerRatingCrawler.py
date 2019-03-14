from model.Servicemodel import ServiceRecord
from lxml import etree
from services.siteservices.BaseSiteURLCrawler import BaseSiteURLCrawler
class ResellerRatingCrawler(BaseSiteURLCrawler):

    def __init__(self,category,servicename,url):

        self.category = category
        self.servicename = servicename
        self.link = {"ServiceName": servicename,
                "Category": category,
                "url": url}
        super(ResellerRatingCrawler,self).__init__()
        self.createCategory(self.link)
        pass
    def parsing(self, response1):
        return self.crawl(response1)

    def crawl(self, response):
        reviews = []
        print("Reviews from Resellerrating.com")
        # https://www.resellerratings.com/store/Nordvpn_com
        for node in  response.xpath("//div[@class='cell review-body centered-medium']/span"):
            reviews.append(node.xpath('string()').extract());
        headings1= response.xpath("//div[@class='cell review-title centered-medium']").extract()

        # headings =  response.xpath("//div[@class='comment']/p[@class='review-title']/span/text()").extract()
        dates =  response.xpath("//div[@class='cell align-right large-3']/span[@class='date']/text()").extract()
        ratings = response.xpath("///div[@class='cell siteStars large-9']/span[@class='starRating']/strong/text()").extract()
        authors1 =  response.xpath("//div/a[@class='rr-purple store-link']/strong/text()").extract()
        website_name = response.xpath("//html/head/meta[15]/@content").extract()
        authors = []
        headings = []
        for content in headings1:
            root = etree.HTML(content)
            if len(root.xpath("//span/@text()")) > 0:
                headings.append(root.xpath("//span/text()").strip())[0]
            else:
                headings.append("")
        for cont in authors1:
            authors.append(cont.strip())
        print("Reviews ", len(reviews))
        print("Authors ", len(authors), authors)
        print("ratings ", len(ratings), ratings)
        print("headings ", len(headings), headings)

        print("Dates ", len(dates), dates)

        img_src = None
        for item in range(0, len(reviews)):
            if(len(headings)==0):
                servicename1 = ServiceRecord(response.url, ratings[item],None, dates[item], authors[item],
                                             "",
                                             self.servicename, reviews[item], img_src,website_name);
            else:
                servicename1 = ServiceRecord(response.url, ratings[item],headings[item], dates[item], authors[item], self.category,
                          self.servicename, reviews[item],img_src, website_name);
            self.save(servicename1)
        self.pushToServer()
