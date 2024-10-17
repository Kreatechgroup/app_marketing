import time
import frappe
import requests

def format_phone_number_with_country_code(company, phone_number):
    if "+" in phone_number:
        return phone_number
    else:
        return f"{get_api_key(company, 'country_code')}{phone_number}"

def send_message(**kwargs):
    url = kwargs.get("url", None)
    agent_id = kwargs.get("agent_id", None)
    message = kwargs.get("message", "Prueba")
    mobile_no = kwargs.get("mobile_no", "+50247589219")
    company = kwargs.get("company", "Grupo Creative S.A.")
    is_api = kwargs.get("is_api", False)
    params = kwargs.get("params", [])
    
    if api_key is not None and company is not None:
        api = "https://app.mercately.com/retailers/api/v1/whatsapp/send_message"

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json',
            'api-key': api_key
        }

        obj_payload = {
            "phone_number": format_phone_number_with_country_code(company, mobile_no),
            "message": message
        }

        if is_api:
            api = "https://app.mercately.com/retailers/api/v1/whatsapp/send_notification_by_id"
            obj_payload = {
                "phone_number": format_phone_number_with_country_code(company, mobile_no),
                "internal_id": message,
                "template_params": params
            }
            
        api_url = api
        payload = obj_payload

        if url is not None:
            payload["media_url"] = url

        if agent_id is not None:
            payload["agent_id"] = agent_id

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            print("Respuesta exitosa:")
            print(data)
            time.sleep(5)
        except requests.exceptions.HTTPError as http_err:
            print("Error HTTP:", http_err)
        except Exception as err:
            print("Ocurrió un error:", err)
            recipients = [
                # 'rsoria@creative-latam.com',
                # 'acamargo@creative-latam.com',
                'dmelgar@creative-latam.com'
            ]

            frappe.sendmail(
                recipients=recipients,
                subject=("Ocurrio un error en el envio del recordatorio de al cotizaciones"),
                message=f"Ocurrio un error en el proceso de recordatorio de cotizaciones abiertas: \n{err}",
                header=('🔥 Ocurrio un error en el envio 🔥')
            )

    else:
        print("Se requieren tres argumentos.")

