import time
import frappe
from datetime import datetime, timedelta

from app_marketing.app_marketing.utilities.send_message import send_message

def get_api_key(company, brand):
    api_key_to_company = {
        "Grupo Creative S.A.": {
            "Abito": {
                "api-key": "a9a594aa7942a3a2a71d2d3f57160af6",
                "tree_url": "https://linktr.ee/abito_",
		        "video_url": "",
                "is_api": True,
            },
            "Plus": {
                "api-key": "4a826b941bfacd0e5cf4e80f026ce4e8",
                "tree_url": "https://linktr.ee/plus_",
		        "video_url": "https://n9.cl/pluslatam",
                "is_api": False,
            },
            "country_code": "+502",
            "test_drive_restriction_amount": 10000
        },
        "Grupo Creative, S.A. / Panamá": {
            "Abito": {
                "api-key": "39b5613f3624188b0d02e96cd36eb0e3",
                "tree_url": "https://linktr.ee/abito_pa",
		        "video_url": "",
                "is_api": False,
            },
            "country_code": "+507",
            "test_drive_restriction_amount": 10000
        }
    }

    try:
        return api_key_to_company[company][brand]
    except KeyError:
        print("No existe esa clave")

def get_message_for_promotion_code(customer_name, cupon, due_date, dicount_percent, is_api = False):
    if is_api:
        random_message = "0c6c8771-d7c7-475d-9c74-c2a3d73de859"
    else:
        messages = [
            f"¡Hola {customer_name}!\n\n¡Has recibido un descuento del {dicount_percent}% en tu próxima compra!\nEste descuento es válido hasta el {due_date}.\n¡Aprovecha esta oferta!\n\nTu código de cupón es: {cupon}."
        ]

        random_index = int(time.time()) % 1

        random_message = messages[random_index]

    return random_message

def valid_coupon():
    return frappe.db.sql("""
            SELECT
                cp.name,
                cp.customer,
                cp.code,
                cp.company,
                cp.brand,
                cp.discount,
                DATE_FORMAT(cp.due_date, "%d-%m-%Y") as due_date,
                cu.mobile_no

            FROM `tabCupon` cp

            INNER JOIN `tabCustomer` cu ON cu.name = cp.customer

            WHERE 
                cp.status = "Activo" AND
                cp.used != 1 AND
                NOT EXISTS (
                    SELECT 
                        *
                    FROM `tabMK_Notifications` mk
                    WHERE 
                        mk.document_reference = "Cupon" AND
                        mk.document = cp.name AND
                        mk.notified = 1
                )
        """, as_dict=True)

def send_promotion_code():
    # Get the valid coupon and iterate through each coupon to send a message to the client.
    for coupon in valid_coupon():
        api_key = get_api_key(coupon["company"], coupon["brand"])["api-key"]
        is_api = get_api_key(coupon["company"], coupon["brand"])["is_api"]
        message = get_message_for_promotion_code(coupon["customer"], coupon["code"], coupon["due_date"], coupon["discount"], is_api)

        # Create a new log of notification with notification type DISCOUNT_COUPON.
        mk_notification = frappe.new_doc("MK_Notifications")

        mk_notification.document_reference = "Cupon"
        mk_notification.document = coupon["name"]
        mk_notification.notified = True
        mk_notification.notification_type = "DISCOUNT_COUPON"

        mk_notification.insert()
        if coupon["company"] == "Grupo Creative, S.A. / Panamá":
            # mobile_no=coupon["mobile_no"]
            send_message(api_key=api_key, message=message, company= coupon["company"], params=[
                    coupon["customer"],
                    coupon["code"],
                    coupon["due_date"],
                    coupon["discount"]
                ]
            )
        else:
            send_message(api_key=api_key, message=message, company= coupon["company"])

