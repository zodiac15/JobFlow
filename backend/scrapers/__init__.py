from .linkedin import LinkedInScraper
from .naukri import NaukriScraper
from .foundit import FounditScraper
from .weworkremotely import WeWorkRemotelyScraper
from .instahyre import InstahyreScraper

def get_scrapers():
    return [
        LinkedInScraper(),
        NaukriScraper(),
        FounditScraper(),
        WeWorkRemotelyScraper(),
        InstahyreScraper()
    ]
