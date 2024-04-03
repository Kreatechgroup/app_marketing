import time
import frappe
from datetime import datetime, timedelta

def get_message_for_promotion_code(customer_name, cupon, due_date, dicount_percent):
    messages = [
        f"¡Hola {customer_name}!\n¡Has recibido un descuento del {dicount_percent}% en tu próxima compra! Este descuento es válido hasta el {due_date}. ¡Aprovecha esta oferta!\n\nTu código de cupón es: *{cupon}*."
    ]

    random_index = int(time.time()) % 1

    random_message = messages[random_index]

    return random_index

