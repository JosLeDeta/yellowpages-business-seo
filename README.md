# yellowpages-business-seo
yellowpages-business-seo is an analyzing tool to classify business web pages based on their seo score using Google PageSpeed Insights.

An API key is required to perform page analisys.
Edit analyzer.py and put your key.

It can collect business data from different sites.
- YellowPages Canada
- PaginasAmarillas España

## Usage 

To run the terminal client version:

```bash
usage: terminal_cli.py [-h] [--provider PROVIDER] category location n_pages

positional arguments:
  category             category to search
  location             city name
  n_pages              N pages to scan

optional arguments:
  -h, --help           show this help message and exit
  --provider PROVIDER  ES or CA (Default: ES)
```

To run the web version:

```bash
python main.py
```