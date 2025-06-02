import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.login_model import LoginModel
from views.chon_chuc_nang_view import chon_chuc_nang
from controllers.bat_tat_screen_controller import ScreenController
from tkinter import messagebox

class AuthController:
    def __init__(self):
        self.login_model = LoginModel()
        self.current_user_role = None # Thêm biến để lưu vai trò của người dùng hiện tại

    def handle_login(self, username, password, root, password_entry):
        username = username.strip()
        password = password.strip()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return False

        if username == "admin" and password == "123":
            print("Đăng nhập thành công với tài khoản ADMIN")
            self.login_model.ensure_data_file_exists() # Đảm bảo file JSON tồn tại
            self.current_user_role = "admin" # Set vai trò
            ScreenController.close_login_screen(root)
            ScreenController.open_main_screen()
            return True

        elif self.login_model.authenticate(username, password):
            print(f"Đăng nhập thành công với tài khoản: {username}")
            self.current_user_role = self.login_model.get_user_role(username) # Lấy vai trò từ model
            ScreenController.close_login_screen(root)
            ScreenController.open_main_screen()
            return True

        else:
            print("Đăng nhập thất bại")
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
            password_entry.delete(0, 'end')
            return False

    def register_user(self, username, password, role="user"):
        """Xử lý logic đăng ký người dùng mới"""
        # Kiểm tra xem tên đăng nhập đã tồn tại chưa
        if self.login_model.get_user_role(username) is not None:
            return False # Tên đăng nhập đã tồn tại

        # Thêm người dùng mới vào model
        success = self.login_model.add_user(username, password, role)
        return success

    def get_current_user_role(self):
        """Trả về vai trò của người dùng hiện tại (nếu có)"""
        # Đây là một giả định đơn giản. Trong ứng dụng thực tế, bạn sẽ cần một cơ chế xác thực
        # và quản lý phiên người dùng phức tạp hơn.
        return self.current_user_role
