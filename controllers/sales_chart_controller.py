import json
import os
from collections import defaultdict
from tkinter import messagebox

class SalesChartController:
    def __init__(self):
        self.data = []

    def load_data(self):
        """Đọc dữ liệu từ customers.json"""
        try:
            if os.path.exists("customers.json"):
                with open("customers.json", 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy file customers.json")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file customers.json:\n{str(e)}")

    def process_data(self):
        """Xử lý và thống kê số lượng bán theo sản phẩm"""
        product_stats = defaultdict(int)

        for item in self.data:
            if item.get('product') and item.get('quantity'):
                try:
                    product_name = item['product'].strip()
                    quantity = int(str(item['quantity']).replace(',', ''))
                    product_stats[product_name] += quantity
                except (ValueError, TypeError):
                    continue

        return product_stats
