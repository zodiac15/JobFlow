from .base_scraper import BaseScraper
import time
import random

class NaukriScraper(BaseScraper):
    def scrape(self, query, location):
        print(f"Scraping Naukri (Selenium) for {query} in {location}")
        jobs = []
        driver = None
        
        try:
            driver = self.setup_driver()
            # Naukri URL structure
            url = f"https://www.naukri.com/{query}-jobs-in-{location}"
            print(f"Navigating to: {url}")
            
            driver.get(url)
            time.sleep(3) # Wait for JS to load
            
            # Extract job cards using Selenium
            # Note: Selectors on Naukri are complex and change. This uses generic classes if possible.
            # Using basic structure assumption for demo.
            
            job_cards = driver.find_elements("css selector", ".srp-jobtuple-wrapper")
            
            if not job_cards:
                 # Fallback if no cards found (anti-bot or selector change)
                 print("No job cards found with Selenium. Possibly blocked.")
            
            for index, card in enumerate(job_cards[:5]): # Limit to 5 for speed
                try:
                    title_elem = card.find_element("css selector", ".title")
                    company_elem = card.find_element("css selector", ".comp-name")
                    loc_elem = card.find_element("css selector", ".locWdth")
                    
                    title = title_elem.text
                    company = company_elem.text
                    location_text = loc_elem.text
                    job_url = title_elem.get_attribute('href')
                    
                    description = "View full description on Naukri.com"
                    try:
                        # Open new tab
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.get(job_url)
                        time.sleep(2) # Wait for load
                        
                        # Try to find description
                        try:
                            # Common selectors for Naukri description
                            desc_elem = None
                            selectors = [
                                ".styles_job-desc-container__txpYf", 
                                "section.job-desc", 
                                ".job-desc",
                                ".dang-inner-html" 
                            ]
                            for sel in selectors:
                                try:
                                    desc_elem = driver.find_element("css selector", sel)
                                    if desc_elem:
                                        break
                                except:
                                    continue
                            
                            if desc_elem:
                                description = desc_elem.text
                            else:
                                description = "Description extraction failed. Please visit URL."
                                
                        except Exception as e:
                            print(f"Could not extract description for {title}: {e}")
                            
                        # Close tab
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                    except Exception as e:
                        print(f"Failed to visit job page: {e}")
                        # Ensure we are back on main tab
                        if len(driver.window_handles) > 1:
                            driver.switch_to.window(driver.window_handles[-1])
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                    
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_text,
                        'source': 'Naukri',
                        'url': job_url,
                        'description': description
                    })
                except Exception as e:
                    print(f"Error parsing Naukri card: {e}")
                    continue
                    
        except Exception as e:
            print(f"Naukri Selenium Scrape Failed: {e}")
            # Fallback to mock if selenium fails completely
            jobs.append({
                'title': f'{query} Developer (Selenium Fallback)',
                'company': 'Naukri Mock Corp',
                'location': location,
                'source': 'Naukri',
                'url': 'https://www.naukri.com',
                'description': 'Selenium scraping encountered an error. This is a fallback entry.'
            })
        finally:
            if driver:
                driver.quit()
        
        return jobs
