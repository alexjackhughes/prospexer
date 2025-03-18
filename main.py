import csv
import pandas as pd
from exa_py import Exa
from firecrawl import FirecrawlApp
from openai import OpenAI

# --- CONFIG ---
EXA_API_KEY = "YOUR KEY" # You can get yours here: https://dashboard.exa.ai/api-keys
FIRECRAWL_API_KEY = "YOUR KEY" # You can get yours here: https://www.firecrawl.dev/app/api-keys
OPENAI_API_KEY = "YOUR KEY" # You can get yours here: https://platform.openai.com/api-keys

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
Return a JSON array of objects, where each object has these keys: Name, Job Title, Company, Contact Info.
Format the response as a single valid JSON array.

Text:
{text}
"""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0)

        # Get the response content
        raw_output = response.choices[0].message.content.strip()

        # Try to parse the entire response as JSON
        try:
            import json
            contacts = json.loads(raw_output)
            if not isinstance(contacts, list):
                contacts = [contacts]  # Convert single object to list
            logger.info(f"Successfully extracted {len(contacts)} contacts")
            return contacts
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return []

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

    # Create or load existing results file
    try:
        results_df = pd.read_csv('results.csv')
        logger.info("Loaded existing results.csv file")
    except FileNotFoundError:
        results_df = pd.DataFrame(columns=['Name', 'Job Title', 'Company', 'Contact Info'])
        results_df.to_csv('results.csv', index=False)
        logger.info("Created new results.csv file")

    for idx, row in df.iterrows():
        vc_name = row['name']
        logger.info(f"Processing VC {idx + 1}/{len(df)}: {vc_name}")

        # 1) Search for team page
        team_url = find_team_page(vc_name)

        # 2) Scrape page as markdown
        page_markdown = scrape_markdown(team_url)

        # 3) Use OpenAI to extract contact info
        contacts = extract_contacts_from_text(page_markdown)

        # 4) Process and save results immediately
        if contacts:
            new_contacts = []
            for c in contacts:
                new_contacts.append({
                    'Name': c.get('Name', ''),
                    'Job Title': c.get('Job Title', ''),
                    'Company': c.get('Company', vc_name),  # default to the VC name if not found
                    'Contact Info': c.get('Contact Info', '')
                })

            # Append new contacts to results and save immediately
            new_df = pd.DataFrame(new_contacts)
            results_df = pd.concat([results_df, new_df], ignore_index=True)
            results_df.to_csv('results.csv', index=False)
            logger.info(f"Saved {len(new_contacts)} contacts for {vc_name} to results.csv")
        else:
            logger.warning(f"No contacts found for {vc_name}")

    logger.info("Completed processing all VCs")

if __name__ == "__main__":
    main()
