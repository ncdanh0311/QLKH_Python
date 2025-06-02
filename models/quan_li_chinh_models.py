import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class CustomerModel:
    def __init__(self, data_file='data/customers.json'):
        self.data_file = data_file
        self.customers = []
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.customers = json.load(f)
            else:
                self.customers = []
                self.save_data()
        except Exception as e:
            print(f"Lỗi khi load dữ liệu: {e}")
            self.customers = []
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.customers, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
            return False

    def add_customer(self, customer_data: Dict) -> bool:
        """Thêm khách hàng mới"""
        try:
            self.customers.append({
                'customer_id': customer_data.get('customer_id'),
                'name': customer_data.get('name'),
                'group': customer_data.get('group'),
                'gender': customer_data.get('gender'),
                'phone': customer_data.get('phone'),
                'email': customer_data.get('email'),
                'customer_type': customer_data.get('customer_type'),
                'cmnd': customer_data.get('cmnd'),
                'birth_date': customer_data.get('birth_date'),
                'address': customer_data.get('address'),
                'product': customer_data.get('product'),
                'quantity': customer_data.get('quantity'),
                'unit_price': customer_data.get('unit_price'),
                'total_amount': customer_data.get('total_amount'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            return self.save_data()
        except Exception as e:
            print(f"Lỗi khi thêm khách hàng: {e}")
            return False

    def update_customer(self, customer_id: str, customer_data: Dict) -> bool:
        """Cập nhật thông tin khách hàng dựa theo customer_id"""
        try:
            print("DEBUG - Đang cập nhật customer_id:", customer_id)
            print("DEBUG - Danh sách hiện có:", [c['customer_id'] for c in self.customers])

            for i, customer in enumerate(self.customers):
                if customer['customer_id'] == customer_id:
                    print("✅ Tìm thấy khách hàng. Tiến hành cập nhật...")
                    self.customers[i].update({
                        'name': customer_data.get('name', customer['name']),
                        'group': customer_data.get('group', customer['group']),
                        'gender': customer_data.get('gender', customer['gender']),
                        'phone': customer_data.get('phone', customer['phone']),
                        'email': customer_data.get('email', customer['email']),
                        'customer_type': customer_data.get('customer_type', customer['customer_type']),
                        'cmnd': customer_data.get('cmnd', customer['cmnd']),
                        'birth_date': customer_data.get('birth_date', customer['birth_date']),
                        'address': customer_data.get('address', customer['address']),
                        'product': customer_data.get('product', customer['product']),
                        'quantity': customer_data.get('quantity', customer['quantity']),
                        'unit_price': customer_data.get('unit_price', customer['unit_price']),
                        'total_amount': customer_data.get('total_amount', customer['total_amount']),
                        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    success = self.save_data()
                    print("DEBUG - Kết quả lưu:", success)
                    return success

            print("❌ Không tìm thấy customer_id trong danh sách!")
            return False

        except Exception as e:
            print(f"❌ Lỗi khi cập nhật khách hàng: {e}")
            return False



    def delete_customer(self, customer_id: str) -> bool:
        try:
            self.customers = [c for c in self.customers if c['customer_id'] != customer_id]
            return self.save_data()
        except Exception as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            return False

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        for customer in self.customers:
            if customer['customer_id'] == customer_id:
                return customer
        return None

    def get_all_customers(self) -> List[Dict]:
        return self.customers.copy()

    def search_customers(self, keyword: str) -> List[Dict]:
        keyword = keyword.lower()
        return [
            c for c in self.customers
            if keyword in c['name'].lower() or
               keyword in c['phone'].lower() or
               keyword in c['email'].lower() or
               keyword in c['address'].lower()
        ]

    def get_customer_stats(self) -> Dict:
        total = len(self.customers)
        vip_count = sum(1 for c in self.customers if c.get('customer_type') == 'VIP')
        return {
            'total': total,
            'vip': vip_count,
            'regular': total - vip_count
        }
