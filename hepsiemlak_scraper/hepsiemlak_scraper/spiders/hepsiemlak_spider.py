import scrapy


class HepsiemlakSpider(scrapy.Spider):
    name = 'hepsiemlak'
    allowed_domains = ['hepsiemlak.com']
    start_urls = ['https://www.hepsiemlak.com/buca-kiralik/daire']

    # Set a custom attribute to track the page number
    page_count = 0  # Initialize page counter

    # Custom settings for this spider
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Adjust this value as needed (2 seconds)
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Ensure only 1 request at a time
        'FEED_FORMAT': 'csv',  # Set output format to CSV
        'FEED_URI': 'output.csv',  # Output file name
        'FEED_EXPORT_ENCODING': 'utf-32',  # Set the encoding for the output
        'CSV_DELIMITER': ';',  # Change delimiter to semicolon
        'RETRY_ENABLED': True,  # Enable retries
        'RETRY_TIMES': 5,  # Number of retries
    }

    def parse(self, response):
        # Extract all <li> elements with the property links
        li_elements = response.xpath('//ul[@class="list-items-container"]//li')

        # Iterate over each <li> element
        for li in li_elements:
            link = li.xpath('.//a[@class="img-link"]/@href').get()

            if link:
                # Build full URL and follow it
                full_link = response.urljoin(link)
                yield scrapy.Request(url=full_link, callback=self.parse_property_page)

        # Increment the page counter after processing the current page
        self.page_count += 1

        # Check if we have scanned less than 21 pages
        if self.page_count < 21:
            # Handle pagination - go to the next page
            next_page = response.xpath('//a[contains(@class, "he-pagination__navigate-text--next")]/@href').get()

            # If the next page is found, follow the link
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.log(f"Next page found: {next_page_url}")
                yield scrapy.Request(url=next_page_url, callback=self.parse)
            else:
                self.log("No next page found.")
        else:
            self.log("Scanned 21 pages, stopping.")

    def parse_property_page(self, response):
        # Scrape the H1 text (property title)
        ilan_metni = response.css('div.left h1::text').get()

        # Scrape the required information
        ilan_tarihi = response.xpath('//li[span[text()="Son Güncelleme Tarihi"]]/span[2]/text()').get()
        mahalle = response.xpath('(//ul[@class="short-property"]//li)[3]/text()').get()
        bulunduğu_kat = response.xpath('//li[span[text()="Bulunduğu Kat"]]/span[2]/text()').get()
        bina_yasi = response.xpath('//li[span[text()="Bina Yaşı"]]/span[2]/text()').get()
        oda_salon_sayisi = response.xpath('//li[span[text()="Oda + Salon Sayısı"]]/span[2]/text()').get()
        brut_net_m2 = response.xpath('//li[span[text()="Brüt / Net M2"]]/span/text()').getall()
        brut_net_m2 = brut_net_m2[1].strip() + brut_net_m2[2].strip() if len(brut_net_m2) > 1 else None
        esya_durumu = response.xpath('//li[span[text()="Eşya Durumu"]]/span[2]/text()').get()
        isinma_tipi = response.xpath('//li[span[text()="Isınma Tipi"]]/span[2]/text()').get()

        # Scrape the price
        kira_bedeli = response.css('p.price::text').get().strip() if response.css('p.price::text').get() else None

        # Return scraped data
        yield {
            'İlan Metni': ilan_metni.strip() if ilan_metni else None,
            'İlan Tarihi': ilan_tarihi.strip() if ilan_tarihi else None,
            'Mahalle': mahalle.strip() if mahalle else None,
            'Bulunduğu Kat': bulunduğu_kat.strip() if bulunduğu_kat else None,
            'Bina Yaşı': bina_yasi.strip() if bina_yasi else None,
            'Oda + Salon Sayısı': oda_salon_sayisi.strip() if oda_salon_sayisi else None,
            'Brüt / Net M2': brut_net_m2,
            'Eşya Durumu': esya_durumu.strip() if esya_durumu else None,
            'Isınma Tipi': isinma_tipi.strip() if isinma_tipi else None,
            'Kira Bedeli': kira_bedeli
        }
