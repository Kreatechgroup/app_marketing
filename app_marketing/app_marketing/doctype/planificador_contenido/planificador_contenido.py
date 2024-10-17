# -*- coding: utf-8 -*-
# Copyright (c) 2024, Kreatech Group and contributors
# For license information, please see license.txt

import frappe

from datetime import datetime
from frappe.model.document import Document


class PlanificadorContenido(Document):
    def on_submit(self):
        submit_all_doctypes(self.name)


@frappe.whitelist()
def submit_all_doctypes(doc_name) -> None:
    try:
        doctypes = frappe.get_all("Contenido Posteado", filters={"periodo": doc_name}, fields=["name"])

        for doctype in doctypes:
            doc = frappe.get_doc('Contenido Posteado', doctype.name)
            if doc.docstatus != 1:
                doc.docstatus = 1
                doc.save()

        frappe.msgprint(_("Documentos validados exitosamente."), indicator='green')

    except Exception as e:
        frappe.msgprint(_("Ocurrió un error al enviar documentos. Consulte el registro de errores para más detalles."),
                        indicator='red')


from frappe import _


@frappe.whitelist()
def get_all_content_for_brand_and_type(period: str, brand: str, social_media: str, type_of_content: str):
    try:
        return frappe.db.sql("""
        SELECT
			COUNT(cnt.name) AS count_of_content
		FROM `tabPlanificador Contenido` pc
		INNER JOIN `tabContenido Planificado Tabla` cmpl ON cmpl.parent = pc.name AND cmpl.parenttype = 'Planificador Contenido'
		INNER JOIN `tabContenido Posteado` cmp ON cmp.periodo = pc.name AND cmp.brand = %(brand)s
		INNER JOIN `tabContenido Tabla` cnt ON cnt.parent = cmp.name AND cnt.parenttype = 'Contenido Posteado'
		WHERE
			cmpl.brand = %(brand)s
			AND cmp.periodo = %(period)s
			AND cmpl.type_of_content = %(type_of_content)s
			AND cnt.social_media = %(social_media)s
			AND cmpl.type_of_content = cnt.type_of_content
        """, {'period': period, 'social_media': social_media, 'brand': brand, 'type_of_content': type_of_content},
                             as_dict=True)

    except Exception as e:
        frappe.log_error(
            f"Error en consulta SQL: {str(e)} - Periodo: {period} - Plataforma: {social_media}- brand: {brand} - type_of_content: {type_of_content}")
        frappe.throw(
            _("Ocurrió un error al obtener el conteo de contenido. Consulte el registro de errores para más detalles."))
