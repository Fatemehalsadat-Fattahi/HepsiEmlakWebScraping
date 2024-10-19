# Hepsiemlak Scrapy Project

This is a Scrapy-based project designed to scrape rental apartment data from **hepsiemlak.com**. It extracts relevant details such as listing date, neighborhood, price, and more, and saves the data to a CSV file.

## Features

- Scrapes rental listings from Buca, İzmir.
- Extracts key property details such as:
  - Listing date
  - Neighborhood
  - Floor level
  - Number of rooms
  - Size (in m²)
  - Furnished status
  - Natural gas availability
  - Rent price
- Outputs the scraped data to a CSV file in UTF-32 encoding.
- Supports pagination to scrape multiple pages (up to 21).

## Setup and Usage

### Prerequisites

- Python 3.x
- Scrapy

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/hepsiemlak-scrapy-project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd hepsiemlak-scrapy-project
    ```
3. Install the required Python packages:
    ```bash
    pip install scrapy
    ```

### Running the Spider

To start scraping the data:

```bash
scrapy crawl hepsiemlak
