import requests

def fetch_immospout24(max_rent, rooms, location):
    url = f"https://api.immoscout24.com/v1/search?location={location}&max_price={max_rent}&rooms={rooms}"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"  # Nahraď klíčem API
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        flats = []
        for listing in data['listings']:
            flats.append({
                "title": listing['title'],
                "price": listing['price'],
                "rooms": listing['rooms'],
                "link": listing['link']
            })
        return flats
    else:
        return []
