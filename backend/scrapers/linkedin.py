from .base_scraper import BaseScraper
import urllib.parse
import time
import random

class LinkedInScraper(BaseScraper):
    def scrape(self, query, location):
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        params = {
            'keywords': query,
            'location': location
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        print(f"Scraping LinkedIn: {url}")
        
        soup = self.get_soup(url)
        jobs = []
        
        if not soup:
            return jobs

        job_cards = soup.find_all('li')

        for card in job_cards:
            try:
                title_tag = card.find('h3', class_='base-search-card__title')
                company_tag = card.find('h4', class_='base-search-card__subtitle')
                location_tag = card.find('span', class_='job-search-card__location')
                link_tag = card.find('a', class_='base-card__full-link')
                date_tag = card.find('time', class_='job-search-card__listdate')

                if title_tag and link_tag:
                    job_url = link_tag['href']
                    description = self.scrape_description(job_url)
                    
                    jobs.append({
                        'title': title_tag.text.strip(),
                        'company': company_tag.text.strip() if company_tag else 'Unknown',
                        'location': location_tag.text.strip() if location_tag else 'Unknown',
                        'source': 'LinkedIn',
                        'url': job_url,
                        'description': description or "View full details on LinkedIn."
                    })
                    # Be polite to the server
                    time.sleep(random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"Error parsing job card: {e}")
                continue
                
        return jobs

    def scrape_description(self, url):
        try:
            print(f"Fetching description for: {url}")
            soup = self.get_soup(url)
            if not soup:
                return None
            
            # LinkedIn guest view description container
            description_div = soup.find('div', class_='show-more-less-html__markup')
            if description_div:
                 # Convert HTML to basic text/markdown or keep HTML
                 # For safety, let's keep text but structured
                 return description_div.get_text(separator='\n').strip()
            return None
        except Exception:
            return None
