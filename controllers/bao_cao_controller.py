# controllers/bao_cao_controller.py
import json
import os
from datetime import datetime
from collections import defaultdict
from tkinter import messagebox
import logging

class BaoCaoController:
    def __init__(self):
        self.customer_data = []
        self.stats = {}
        self.data_loaded = False
        self.data_file_path = None
        
        # Thiết lập logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_customer_data(self):
        """Tải dữ liệu khách hàng từ file JSON"""
        try:
            # Thử tìm file customer.json trong các thư mục có thể
            possible_paths = [
                'data/customer.json',
                'customer.json',
                '../data/customer.json',
                'assets/customer.json',
                'assets/data/customer.json'
            ]
            
            self.data_loaded = False
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if self._validate_json_data(data):
                            self.customer_data = data
                            self.data_file_path = path
                            self.data_loaded = True
                            self.logger.info(f"✅ Đã tải dữ liệu từ: {path}")
                            break
                        else:
                            self.logger.warning(f"⚠️ File {path} có định dạng không hợp lệ")
            
            if not self.data_loaded:
                self.logger.warning("⚠️ Không tìm thấy file customer.json hợp lệ, sử dụng dữ liệu mẫu")
                self.use_sample_data()
                self.data_loaded = True
            
            # Tính toán thống kê sau khi tải dữ liệu
            self.calculate_all_statistics()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Lỗi khi tải dữ liệu: {e}")
            self.use_sample_data()
            self.calculate_all_statistics()
            return False
    
    def _validate_json_data(self, data):
        """Kiểm tra tính hợp lệ của dữ liệu JSON"""
        if not isinstance(data, list):
            return False
        
        if len(data) == 0:
            return True  # Cho phép dữ liệu rỗng
        
        # Kiểm tra các trường bắt buộc
        required_fields = ['customer_id', 'name']
        for customer in data:
            if not isinstance(customer, dict):
                return False
            for field in required_fields:
                if field not in customer:
                    return False
        
        return True
    
    def use_sample_data(self):
        """Sử dụng dữ liệu mẫu khi không tìm thấy file"""
        self.customer_data = [
            # {
            #     "customer_id": "KH1001",
            #     "name": "Nguyễn Văn An",
            #     "group": "VIP",
            #     "gender": "Nam",
            #     "phone": "0987654321",
            #     "email": "an.nguyen@email.com",
            #     "customer_type": "VIP",
            #     "cmnd": "123456789",
            #     "birth_date": "1990-03-15",
            #     "address": "Hà Nội",
            #     "product": "💻 Laptop Gaming",
            #     "quantity": "2",
            #     "unit_price": "25000000",
            #     "total_amount": "50000000"
            # },
            # {
            #     "customer_id": "KH1002",
            #     "name": "Trần Thị Bình",
            #     "group": "Thường",
            #     "gender": "Nữ",
            #     "phone": "0976543210",
            #     "email": "binh.tran@email.com",
            #     "customer_type": "Thường",
            #     "cmnd": "987654321",
            #     "birth_date": "1985-07-20",
            #     "address": "Hồ Chí Minh",
            #     "product": "📱 Smartphone",
            #     "quantity": "1",
            #     "unit_price": "15000000",
            #     "total_amount": "15000000"
            # },
            # {
            #     "customer_id": "KH1003",
            #     "name": "Lê Văn Cường",
            #     "group": "VIP",
            #     "gender": "Nam",
            #     "phone": "0965432109",
            #     "email": "cuong.le@email.com",
            #     "customer_type": "VIP",
            #     "cmnd": "456789123",
            #     "birth_date": "1992-11-10",
            #     "address": "Đà Nẵng",
            #     "product": "🖥️ PC Desktop",
            #     "quantity": "1",
            #     "unit_price": "35000000",
            #     "total_amount": "35000000"
            # },
            # {
            #     "customer_id": "KH1004",
            #     "name": "Phạm Thị Dung",
            #     "group": "Thường",
            #     "gender": "Nữ",
            #     "phone": "0954321098",
            #     "email": "dung.pham@email.com",
            #     "customer_type": "Thường",
            #     "cmnd": "789123456",
            #     "birth_date": "1988-05-25",
            #     "address": "Hải Phòng",
            #     "product": "⌚ Smartwatch",
            #     "quantity": "2",
            #     "unit_price": "8000000",
            #     "total_amount": "16000000"
            # },
            # {
            #     "customer_id": "KH1005",
            #     "name": "Hoàng Văn Em",
            #     "group": "VIP",
            #     "gender": "Nam",
            #     "phone": "0943210987",
            #     "email": "em.hoang@email.com",
            #     "customer_type": "VIP",
            #     "cmnd": "321654987",
            #     "birth_date": "1995-12-08",
            #     "address": "Cần Thơ",
            #     "product": "🎧 Headphones Premium",
            #     "quantity": "3",
            #     "unit_price": "5000000",
            #     "total_amount": "15000000"
            # }
        ]
        self.data_file_path = None
    
    def clean_amount_value(self, amount):
        """Làm sạch và chuyển đổi giá trị tiền tệ"""
        if not amount:
            return 0
        
        try:
            # Chuyển thành string nếu chưa phải
            amount_str = str(amount).strip()
            
            # Loại bỏ các ký tự không phải số
            cleaned = ''.join(char for char in amount_str if char.isdigit())
            
            return int(cleaned) if cleaned else 0
        except (ValueError, TypeError):
            return 0
    
    def clean_quantity_value(self, quantity):
        """Làm sạch và chuyển đổi giá trị số lượng"""
        if not quantity:
            return 0
        
        try:
            # Chuyển thành string và loại bỏ ký tự không phải số
            qty_str = str(quantity).strip()
            cleaned = ''.join(char for char in qty_str if char.isdigit())
            return int(cleaned) if cleaned else 0
        except (ValueError, TypeError):
            return 0
    
    def calculate_all_statistics(self):
        """Tính toán tất cả các thống kê từ dữ liệu"""
        self.stats = {
            'total_customers': len(self.customer_data),
            'vip_customers': 0,
            'regular_customers': 0,
            'male_customers': 0,
            'female_customers': 0,
            'total_revenue': 0,
            'total_quantity': 0,
            'products': defaultdict(int),
            'regions': defaultdict(int),
            'age_groups': defaultdict(int),
            'monthly_revenue': defaultdict(int),
            'customer_types': defaultdict(int),
            'top_customers': [],
            'revenue_by_region': defaultdict(int),
            'product_revenue': defaultdict(int)
        }
        
        total_revenues = []
        
        for customer in self.customer_data:
            try:
                # Đếm loại khách hàng - sử dụng cả 'customer_type' và 'group'
                customer_type = customer.get('customer_type', customer.get('group', 'Thường'))
                if customer_type.lower() in ['vip', 'VIP']:
                    self.stats['vip_customers'] += 1
                else:
                    self.stats['regular_customers'] += 1
                
                self.stats['customer_types'][customer_type] += 1
                
                # Đếm giới tính
                gender = customer.get('gender', 'Không xác định')
                if gender.lower() in ['nam', 'male']:
                    self.stats['male_customers'] += 1
                elif gender.lower() in ['nữ', 'female', 'nu']:
                    self.stats['female_customers'] += 1
                
                # Tính doanh thu - sử dụng hàm clean_amount_value
                revenue = self.clean_amount_value(customer.get('total_amount', 0))
                self.stats['total_revenue'] += revenue
                
                if revenue > 0:
                    # Lưu thông tin khách hàng với doanh thu để tìm top customers
                    total_revenues.append({
                        'customer_id': customer.get('customer_id', 'N/A'),
                        'name': customer.get('name', 'N/A'),
                        'revenue': revenue,
                        'product': customer.get('product', 'N/A'),
                        'customer_type': customer_type
                    })
                    
                    # Doanh thu theo khu vực
                    region = customer.get('address', 'Không xác định')
                    self.stats['revenue_by_region'][region] += revenue
                    
                    # Doanh thu theo sản phẩm
                    product = customer.get('product', 'Không xác định')
                    self.stats['product_revenue'][product] += revenue
                
                # Đếm số lượng sản phẩm - sử dụng hàm clean_quantity_value
                quantity = self.clean_quantity_value(customer.get('quantity', 0))
                self.stats['total_quantity'] += quantity
                
                # Thống kê sản phẩm
                product = customer.get('product', 'Không xác định')
                self.stats['products'][product] += 1
                
                # Thống kê khu vực
                address = customer.get('address', 'Không xác định')
                self.stats['regions'][address] += 1
                
                # Tính tuổi và nhóm tuổi
                self._calculate_age_group(customer)
                
            except Exception as e:
                self.logger.warning(f"Lỗi khi xử lý khách hàng {customer.get('customer_id', 'N/A')}: {e}")
                continue
        
        # Tìm top 5 khách hàng có doanh thu cao nhất
        self.stats['top_customers'] = sorted(total_revenues, key=lambda x: x['revenue'], reverse=True)[:5]
        
        # Tính toán các chỉ số bổ sung
        self._calculate_additional_metrics()
    
    def _calculate_age_group(self, customer):
        """Tính toán nhóm tuổi của khách hàng"""
        try:
            birth_date = customer.get('birth_date', '')
            if birth_date:
                birth_year = int(birth_date.split('-')[0])
                current_year = datetime.now().year
                age = current_year - birth_year
                
                if age < 25:
                    age_group = "18-24"
                elif age < 35:
                    age_group = "25-34"
                elif age < 45:
                    age_group = "35-44"
                elif age < 55:
                    age_group = "45-54"
                else:
                    age_group = "55+"
                
                self.stats['age_groups'][age_group] += 1
            else:
                self.stats['age_groups']['Không xác định'] += 1
        except (ValueError, IndexError):
            self.stats['age_groups']['Không xác định'] += 1
    
    def _calculate_additional_metrics(self):
        """Tính toán các chỉ số bổ sung"""
        if self.stats['total_customers'] > 0:
            self.stats['avg_revenue_per_customer'] = self.stats['total_revenue'] / self.stats['total_customers']
            self.stats['vip_percentage'] = (self.stats['vip_customers'] / self.stats['total_customers']) * 100
            self.stats['male_percentage'] = (self.stats['male_customers'] / self.stats['total_customers']) * 100
            self.stats['female_percentage'] = (self.stats['female_customers'] / self.stats['total_customers']) * 100
        else:
            self.stats['avg_revenue_per_customer'] = 0
            self.stats['vip_percentage'] = 0
            self.stats['male_percentage'] = 0
            self.stats['female_percentage'] = 0
    
    def get_statistics(self):
        """Trả về thống kê đã tính toán"""
        if not self.data_loaded:
            self.load_customer_data()
        return self.stats.copy()  # Trả về bản sao để tránh thay đổi không mong muốn
    
    def get_customer_data(self):
        """Trả về dữ liệu khách hàng"""
        if not self.data_loaded:
            self.load_customer_data()
        return self.customer_data.copy()  # Trả về bản sao
    
    def get_report_summary(self):
        """Tạo tóm tắt báo cáo"""
        if not self.data_loaded:
            self.load_customer_data()
        
        # Tìm sản phẩm và khu vực hàng đầu
        top_product = 'N/A'
        top_region = 'N/A'
        
        if self.stats['products']:
            top_product = max(self.stats['products'].items(), key=lambda x: x[1])[0]
        
        if self.stats['regions']:
            top_region = max(self.stats['regions'].items(), key=lambda x: x[1])[0]
        
        summary = {
            'report_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'data_source': self.data_file_path or 'Dữ liệu mẫu',
            'total_customers': self.stats['total_customers'],
            'total_revenue': self.stats['total_revenue'],
            'vip_customers': self.stats['vip_customers'],
            'regular_customers': self.stats['regular_customers'],
            'vip_percentage': self.stats.get('vip_percentage', 0),
            'male_customers': self.stats['male_customers'],
            'female_customers': self.stats['female_customers'],
            'total_quantity': self.stats['total_quantity'],
            'top_product': top_product,
            'top_region': top_region,
            'avg_revenue': self.stats.get('avg_revenue_per_customer', 0)
        }
        
        return summary
    
    def export_report_data(self):
        """Xuất dữ liệu báo cáo để sử dụng cho giao diện"""
        if not self.data_loaded:
            self.load_customer_data()
        
        return {
            'customer_data': self.get_customer_data(),
            'statistics': self.get_statistics(),
            'summary': self.get_report_summary(),
            'data_validation': self.validate_data()
        }
    
    def validate_data(self):
        """Kiểm tra tính hợp lệ của dữ liệu"""
        if not self.customer_data:
            return {
                'is_valid': False,
                'message': "Không có dữ liệu khách hàng",
                'details': []
            }
        
        required_fields = ['customer_id', 'name']
        optional_fields = ['phone', 'email', 'address', 'product', 'total_amount']
        
        issues = []
        warnings = []
        
        for i, customer in enumerate(self.customer_data):
            customer_issues = []
            
            # Kiểm tra các trường bắt buộc
            for field in required_fields:
                if field not in customer or not customer[field]:
                    customer_issues.append(f"thiếu trường bắt buộc '{field}'")
            
            # Kiểm tra các trường tùy chọn và cảnh báo nếu thiếu
            for field in optional_fields:
                if field not in customer or not customer[field]:
                    warnings.append(f"Khách hàng {customer.get('customer_id', i+1)} thiếu trường '{field}'")
            
            # Kiểm tra định dạng số điện thoại
            phone = customer.get('phone', '')
            if phone and not phone.replace(' ', '').replace('-', '').isdigit():
                customer_issues.append("số điện thoại không hợp lệ")
            
            # Kiểm tra định dạng email
            email = customer.get('email', '')
            if email and '@' not in email:
                customer_issues.append("email không hợp lệ")
            
            if customer_issues:
                issues.append(f"Khách hàng {customer.get('customer_id', i+1)}: {', '.join(customer_issues)}")
        
        is_valid = len(issues) == 0
        
        return {
            'is_valid': is_valid,
            'message': "Dữ liệu hợp lệ" if is_valid else f"Tìm thấy {len(issues)} lỗi trong dữ liệu",
            'errors': issues,
            'warnings': warnings,
            'total_records': len(self.customer_data),
            'error_count': len(issues),
            'warning_count': len(warnings)
        }
    
    def refresh_data(self):
        """Làm mới dữ liệu từ file"""
        self.data_loaded = False
        self.customer_data = []
        self.stats = {}
        return self.load_customer_data()
    
    def save_data(self, file_path=None):
        """Lưu dữ liệu hiện tại vào file"""
        try:
            save_path = file_path or self.data_file_path or 'data/customer.json'
            
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as file:
                json.dump(self.customer_data, file, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✅ Đã lưu dữ liệu vào: {save_path}")
            return True, f"Dữ liệu đã được lưu vào {save_path}"
            
        except Exception as e:
            error_msg = f"Lỗi khi lưu dữ liệu: {e}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def add_customer(self, customer_data):
        """Thêm khách hàng mới"""
        try:
            # Kiểm tra dữ liệu đầu vào
            required_fields = ['customer_id', 'name']
            for field in required_fields:
                if field not in customer_data or not customer_data[field]:
                    return False, f"Thiếu trường bắt buộc: {field}"
            
            # Kiểm tra trùng ID
            existing_ids = [c.get('customer_id') for c in self.customer_data]
            if customer_data['customer_id'] in existing_ids:
                return False, f"Mã khách hàng {customer_data['customer_id']} đã tồn tại"
            
            # Thêm khách hàng
            self.customer_data.append(customer_data)
            self.calculate_all_statistics()
            
            return True, "Thêm khách hàng thành công"
            
        except Exception as e:
            return False, f"Lỗi khi thêm khách hàng: {e}"
    
    def update_customer(self, customer_id, updated_data):
        """Cập nhật thông tin khách hàng"""
        try:
            for i, customer in enumerate(self.customer_data):
                if customer.get('customer_id') == customer_id:
                    # Cập nhật dữ liệu
                    self.customer_data[i].update(updated_data)
                    self.calculate_all_statistics()
                    return True, "Cập nhật khách hàng thành công"
            
            return False, f"Không tìm thấy khách hàng với ID: {customer_id}"
            
        except Exception as e:
            return False, f"Lỗi khi cập nhật khách hàng: {e}"
    
    def delete_customer(self, customer_id):
        """Xóa khách hàng"""
        try:
            for i, customer in enumerate(self.customer_data):
                if customer.get('customer_id') == customer_id:
                    deleted_customer = self.customer_data.pop(i)
                    self.calculate_all_statistics()
                    return True, f"Đã xóa khách hàng: {deleted_customer.get('name', 'N/A')}"
            
            return False, f"Không tìm thấy khách hàng với ID: {customer_id}"
            
        except Exception as e:
            return False, f"Lỗi khi xóa khách hàng: {e}"