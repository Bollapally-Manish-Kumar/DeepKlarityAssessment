"""Wikipedia scraping service using BeautifulSoup."""
import requests
from bs4 import BeautifulSoup, Tag
from typing import Dict, List, Optional, Tuple
import re
from urllib.parse import urlparse


class WikipediaScraper:
    """Service for scraping Wikipedia articles."""
    
    # Headers to mimic a browser request
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def validate_url(self, url: str) -> bool:
        """Validate that the URL is a valid Wikipedia article URL."""
        try:
            parsed = urlparse(url)
            if not parsed.netloc.endswith("wikipedia.org"):
                return False
            if "/wiki/" not in parsed.path:
                return False
            special_prefixes = ["Special:", "File:", "Category:", "Template:", "Talk:", "User:", "Wikipedia:", "Help:", "Portal:"]
            article_name = parsed.path.split("/wiki/")[-1]
            for prefix in special_prefixes:
                if article_name.startswith(prefix):
                    return False
            return True
        except Exception:
            return False
    
    def fetch_article(self, url: str) -> Tuple[str, BeautifulSoup]:
        """Fetch and parse a Wikipedia article."""
        if not self.validate_url(url):
            raise ValueError(f"Invalid Wikipedia URL: {url}")
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        return response.text, soup
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the article title."""
        title_elem = soup.find("h1", {"id": "firstHeading"})
        if title_elem:
            return title_elem.get_text(strip=True)
        
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            return title.replace(" - Wikipedia", "").strip()
        
        return "Unknown Title"
    
    def extract_summary(self, soup: BeautifulSoup) -> str:
        """Extract the article summary (first few paragraphs)."""
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return ""
        
        parser_output = content_div.find("div", {"class": "mw-parser-output"})
        if not parser_output:
            return ""
        
        summary_parts = []
        for elem in parser_output.find_all("p", limit=10):
            if isinstance(elem, Tag):
                text = elem.get_text(strip=True)
                if text and len(text) > 50:
                    summary_parts.append(text)
                    if len(summary_parts) >= 2:
                        break
        
        return " ".join(summary_parts)
    
    def extract_sections(self, soup: BeautifulSoup) -> List[str]:
        """Extract section headings from the article."""
        sections = []
        excluded = ["See also", "References", "External links", "Notes", "Further reading", "Bibliography"]
        
        for heading in soup.find_all("h2"):
            if isinstance(heading, Tag):
                span = heading.find("span", {"class": "mw-headline"})
                if span and isinstance(span, Tag):
                    section_name = span.get_text(strip=True)
                    if section_name not in excluded:
                        sections.append(section_name)
        
        return sections
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        """Extract the main text content of the article."""
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return ""
        
        parser_output = content_div.find("div", {"class": "mw-parser-output"})
        if not parser_output:
            return ""
        
        # Collect text without modifying the soup
        text_parts = []
        stop_sections = {"See also", "References", "External links", "Notes", "Further reading", "Bibliography"}
        stop_found = False
        
        for elem in parser_output.find_all(["p", "h2", "h3", "li"]):
            if not isinstance(elem, Tag):
                continue
            
            # Check if we've hit a stop section
            if elem.name == "h2":
                span = elem.find("span", {"class": "mw-headline"})
                if span and isinstance(span, Tag):
                    heading_text = span.get_text(strip=True)
                    if heading_text in stop_sections:
                        stop_found = True
                        break
            
            # Skip if we're past stop sections
            if stop_found:
                break
            
            text = elem.get_text(strip=True)
            if text and len(text) > 20:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def extract_entities(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract key entities from the article using simple heuristics."""
        entities = {
            "people": [],
            "organizations": [],
            "locations": []
        }
        
        try:
            # Extract from infobox
            infobox = soup.find("table", {"class": re.compile(r"infobox")})
            if infobox and isinstance(infobox, Tag):
                links = list(infobox.find_all("a"))[:50]
                for link in links:
                    if not isinstance(link, Tag):
                        continue
                    href = link.get("href")
                    if not href or not isinstance(href, str):
                        continue
                    text = link.get_text(strip=True)
                    if not text or len(text) < 3:
                        continue
                    
                    href_lower = href.lower()
                    if any(kw in href_lower for kw in ["university", "institute", "company", "organization", "corporation"]):
                        if text not in entities["organizations"] and len(entities["organizations"]) < 5:
                            entities["organizations"].append(text)
                    elif any(kw in href_lower for kw in ["country", "city", "state", "kingdom", "republic"]):
                        if text not in entities["locations"] and len(entities["locations"]) < 5:
                            entities["locations"].append(text)
            
            # Extract from content
            content_soup = soup.find("div", {"class": "mw-parser-output"})
            if content_soup and isinstance(content_soup, Tag):
                links = list(content_soup.find_all("a"))[:100]
                for link in links:
                    if not isinstance(link, Tag):
                        continue
                    href = link.get("href")
                    if not href or not isinstance(href, str):
                        continue
                    if not href.startswith("/wiki/"):
                        continue
                    
                    text = link.get_text(strip=True)
                    if not text or len(text) < 3:
                        continue
                    
                    # Skip dates
                    if re.match(r"^\d+$", text) or re.match(r"^\w+\s+\d+", text):
                        continue
                    
                    href_lower = href.lower()
                    if any(kw in href_lower for kw in ["_university", "_college", "_institute", "_company", "_corporation"]):
                        if text not in entities["organizations"] and len(entities["organizations"]) < 5:
                            entities["organizations"].append(text)
                    elif any(kw in href_lower for kw in ["_country", "_city", "_state", "united_kingdom", "united_states"]):
                        if text not in entities["locations"] and len(entities["locations"]) < 5:
                            entities["locations"].append(text)
        except Exception:
            pass
        
        return entities
    
    def scrape(self, url: str) -> Dict:
        """Scrape a Wikipedia article and return structured data."""
        raw_html, soup = self.fetch_article(url)
        
        title = self.extract_title(soup)
        summary = self.extract_summary(soup)
        sections = self.extract_sections(soup)
        entities = self.extract_entities(soup)
        content = self.extract_content(soup)
        
        return {
            "url": url,
            "title": title,
            "summary": summary,
            "sections": sections,
            "content": content,
            "key_entities": entities,
            "raw_html": raw_html
        }


# Singleton instance
scraper = WikipediaScraper()


def scrape_wikipedia(url: str) -> Dict:
    """Convenience function to scrape a Wikipedia article."""
    return scraper.scrape(url)
