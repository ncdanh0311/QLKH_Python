from models.quan_li_chinh_models import CustomerModel  # Đảm bảo đường dẫn đúng

class CustomerController:
    def __init__(self):
        self.model = CustomerModel()

    def get_all_customers(self):
        """Lấy toàn bộ khách hàng"""
        return self.model.get_all_customers()

    def add_customer(self, customer_data):
        """Thêm khách hàng"""
        return self.model.add_customer(customer_data)

    def update_customer(self, customer_id, customer_data):
        """Cập nhật khách hàng"""
        return self.model.update_customer(customer_id, customer_data)

    def delete_customer(self, customer_id):
        """Xóa khách hàng"""
        return self.model.delete_customer(customer_id)

    def search_customers(self, keyword):
        """Tìm kiếm khách hàng"""
        return self.model.search_customers(keyword)

    def get_customer_by_id(self, customer_id):
        """Lấy khách hàng theo ID"""
        return self.model.get_customer_by_id(customer_id)

    def get_stats(self):
        """Thống kê khách hàng"""
        return self.model.get_customer_stats()
