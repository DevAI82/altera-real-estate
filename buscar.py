import os
import sys
import requests

# Forzar codificación UTF-8 en terminales Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "350e9fe98cmshffb3d841c773c02p1f94b9jsnb998be962c89")
RAPIDAPI_HOST = "idealista17.p.rapidapi.com"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def resolver_location_id(zona_texto: str):
    """Resuelve cualquier texto a un locationId válido de Idealista."""
    # 1. Intentar con auto-complete
    try:
        r = requests.get(f"https://{RAPIDAPI_HOST}/auto-complete", headers=headers, params={"location_name": zona_texto, "country": "es"}, timeout=10)
        if r.status_code == 200:
            for l in r.json().get("data", {}).get("locations", []):
                if l.get("locationId"):
                    return l["name"], l["locationId"], l.get("total", 0)
    except Exception:
        pass

    # 2. Intentar con smart-search
    try:
        r = requests.get(f"https://{RAPIDAPI_HOST}/smart-search", headers=headers, params={"search_text": zona_texto, "country": "es", "search_type": "for_sale", "property_type": "homes"}, timeout=10)
        if r.status_code == 200:
            for res in r.json().get("data", {}).get("results", []):
                if res.get("locationId"):
                    return res["name"], res["locationId"], res.get("total", 0)
    except Exception:
        pass

    # 3. Fallback: intentar con la última palabra (ej. "Albacete" en "Ensanche Albacete")
    palabras = zona_texto.strip().split()
    if len(palabras) > 1:
        return resolver_location_id(palabras[-1])

    return None, None, 0

def buscar_inmuebles_en_zona(zona_texto: str, operacion: str = "for_sale", cantidad: int = 5):
    """
    Realiza la búsqueda completa en 2 pasos:
    1. Resuelve la localización a un locationId de Idealista
    2. Obtiene los inmuebles reales con /property-search
    """
    print(f"\n" + "="*70)
    print(f"🔍 BUSCANDO EN IDEALISTA: '{zona_texto}' (Operación: {'Venta' if operacion=='for_sale' else 'Alquiler'})")
    print("="*70)

    print("⏳ Paso 1: Identificando zona oficial en Idealista España...")
    nombre_oficial, location_id, total_inmuebles = resolver_location_id(zona_texto)

    if not location_id:
        print(f"❌ No se pudo resolver '{zona_texto}' a una ubicación oficial de Idealista.")
        return

    print(f"✅ ¡Zona localizada con éxito!")
    print(f"   • Nombre oficial:  {nombre_oficial}")
    print(f"   • Location ID:     {location_id}")
    if total_inmuebles:
        print(f"   • Inmuebles en BD: {total_inmuebles:,} propiedades activas")

    # ----------------------------------------------------
    # PASO 2: Obtener los inmuebles reales (/property-search)
    # ----------------------------------------------------
    print(f"\n⏳ Paso 2: Descargando los {cantidad} primeros inmuebles reales de la zona...")
    search_url = f"https://{RAPIDAPI_HOST}/property-search"
    search_params = {
        "location_ids": location_id,
        "country": "es",
        "search_type": operacion,
        "property_type": "homes",
        "result_count": cantidad
    }

    try:
        res_search = requests.get(search_url, headers=headers, params=search_params, timeout=15)
        if res_search.status_code != 200:
            print(f"❌ Error en property-search: {res_search.status_code} - {res_search.text}")
            return

        data_search = res_search.json()
        listings = data_search.get("data", {}).get("listings", [])

        if not listings:
            print("⚠️ No hay inmuebles disponibles en este momento para los filtros seleccionados.")
            return

        print(f"✅ Se recibieron {len(listings)} inmuebles reales en directo:\n")

        precios_m2 = []
        for idx, item in enumerate(listings, 1):
            precio = item.get("price", 0)
            tamano = item.get("size", 0)
            habs = item.get("rooms", "?")
            banos = item.get("bathrooms", "?")
            titulo = item.get("suggestedTexts", {}).get("title") or item.get("address", "Inmueble")
            url = item.get("url", f"https://www.idealista.com/inmueble/{item.get('propertyCode')}/")
            if not url.startswith("http"):
                url = f"https://www.idealista.com{url}"

            pm2 = round(precio / tamano, 2) if (precio and tamano) else 0
            if pm2:
                precios_m2.append(pm2)

            print(f"[{idx}] {titulo}")
            print(f"    💰 Precio:       {precio:,.0f} €  ({pm2:,.0f} €/m²)" if pm2 else f"    💰 Precio: {precio:,.0f} €")
            print(f"    📐 Superficie:   {tamano} m²  |  🛏 {habs} habs  |  🚿 {banos} baños")
            print(f"    🔗 Ver anuncio:  {url}")
            print("-" * 70)

        if precios_m2:
            media_m2 = sum(precios_m2) / len(precios_m2)
            print(f"\n📊 RESUMEN DE MERCADO EN {nombre_oficial.upper()}:")
            print(f"   • Precio Medio de la muestra:  {media_m2:,.2f} €/m²")
            print(f"   • Precio Mínimo encontrado:    {min(p.get('price', 0) for p in listings):,.0f} €")
            print(f"   • Precio Máximo encontrado:    {max(p.get('price', 0) for p in listings):,.0f} €")
            print("=" * 70)

    except Exception as e:
        print(f"❌ Error de conexión en Paso 2: {e}")

if __name__ == "__main__":
    import sys
    # Si pasa la zona como argumento: python buscar.py "Valencia Ruzafa"
    if len(sys.argv) > 1:
        zona_input = " ".join(sys.argv[1:])
    else:
        print("\n🏠 --- BUSCADOR EN VIVO DE IDEALISTA --- 🏠")
        try:
            zona_input = input("Escribe una zona o ciudad (ej. Albacete, Ruzafa Valencia, Chamberí Madrid): ").strip()
        except EOFError:
            zona_input = "Albacete"
            
    if not zona_input:
        zona_input = "Albacete"
        
    buscar_inmuebles_en_zona(zona_input, operacion="for_sale", cantidad=5)
