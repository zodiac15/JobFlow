from scrapers.weworkremotely import WeWorkRemotelyScraper
from scrapers.instahyre import InstahyreScraper

def test_wwr():
    print("Testing WeWorkRemotely...")
    s = WeWorkRemotelyScraper()
    jobs = s.scrape("python", "")
    print(f"WWR Found: {len(jobs)}")
    for j in jobs[:2]:
        print(f" - {j['title']} @ {j['company']}")

def test_instahyre():
    print("\nTesting Instahyre...")
    s = InstahyreScraper()
    jobs = s.scrape("Java", "Bangalore") 
    print(f"Instahyre Found: {len(jobs)}")
    for j in jobs[:2]:
        print(f" - {j['title']} @ {j['company']}")

if __name__ == "__main__":
    test_wwr()
    # test_instahyre() # Commented out to run sequentially if needed or enable both
    pass
