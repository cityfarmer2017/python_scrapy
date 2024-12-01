python3 -m venv venv

source venv/bin/activate

pip install scrapy

scrapy startproject bookscraper

scrapy genspider bookspider books.toscrape.com

[ pip install ipython ]

scrapy shell

	fetch('https://books.toscrape.com')
	response.css('article.product_pod')
	response.css('article.product_pod').get()
	books = response.css('article.product_pod')
	book = books[0]
	book.css('h3 a::text').get()
	book.css('.product_pod .price_color::text').get()
	book.css('h3 a').attrib['href']
	response.css('li.next a ::attr(href)').get()
	
	fetch('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
	response.css('.product_page')
	response.css('.product_main h1::text').get()
	response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
	response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
	
	exit

scrapy crawl bookspider

scrapy crawl bookspider -o bookdata.json

scrapy crawl bookspider -o bookdata.csv

scrapy crawl bookspider -O bookdata.json

scrapy crawl bookspider -O bookdata.csv