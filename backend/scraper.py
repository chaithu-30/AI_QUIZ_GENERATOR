import requests
from bs4 import BeautifulSoup
from typing import Tuple, Optional
import re

def clean_text(text: str) -> str:
    """Remove extra whitespace and normalize text"""
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove citation brackets like [1], [2]
    text = re.sub(r'\[\d+\]', '', text)
    return text.strip()

def scrape_wikipedia(url: str) -> Tuple[str, str, str]:
    """
    Scrape Wikipedia article and extract clean content.
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Tuple of (title, clean_text, raw_html)
        
    Raises:
        ValueError: If URL is invalid or article not found
        requests.RequestException: If network error occurs
    """
    # Validate Wikipedia URL
    if not url.startswith('https://en.wikipedia.org/wiki/'):
        raise ValueError("Invalid Wikipedia URL. Must be an English Wikipedia article.")
    
    try:
        # Fetch the page with timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Educational Quiz Generator Bot)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
    except requests.Timeout:
        raise ValueError("Request timed out. Wikipedia might be slow or unreachable.")
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch article: {str(e)}")
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title_element = soup.find('h1', {'id': 'firstHeading'})
    if not title_element:
        raise ValueError("Could not find article title. Invalid Wikipedia page.")
    
    title = title_element.get_text().strip()
    
    # Find main content div
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if not content_div:
        raise ValueError("Could not find article content. Page structure may have changed.")
    
    # Remove unwanted elements
    for element in content_div.find_all(['sup', 'table', 'style', 'script']):
        element.decompose()
    
    # Remove reference sections
    for heading in content_div.find_all(['h2', 'h3']):
        heading_text = heading.get_text().lower()
        if any(term in heading_text for term in ['references', 'external links', 'see also', 'notes']):
            # Remove this section and everything after it
            for sibling in list(heading.next_siblings):
                if sibling.name and sibling.name.startswith('h'):
                    break
                if hasattr(sibling, 'decompose'):
                    sibling.decompose()
            heading.decompose()
    
    # Extract paragraphs
    paragraphs = content_div.find_all('p')
    content_parts = []
    
    for p in paragraphs:
        text = p.get_text()
        if len(text.strip()) > 50:  # Only substantial paragraphs
            content_parts.append(clean_text(text))
    
    if not content_parts:
        raise ValueError("No substantial content found in article.")
    
    # Join paragraphs with proper spacing
    clean_content = '\n\n'.join(content_parts)
    
    # Limit content length to avoid token limits (roughly 3000 words)
    words = clean_content.split()
    if len(words) > 3000:
        clean_content = ' '.join(words[:3000]) + "..."
    
    return title, clean_content, response.text

def validate_wikipedia_url(url: str) -> bool:
    """Quick validation of Wikipedia URL format"""
    pattern = r'^https://en\.wikipedia\.org/wiki/[^:]+$'
    # Exclude special pages
    if ':' in url.split('/wiki/')[-1]:
        return False
    return bool(re.match(pattern, url))
