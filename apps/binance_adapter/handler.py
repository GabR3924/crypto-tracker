import requests
import json
import urllib3

from decimal import Decimal
import sys
sys.path.append("C:/Users/garc2/OneDrive/Escritorio/crypto tracker")
from .db_handler import save_data
from datetime import datetime

# Desactivar temporalmente las advertencias de solicitud insegura si estás en un entorno de prueba
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL para obtener anuncios P2P
url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def obtener_anuncios(asset, fiat, trade_type, cantidad_min_deseada=None):
    anuncios = []
    page = 1

    while len(anuncios) < 5:
        payload = {
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type,
            "page": page,
            "rows": 5,
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)

            if response.status_code == 200:
                data = response.json()
                
                if not data.get("data"):
                    break

                for adv in data.get("data", []):
                    advert_info = adv.get("adv", {})
                    advertiser_info = adv.get("advertiser", {})
                    
                    # Extraer información relevante
                    precio = Decimal(advert_info.get("price", "0")).quantize(Decimal('0.001'))
                    cantidad_min = float(advert_info.get("minSingleTransAmount", 0))
                    metodos_pago = [
                        str(payment.get("tradeMethodName") or "") 
                        for payment in advert_info.get("tradeMethods", [])
                    ]
                    metodos_pago_str = ", ".join(metodos_pago)

                    
                    # Filtrar solo los anuncios si cantidad_min_deseada tiene valor
                    if cantidad_min_deseada is None or cantidad_min == cantidad_min_deseada:
                        anuncio = {
                            "id": advert_info.get("advNo", ""),
                            "precio": precio,
                            "cantidad_min": cantidad_min,
                            "metodos_pago": metodos_pago,
                            "metodos_pago_str": metodos_pago_str,
                            "vendedor": advertiser_info.get("nickName", ""),
                            "completadas": advertiser_info.get("completedOrderNum", 0),
                            "porcentaje": advertiser_info.get("finishRate", 0)
                        }
                        
                        anuncios.append(anuncio)
                    
                if len(anuncios) < 5:
                    page += 1
                else:
                    break
            else:
                print(f"Error {response.status_code}: {response.text}")
                break
        except Exception as e:
            print(f"Error al hacer la solicitud: {e}")
            break

    return anuncios

class BinanceHandler:
    def __init__(self):
        pass
    
    def fetch_advertisements(self, trade_type, asset="USDT", fiat="VES", cantidad_min_deseada=None):
        anuncios = obtener_anuncios(asset, fiat, trade_type, cantidad_min_deseada)
        prices = [adv['precio'] for adv in anuncios if 'precio' in adv]
        
        # Mostrar los anuncios con sus detalles
        self.mostrar_anuncios(anuncios, trade_type)
        
        return prices, anuncios

    def mostrar_anuncios(self, anuncios, tipo):
        """Muestra los detalles de cada anuncio"""
        print(f"\n=== Detalles de los anuncios {tipo} ===")
        for i, adv in enumerate(anuncios, start=1):
            print(f"{i}. Vendedor: {adv['vendedor']}")
            print(f"   Precio: {adv['precio']} VES")
            print(f"   Cantidad mínima: {adv['cantidad_min']} USDT")
            print(f"   Métodos de pago: {adv['metodos_pago_str']}\n")
            
    def enviar_datos(self, compra, venta, ganancia, origen='binance'):
        """Envía datos calculados a la base de datos"""
        try:
            save_data(compra, venta, ganancia, origen)
            print("✅ Datos guardados correctamente en la base de datos.")
        except Exception as e:
            print(f"❌ Error al guardar datos en la base de datos: {e}")
