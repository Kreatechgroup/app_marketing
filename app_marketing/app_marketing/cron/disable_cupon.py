import frappe

def get_all_coupon():
    return frappe.db.sql("""
        SELECT 
            name,
            due_date,
            discount,
            status
        FROM 
            `tabCupon`
        WHERE 
            status = 'Activo' AND
            CURDATE() > due_date;
    """, as_dict=True)

def change_status_of_coupon():
    coupon_with_status_active_past_due_date = get_all_coupon()
    for coupon in coupon_with_status_active_past_due_date:
        get_coupon = frappe.get_doc("Cupon", coupon.name)
        get_coupon.status = "Deshabilitado"
        get_coupon.save()


