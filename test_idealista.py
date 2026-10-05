import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "350e9fe98cmshffb3d841c773c02p1f94b9jsnb998be962c89")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "idealista17.p.rapidapi.com")

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def smart_search(query="Salamanca, Madrid"):
    url = f"https://{RAPIDAPI_HOST}/smart-search"
    params = {
        "search_text": query,
        "country": "es",
        "search_type": "for_sale",
        "property_type": "homes"
    }
    response = requests.get(url, headers=headers, params=params, timeout=15)
    if response.status_code == 200:
        return response.json()
    return None

def property_search(location_id, result_count=10):
    url = f"https://{RAPIDAPI_HOST}/property-search"
    params = {
        "location_ids": location_id,
        "country": "es",
        "search_type": "for_sale",
        "property_type": "homes",
        "result_count": result_count
    }
    response = requests.get(url, headers=headers, params=params, timeout=15)
    if response.status_code == 200:
        return response.json()
    print("Error search:", response.status_code, response.text)
    return None

if __name__ == "__main__":
    print("1. Buscando zona 'Salamanca, Madrid'...")
    res_smart = smart_search("Salamanca, Madrid")
    results = res_smart.get("data", {}).get("results", [])
    if results:
        loc = results[0]
        print(f"-> Zona: {loc['name']} | ID: {loc['locationId']} | Total inmuebles: {loc['total']}")
        
        print("\n2. Obteniendo testigos reales del mercado...")
        res_props = property_search(loc['locationId'], result_count=5)
        if res_props:
            items = res_props.get("data", {}).get("listings", [])
            print(f"Total listados recibidos: {len(items)}\n")
            precios_m2 = []
            for idx, p in enumerate(items, 1):
                price = p.get("price")
                size = p.get("size")
                rooms = p.get("rooms")
                title = p.get("suggestedTexts", {}).get("title", "")
                m2_price = round(price / size, 2) if price and size else 0
                if m2_price:
                    precios_m2.append(m2_price)
                print(f"[{idx}] {price:,.0f} € | {size} m² | {rooms} habs | {m2_price:,.0f} €/m² | {title}")
            
            if precios_m2:
                media_m2 = sum(precios_m2) / len(precios_m2)
                print(f"\n=======================================================")
                print(f"-> PRECIO MEDIO EN LA ZONA: {media_m2:,.2f} €/m²")
                print(f"=======================================================")
    else:
        print("No se encontraron resultados.")
