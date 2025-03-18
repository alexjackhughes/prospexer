# Prospexer

This is a tool to scrape VC team pages and extract contact information.

Simply add your data into the `data.csv` file and run the script.

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
