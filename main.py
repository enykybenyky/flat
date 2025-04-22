import time
import os
import uvicorn
from fastapi import FastAPI
from scraper.homegate import fetch_homegate
from scraper.immospout24 import fetch_immospout24
from scraper.flatfox import fetch_flatfox
from email_utils import send_email
from config import MAX_RENT, ROOMS, LOCATION, CHECK_INTERVAL_MINUTES

app = FastAPI()
seen_links = set()

@app.get("/")
def read_root():
    return {"message": "Aplikace běží. Použijte /search pro hledání bytů."}

@app.get("/search")
def search_flats():
    new_results = []
    sources = [fetch_homegate, fetch_immospout24, fetch_flatfox]

    for fetch in sources:
        listings = fetch(MAX_RENT, ROOMS, LOCATION)
        for flat in listings:
            if flat["link"] not in seen_links:
                seen_links.add(flat["link"])
                new_results.append(flat)

    if new_results:
        send_email("Nové byty k pronájmu", format_result(new_results))
        return {"message": "Nové byty byly nalezeny a odeslány e-mailem.", "flats": new_results}
    else:
        return {"message": "Žádné nové byty nebyly nalezeny."}

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

def run_checker():
    while True:
        check_new_flats()
        time.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    # Spustí kontrolu nových bytů paralelně s FastAPI
    import threading
    threading.Thread(target=run_checker, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

