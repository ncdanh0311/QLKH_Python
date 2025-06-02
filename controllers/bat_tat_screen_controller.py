from views.chon_chuc_nang_view import chon_chuc_nang
from views.quan_li_chinh_view import CustomerManagementView
import tkinter as tk

class ScreenController:
    @staticmethod
    def close_login_screen(root):
        root.destroy()

    @staticmethod
    def open_main_screen():
        app = chon_chuc_nang()
        app.run()

    @staticmethod
    def close_chuc_nang_screen(window):
        window.destroy()

    @staticmethod
    def open_customer_management_screen(current_window):
        ScreenController.close_chuc_nang_screen(current_window)
        root = tk.Tk()
        view = CustomerManagementView(root)
        view.pack(fill="both", expand=True)
        root.mainloop()
    
    @staticmethod
    def logout_to_login(current_window):
        """Đăng xuất và quay về màn hình login"""
        current_window.destroy()
        root = tk.Tk()
        from views.login_view import LoginView
        login_view = LoginView(root)
        root.mainloop()

    @staticmethod
    def open_register_screen():
        """Mở màn hình đăng ký tài khoản"""
        root = tk.Tk()
        from views.register_view import RegisterView
        register_view = RegisterView(root)
        root.mainloop()

    @staticmethod
    def close_register_screen(root):
        """Đóng màn hình đăng ký tài khoản"""
        root.destroy()

    @staticmethod
    def open_login_screen():
        """Mở lại màn hình login (sau khi đóng màn hình đăng ký)"""
        root = tk.Tk()
        from views.login_view import LoginView
        login_view = LoginView(root)
        root.mainloop()