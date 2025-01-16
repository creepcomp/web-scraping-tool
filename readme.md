# Web Scraping Tool

This repository contains a Python-based web scraping tool that allows users to extract data from web pages and save it in a structured format (CSV). The tool is designed to be flexible and configurable, enabling users to specify the target URL, the data fields to extract, and the output file.

## Features

- **Configurable Scraping**: Easily configure the scraping parameters using a JSON configuration file.
- **Data Extraction**: Extract data using CSS selectors or regular expressions.
- **CSV Output**: Save the scraped data in a CSV file for easy analysis and manipulation.
- **Error Handling**: Basic error handling to manage request failures and other exceptions.
- **Rate Limiting**: Built-in delay between requests to avoid overwhelming the target server.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Configuration

The tool uses a `config.json` file to define the scraping parameters. Below is an example of the configuration file structure:

```json
{
    "url": "https://example.com/page/{id}",
    "output": "output.csv",
    "item": "item-class",
    "fields": [
        {
            "name": "Field1",
            "selector": ".field1-selector"
        },
        {
            "name": "Field2",
            "pattern": "Pattern to extract Field2: (.*)"
        }
    ]
}
```

### Configuration Fields

- `url`: The URL template for the pages to scrape. Use `{id}` as a placeholder for pagination.
- `output`: The name of the output CSV file.
- `item`: The CSS class or identifier for the items to scrape.
- `fields`: A list of fields to extract, where each field can have:
  - `name`: The name of the field in the output CSV.
  - `selector`: A CSS selector to extract data.
  - `pattern`: A regex pattern to extract data.

## Usage

1. Create a `config.json` file with the desired configuration.
2. Run the script:

```bash
python web_scraping_tool.py
```

3. The scraped data will be saved in the specified output CSV file.

## Example

To scrape data from a hypothetical website, you might set up your `config.json` like this:

```json
{
    "url": "https://example.com/products?page={id}",
    "output": "products.csv",
    "item": "product-item",
    "fields": [
        {
            "name": "Product Name",
            "selector": ".product-name"
        },
        {
            "name": "Price",
            "selector": ".product-price"
        },
        {
            "name": "Description",
            "pattern": "Description: (.*)"
        }
    ]
}
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.
