# Prospexer

This is a tool to automatically scrape venture capital firm team pages and extract contact information at scale. It uses advanced AI to find and process team pages, making it easy to build targeted contact lists for your outreach.

It could easily be extended to scrape other types of pages, such as companies etc. just change the search query in `main.py`.

## What it does

- 🔍 Automatically finds VC team/about pages using Exa's search API
- 📄 Scrapes the content using Firecrawl's reliable scraping service
- 🤖 Extracts contact details using OpenAI's language models
- 📊 Outputs structured contact data in CSV format

## Quick Start

Simply add your target VC firms into the `data.csv` file (one firm name per row) and run the script. The tool will:

1. Search for each firm's team page
2. Scrape the content
3. Extract contact information
4. Save results to a new CSV file

Perfect for founders, recruiters, and anyone who needs to build VC contact lists efficiently.

## Prerequisites

- **Python** 3.8+
  - [Download & install Python](https://www.python.org/downloads/)
  - Verify with:
    ```bash
    python --version
    ```
- **pip** (usually comes with Python)

  - Check with:
    ```bash
    pip --version
    ```

- **Dependencies**:
  - [exa-py](https://pypi.org/project/exa-py/) (for web searches)
  - [firecrawl](https://pypi.org/project/firecrawl/) (for website scraping)
  - [openai](https://pypi.org/project/openai/) (for contact extraction)

## Installation

1. Clone or download this repository.
   ```bash
   git clone https://github.com/alexjackhughes/prospexer.git
   cd prospexer
   ```
2. Install dependencies:
   ```bash
   pip install exa-py firecrawl openai pandas
   ```

## Usage

1. **Set up your keys**

   - In `main.py`, fill in your keys:
     ```python
     EXA_API_KEY = "YOUR_EXA_API_KEY"
     FIRECRAWL_API_KEY = "fc-YOUR_FIRECRAWL_API_KEY"
     OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
     ```

2. **Add your `data.csv`**

   - Place a file named `data.csv` in the same folder as `main.py`.
   - Ensure there is a column named `name`, containing each VC’s name.

3. **Run the script**

   ```bash
   python main.py
   ```

4. **Output**
   - A new file named `results.csv` will be created with columns:
     - `Name`
     - `Job Title`
     - `Company`
     - `Contact Info`

## Notes

- **Search Query**: By default, the script looks for `<vc_name> team page`. You can tweak this in the `find_team_page` function within `main.py`.
- **Extraction Prompt**: In `extract_contacts_from_text`, you can modify the prompt sent to OpenAI for more precise contact info or a different output format.
- **Error Handling**: If any step fails (e.g. no results, invalid URL), the script may skip or log an error. You can refine this as needed.

## License

This project is licensed under the MIT License - see below for details:

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
