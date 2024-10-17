# Copyright (c) 2024, Kreatech Group and contributors
# For license information, please see license.txt

import frappe
import hashlib
from frappe.model.document import Document
from datetime import datetime, timedelta


class Cupon(Document):
	def after_insert(self):
		self.generate_promotional_code()
		self.calculate_due_date()
	
	def calculate_due_date(self):
		today = datetime.today()
		due_date = today + timedelta(days=10)
		self.db_set("due_date", due_date, notify=True)

	def generate_promotional_code(self):
		promotion_code = self.name

		hash_object = hashlib.sha256(promotion_code.encode())
		hash_hex = hash_object.hexdigest()

		truncated_hash = hash_hex[:6]

		if not self.code:
			existing_docs = frappe.get_all("Cupon", filters={"code": str(truncated_hash)}, limit=1)
			if not existing_docs:
				try:
					self.db_set("code", truncated_hash, notify=True)
					# discount = int(truncated_hash, 16) % 20 + 1
					discount = 20
					self.db_set("discount", discount, notify=True)
				except Exception as e:
					frappe.msgprint(f"No se pudo establecer el código promocional: {e}")
			else:
				frappe.msgprint("Código promocional duplicado. Generando uno nuevo.")
				self.generate_promotional_code()
		else:
			frappe.msgprint("El documento ya tiene un código promocional.")

