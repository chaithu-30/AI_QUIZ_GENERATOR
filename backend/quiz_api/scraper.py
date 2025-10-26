import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional

def scrape_wikipedia(url: str, timeout: int = 10) -> Dict[str, str]:
    """
    Scrapes a Wikipedia article and returns cleaned content.
    
    Args:
        url: Wikipedia article URL
        timeout: Request timeout in seconds
        
    Returns:
        Dictionary with 'title', 'cleaned_text', and 'raw_html'
        
    Raises:
        ValueError: If URL is not a valid Wikipedia URL
        requests.RequestException: If the request fails
    """
    # Validate Wikipedia URL
    if not url.startswith('https://en.wikipedia.org/wiki/'):
        raise ValueError("URL must be a Wikipedia article (https://en.wikipedia.org/wiki/...)")
    
    try:
        # Fetch the page with a user agent to avoid blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Store raw HTML (bonus requirement)
        raw_html = response.text
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        # Extract title from h1#firstHeading
        title_tag = soup.find('h1', id='firstHeading')
        if not title_tag:
            raise ValueError("Could not find article title")
        title = title_tag.get_text(strip=True)
        
        # Find main content area
        content_div = soup.find('div', id='mw-content-text')
        if not content_div:
            raise ValueError("Could not find article content")
        
        # Get the parser output (actual article body)
        parser_output = content_div.find('div', class_='mw-parser-output')
        if not parser_output:
            parser_output = content_div
        
        # Remove unwanted elements before extraction
        # Remove reference links [1], [2], etc.
        for sup in parser_output.find_all('sup', class_='reference'):
            sup.decompose()
        
        # Remove citation needed tags
        for cite in parser_output.find_all('sup', class_='noprint'):
            cite.decompose()
            
        # Remove edit section links
        for edit in parser_output.find_all('span', class_='mw-editsection'):
            edit.decompose()
        
        # Remove infoboxes, navigation boxes, and tables
        for element in parser_output.find_all(['table', 'div'], 
                                               class_=['infobox', 'navbox', 
                                                      'vertical-navbox', 'sidebar']):
            element.decompose()
        
        # Remove images and figures
        for element in parser_output.find_all(['figure', 'img']):
            element.decompose()
        
        # Extract text from paragraphs and headers
        sections = []
        current_section = []
        
        for element in parser_output.find_all(['h2', 'h3', 'p']):
            if element.name in ['h2', 'h3']:
                # Save previous section
                if current_section:
                    sections.append(' '.join(current_section))
                    current_section = []
                # Add header text
                header_text = element.get_text(strip=True)
                # Remove edit links from headers
                header_text = re.sub(r'\[edit\]', '', header_text)
                if header_text and header_text not in ['See also', 'References', 
                                                       'External links', 'Notes']:
                    current_section.append(f"\n## {header_text}\n")
            elif element.name == 'p':
                text = element.get_text(strip=True)
                if text:  # Only add non-empty paragraphs
                    current_section.append(text)
        
        # Add last section
        if current_section:
            sections.append(' '.join(current_section))
        
        # Join all sections
        cleaned_text = '\n\n'.join(sections)
        
        # Remove extra whitespace and multiple newlines
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        cleaned_text = re.sub(r' +', ' ', cleaned_text)
        
        # Truncate if too long (LLM context limits)
        max_length = 15000  # Characters
        if len(cleaned_text) > max_length:
            cleaned_text = cleaned_text[:max_length] + "\n\n[Content truncated due to length]"
        
        return {
            'title': title,
            'cleaned_text': cleaned_text,
            'raw_html': raw_html
        }
        
    except requests.Timeout:
        raise requests.RequestException(f"Request timed out after {timeout} seconds")
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch Wikipedia page: {str(e)}")
