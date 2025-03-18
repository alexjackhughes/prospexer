import csv
import pandas as pd
from exa_py import Exa
from firecrawl import FirecrawlApp
from openai import OpenAI

# --- CONFIG ---
EXA_API_KEY = 'YOUR KEY' # You can get yours here: https://dashboard.exa.ai/api-keys
FIRECRAWL_API_KEY = 'YOUR KEY' # You can get yours here: https://www.firecrawl.dev/app/api-keys
OPENAI_API_KEY = 'YOUR KEY' # You can get yours here: https://platform.openai.com/api-keys

client = OpenAI(api_key=OPENAI_API_KEY)

import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize clients
exa = Exa(EXA_API_KEY)
firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def find_team_page(vc_name: str) -> str:
    """
    Uses Exa to search for the VC's team page.
    Returns the best URL found or an empty string if none found.
    """
    logger.info(f"Searching for team page for VC: {vc_name}")
    # Adjust query as needed
    query = f"{vc_name} VC 'meet the team/about us/people' page"
    response = exa.search(query=query, type='auto', num_results=3)

    # Access results directly from the SearchResponse object
    if response.results and len(response.results) > 0:
        logger.info(f"Found team page URL: {response.results[0].url}")
        return response.results[0].url
    logger.warning(f"No team page found for {vc_name}")
    return ""

def scrape_markdown(url: str) -> str:
    """
    Uses Firecrawl batch_scrape_urls to scrape markdown from a single URL.
    Returns the markdown as a string.
    """
    if not url:
        logger.warning("No URL provided for scraping")
        return ""
    try:
        logger.info(f"Scraping markdown from URL: {url}")
        scrape_result = firecrawl.batch_scrape_urls([url], {'formats': ['markdown']})

        # Check if we have valid data in the response
        if scrape_result and isinstance(scrape_result, dict) and 'data' in scrape_result:
            data = scrape_result['data']
            if data and isinstance(data, list) and len(data) > 0:
                logger.info("Successfully scraped markdown content")
                return data[0].get('markdown', '')
    except Exception as e:
        logger.error(f"Error scraping URL {url}: {str(e)}")
        pass
    return ""

def extract_contacts_from_text(text: str) -> list:
    """
    Uses OpenAI to parse the text (markdown) and extract:
    Name, Job Title, Company, and Contact Info (email/phone/linkedin).
    Returns a list of dicts with the parsed info.
    """
    if not text.strip():
        logger.warning("No text provided for contact extraction")
        return []

    logger.info("Extracting contacts using OpenAI")
    prompt = f"""
Extract any team members' details from the following text.
Return each person in JSON lines, with keys: Name, Job Title, Company, Contact Info.

Text:
{text}
"""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0)

        # You can refine how you parse the response based on how you instruct the model.
        raw_output = response.choices[0].message.content

        # Very rough example: if the model returns valid JSON lines, parse them.
        # Real usage might require robust JSON parsing or a more structured approach.
        contacts = []
        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = eval(line)  # or use json.loads if valid JSON
                if isinstance(data, dict):
                    contacts.append(data)
            except Exception as e:
                logger.warning(f"Failed to parse contact line: {line}. Error: {str(e)}")
                pass

        logger.info(f"Successfully extracted {len(contacts)} contacts")
        return contacts
    except Exception as e:
        logger.error(f"Error during OpenAI contact extraction: {str(e)}")
        return []

def main():
    logger.info("Starting the contact extraction process")

    # Read data.csv
    try:
        df = pd.read_csv('data.csv')  # expects a column 'name'
        logger.info(f"Successfully loaded data.csv with {len(df)} rows")
    except Exception as e:
        logger.error(f"Failed to load data.csv: {str(e)}")
        return

    all_contacts = []

    for idx, row in df.iterrows():
        vc_name = row['name']
        logger.info(f"Processing VC {idx + 1}/{len(df)}: {vc_name}")

        # 1) Search for team page
        team_url = find_team_page(vc_name)

        # 2) Scrape page as markdown
        page_markdown = scrape_markdown(team_url)

        # 3) Use OpenAI to extract contact info
        contacts = extract_contacts_from_text(page_markdown)

        # 4) Collect results
        for c in contacts:
            # Ensure the keys exist
            all_contacts.append({
                'Name': c.get('Name', ''),
                'Job Title': c.get('Job Title', ''),
                'Company': c.get('Company', vc_name),  # default to the VC name if not found
                'Contact Info': c.get('Contact Info', '')
            })

    # Save results to results.csv
    if all_contacts:
        try:
            results_df = pd.DataFrame(all_contacts)
            results_df.to_csv('results.csv', index=False)
            logger.info(f"Successfully saved {len(all_contacts)} contacts to results.csv")
        except Exception as e:
            logger.error(f"Failed to save results.csv: {str(e)}")
    else:
        logger.warning("No contacts found to save")

if __name__ == "__main__":
    main()
