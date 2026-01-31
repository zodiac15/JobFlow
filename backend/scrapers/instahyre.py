from .base_scraper import BaseScraper
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class InstahyreScraper(BaseScraper):
    def scrape(self, query, location):
        print(f"Scraping Instahyre (Selenium) for {query}...")
        jobs = []
        driver = None
        
        try:
            driver = self.setup_driver()
            # Instahyre search URL
            # Note: Instahyre uses /search-jobs?job_type=...&query=...
            # but simpler entry is via main search or constructed URL
            # Example: https://www.instahyre.com/search-jobs/?string=python&location=Remote
            
            url = f"https://www.instahyre.com/search-jobs/?string={query}&location={location}"
            print(f"Navigating to: {url}")
            
            driver.get(url)
            time.sleep(5) # Wait for SPA load
            
            # Instahyre Job Cards
            # Selector: .employer-row or .job-row
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".employer-block")
            
            if not job_cards:
                 # Try alternative ID or class
                 job_cards = driver.find_elements(By.ID, "employer-profile-opportunity")
            
            print(f"Found {len(job_cards)} potential cards on Instahyre")
            
            for index, card in enumerate(job_cards[:8]):
                try:
                    # Extract Data
                    # Title: h6.candidate-job-profile-heading
                    # Company: .employer-name
                    
                    title_elem = card.find_element(By.CSS_SELECTOR, ".position-link")
                    company_elem = card.find_element(By.CSS_SELECTOR, ".company-name")
                    
                    title = title_elem.text
                    company = company_elem.text
                    job_url = title_elem.get_attribute('href')
                    
                    # Location
                    # Often in .job-locations
                    try:
                        loc_elem = card.find_element(By.CSS_SELECTOR, ".job-locations")
                        location_text = loc_elem.text
                    except:
                        location_text = location
                    
                    # Description - Visit for full details or grab snippet
                    # Since we are already in Selenium, let's grab snippet or visit
                    description = "View on Instahyre"
                    
                    # Optional: Visit page logic (omitted for speed in this iteration, similar to Naukri)
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_text,
                        'source': 'Instahyre',
                        'url': job_url,
                        'description': description
                    })
                except Exception as e:
                    # print(f"Error parsing Instahyre card: {e}")
                    continue
                    
        except Exception as e:
            print(f"Instahyre Scrape Failed: {e}")
        finally:
            if driver:
                driver.quit()
        
        return jobs
