# GrabAndGo

A powerful and efficient tool for downloading images from various websites with support for custom templates and concurrent downloads.

## Features

- **Hybrid Architecture**: Combines Python for web scraping and Go for high-performance downloads
- **Template-based Parsing**: Easily add support for new websites using YAML templates
- **Concurrent Downloads**: Fast and efficient downloads using Go's concurrency model
- **Error Handling**: Robust error handling and retry mechanisms
- **Configurable**: Customize download behavior through configuration

## Prerequisites

- Python 3.7+
- Go 1.16+
- Chrome/Chromium (for Selenium)
- ChromeDriver

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GrabAndGo.git
   cd GrabAndGo
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Go downloader:
   ```bash
   cd src/main/downloader
   go mod download
   go build -o grabber
   cd ../../..
   ```

## Usage

### Basic Usage

```bash
python src/main/download_images.py --url "https://example.com/gallery"
```

### Command Line Options

```
usage: download_images.py [-h] [--output-dir OUTPUT_DIR] [--concurrency CONCURRENCY] [--timeout TIMEOUT] [--no-skip] [--verbose] url

Download images from a given URL.

positional arguments:
  url                   URL of the page containing images

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Directory to save downloaded images (default: ./images)
  --concurrency CONCURRENCY, -c CONCURRENCY
                        Number of concurrent downloads (default: 5)
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout in seconds for each download (default: 30)
  --no-skip             Download files even if they already exist (default: skip existing)
  --verbose, -v         Print detailed progress information
```

## Adding Support for New Websites

1. Create a new template file in `config/templates/` (e.g., `example.yaml`):
   ```yaml
   domain: example.com
   name: Example Site
   selectors:
     images: "img.photo"
     next_page: "a.next-page"
   ```

2. Create an instruction file in `config/instructions/` (e.g., `example.py`):
   ```python
   from selenium.webdriver.common.by import By
   from selenium.webdriver.support import expected_conditions as EC

   def parse_post(url, selectors):
       # Implementation for parsing a single post
       pass

   def parse_folder(url, selectors):
       # Implementation for parsing a folder/gallery
       pass
   ```

## Project Structure

```
GrabAndGo/
├── config/
│   ├── templates/       # YAML templates for different websites
│   └── instructions/    # Python modules with parsing logic
├── src/
│   └── main/
│       ├── downloader/  # Go downloader implementation
│       ├── parser/      # Python parser implementation
│       └── download_images.py  # Main script
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License - see the [LICENSE](LICENSE) file for details.
