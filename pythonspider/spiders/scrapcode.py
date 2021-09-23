import scrapy


def parse_items(response):
    breadcrumbs = response.xpath('//a[@class="breadcrumbs-list__link"]/text()').getall()
    imag_url = response.xpath('//a[@class="show-gallery"]/@href').get()
    image_url = 'https:'+imag_url
    brand = response.xpath("//h1[@class='title']/text()").get()
    pn = response.xpath("//span[@class='product-detail-label']/text()").get()
    pn1 = response.xpath("//a[@href='/collections/carbon38']/text()").get()
    product_name = pn+pn1
    pr = response.xpath('//span[contains(.,"$")]/text()').get()
    price = str(pr)
    reviews = response.xpath("//div[@class='okeReviews-reviewsSummary-ratingCount']/span/text()").get()
    if reviews is None:
        reviews = "0 Reviews"
    size = response.xpath('//*[@id="SingleOptionSelector-1"]/option/text()').getall()
    colour = response.xpath('//*[@id="SingleOptionSelector-0"]/option/text()').getall()
    t = response.xpath('/html/head/meta[4]/@content').get()
    description = str(t)
    sku = response.xpath('//p[contains(.,"SKU")]/text()').get()
    yield {
        'breadcrumbs': breadcrumbs,
        'product_url':response.xpath('//link[@rel="canonical"]/@href').get(),
        'image_url': image_url,
        'brand': brand,
        'product_name': product_name,

        'price': price.strip(),
        'reviews': reviews,
        'colour': colour,
        'sizes': size,
        'description': description.strip(),
        'sku': sku
    }


class ScrapSpider(scrapy.Spider):
    name = 'posts'
    start_urls = ['https://carbon38.com/collections/tops']

    def parse(self, response):
        lst = []
        for quotes in response.css("a.product-link").xpath("@href"):
            lst.append(quotes)
        q = len(lst)
        for i in range(0, q):
            url = lst[i]
            yield response.follow(url.extract(), callback=parse_items)
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


