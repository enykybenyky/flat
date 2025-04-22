import requests

def fetch_flatfox(max_rent, rooms, location):
    url = f"https://api.flatfox.ch/v1/properties?max_price={max_rent}&rooms={','.join(map(str, rooms))}&location={location}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Chyba při načítání dat z Flatfox: {e}")
        return []

    try:
        data = response.json()
        flats = []
        for listing in data.get('listings', []):
            flats.append({
                "title": listing.get('title', 'N/A'),
                "price": listing.get('price', 'N/A'),
                "rooms": listing.get('rooms', 'N/A'),
                "link": listing.get('url', 'N/A')
            })
        return flats
    except ValueError as e:
        print(f"Chyba při zpracování JSON odpovědi: {e}")
        return []