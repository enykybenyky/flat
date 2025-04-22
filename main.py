
import time
from config import MAX_RENT, ROOMS, LOCATION, CHECK_INTERVAL_MINUTES
from scraper.homegate import fetch_homegate
from scraper.immospout24 import fetch_immospout24
from scraper.flatfox import fetch_flatfox
from email_utils import send_email

seen_links = set()

def format_result(results):
    return "\n\n".join([f"{r['title']} - {r['price']} CHF\n{r['rooms']} rooms\n{r['link']}" for r in results])

def check_new_flats():
    new_results = []
    sources = [fetch_homegate, fetch_immospout24, fetch_flatfox]

    for fetch in sources:
        listings = fetch(MAX_RENT, ROOMS, LOCATION)
        for flat in listings:
            if flat['link'] not in seen_links:
                seen_links.add(flat['link'])
                new_results.append(flat)

    if new_results:
        send_email("Nové byty k pronájmu", format_result(new_results))

if __name__ == "__main__":
    while True:
        check_new_flats()
        time.sleep(CHECK_INTERVAL_MINUTES * 60)
