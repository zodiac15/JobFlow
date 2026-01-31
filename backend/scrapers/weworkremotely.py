from .base_scraper import BaseScraper
import time
from selenium.webdriver.common.by import By

class WeWorkRemotelyScraper(BaseScraper):
    def scrape(self, query, location):
        print(f"Scraping WeWorkRemotely (Selenium) for {query}...")
        jobs = []
        driver = None
        
        try:
            driver = self.setup_driver()
            url = f"https://weworkremotely.com/remote-jobs/search?term={query}"
            driver.get(url)
            time.sleep(3)
            
            # WWR structure
            job_rows = driver.find_elements(By.CSS_SELECTOR, "li.feature")
            if not job_rows:
                job_rows = driver.find_elements(By.XPATH, "//section[@class='jobs']//li")
            
            print(f"Found {len(job_rows)} rows via Selenium")
            
            for row in job_rows[:10]:
                try:
                    # Filter out "view all" buttons
                    if "view-all" in row.get_attribute("class"):
                        continue
                        
                    anchors = row.find_elements(By.TAG_NAME, "a")
                    if not anchors: continue
                    
                    # Usually the last anchor wraps the content
                    link_elem = anchors[-1]
                    job_url = link_elem.get_attribute("href")
                    
                    try:
                        title_elem = row.find_element(By.CSS_SELECTOR, "span.title")
                    except:
                         # Fallback for WWR new design
                         title_elem = row.find_element(By.TAG_NAME, "span")
                    
                    try:
                        company_elem = row.find_element(By.CSS_SELECTOR, "span.company")
                    except:
                        company_elem = row.find_element(By.TAG_NAME, "small") # Guess
                        
                    try:
                        loc_elem = row.find_element(By.CSS_SELECTOR, "span.region")
                        location_text = loc_elem.text
                    except:
                        location_text = "Remote"
                    
                    # Debug print removed for clean run
                    jobs.append({
                        'title': title_elem.text,
                        'company': company_elem.text,
                        'location': location_text,
                        'source': 'WeWorkRemotely',
                        'url': job_url,
                        'description': f"Apply at {company_elem.text}"
                    })
                except Exception as e:
                    print(f"DEBUG: Row parse failed: {e}")
                    continue
                    
        except Exception as e:
            print(f"WWR Selenium Failed: {e}")
        finally:
            if driver: driver.quit()
        
        return jobs
