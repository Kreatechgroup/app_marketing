import time
import frappe
from datetime import datetime, timedelta

def get_all_dnan_before_today(min_amount, days_ago_end, days_ago_start):    
    today = datetime.today()
    start_date = today - timedelta(days=days_ago_end)
    end_date = today - timedelta(days=days_ago_start)

    print(f"Fecha de incio: {start_date}")
    print(f"Fecha de incio: {end_date}")

    client_with_dnan = frappe.db.sql("""
     SELECT 
        dnan.customer_name,
        dn.name,
        so.name,
        sinv.name,
        sinv.grand_total,
        CONCAT(
            '[',
                GROUP_CONCAT(
                   DISTINCT JSON_OBJECT(
                        'name', dnan.name,
                        'customer_name', dnan.client_name
                    )
                ),
            ']'
        ) AS acceptance_note
        FROM
            `tabDelivery Note Acceptance Note` dnan
            
        INNER JOIN 
            `tabDelivery Note` dn ON dn.name = dnan.delivery_note
            
        INNER JOIN
            `tabDelivery Note Item` dni ON dni.parent = dn.name
            
        INNER JOIN 
            `tabSales Order` so ON so.name = dni.against_sales_order
            
        INNER JOIN
            `tabSales Order Item` soi ON soi.parent = so.name
            
        INNER JOIN
            `tabSales Invoice Item` sinvi on sinvi.sales_order = so.name
            
        INNER JOIN 
            `tabSales Invoice` sinv ON sinv.name = sinvi.parent
        
       
        LEFT JOIN 
            `tabMK_Notifications` mk ON dnan.name = mk.document
            
        WHERE 
            mk.document IS NULL AND
            dn.docstatus = 1 AND
            dnan.workflow_state = "Completado" AND
            DATE(dnan.creation) BETWEEN %(start_date)s AND %(end_date)s AND
            sinv.grand_total > %(min_amount_to_get_promotion)s
        GROUP BY 
            dnan.client_name
            
        ORDER BY 
            dn.name DESC
    """, values={"start_date": start_date, "end_date": end_date, "min_amount_to_get_promotion": min_amount}, as_dict=True)

    return client_with_dnan

def generate_new_cupon():

    dnan_completed = get_all_dnan_before_today(20000, 7, 14)

    for dnan in dnan_completed:
        new_cupon = frappe.new_doc({
            "Company": "Grupo Creative S.A.",
            "Customer": dnan.customer_name
        })

        new_cupon.insert()