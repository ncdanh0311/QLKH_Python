import sys, os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from controllers.auth_controller import AuthController
from controllers.bat_tat_screen_controller import ScreenController

class RegisterView:
    def __init__(self, root):
        self.root = root
        self.auth_controller = AuthController()
        
        # Cấu hình cửa sổ đăng ký
        self.root.geometry("600x450+640+260")
        self.root.resizable(0, 0)
        self.root.configure(bg="#1a1a2e")
        self.root.title("Quản Lí Khách Hàng - Đăng Ký Tài Khoản")
        
        # Load ảnh (tái sử dụng icon từ login_view)
        self.load_images()
        
        # Xây dựng giao diện đăng ký
        self.build_ui()

    def load_images(self):
        """Load các ảnh cần thiết cho form đăng ký"""
        try:
            email_icon_data = Image.open("assets/images/login/icon_user.png").resize((20, 20))
            password_icon_data = Image.open("assets/images/login/icon_pass.png").resize((20, 20))
            
            self.email_icon = ImageTk.PhotoImage(email_icon_data)
            self.password_icon = ImageTk.PhotoImage(password_icon_data)
            
        except Exception as e:
            print(f"Không thể load ảnh: {e}")
            self.email_icon = None
            self.password_icon = None

    def create_entry(self, parent, icon=None, show=None):
        """Tạo entry đơn giản với style thống nhất"""
        entry_frame = Frame(parent, bg="#2d2d54", bd=1, relief="solid")
        entry_frame.pack(fill="x", pady=5, padx=50)
        
        inner_frame = Frame(entry_frame, bg="#2d2d54")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=8)
        
        if icon:
            icon_label = Label(inner_frame, image=icon, bg="#2d2d54")
            icon_label.pack(side="left", padx=(0, 10))
        
        entry = Entry(inner_frame, font=("Arial", 11), bg="#2d2d54", 
                     fg="#ffffff", bd=0, relief="flat", show=show,
                     insertbackground="#4facfe")
        entry.pack(side="left", fill="both", expand=True)
        
        # Hiệu ứng focus
        def on_focus_in(event):
            entry_frame.config(highlightbackground="#4facfe", highlightthickness=2)
        
        def on_focus_out(event):
            entry_frame.config(highlightbackground="#2d2d54", highlightthickness=1)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry

    def build_ui(self):
        """Xây dựng giao diện đăng ký tài khoản"""
        main_frame = Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True)

        register_card = Frame(main_frame, bg="#16213e", relief="flat", bd=0)
        register_card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=480) 

        form_frame = Frame(register_card, bg="#16213e")
        form_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Tiêu đề
        Label(form_frame, text="Tạo Tài Khoản Mới", 
              font=("Arial", 18, "bold"), 
              fg="#ffffff", bg="#16213e").pack(pady=(0, 20))

        # Username entry
        Label(form_frame, text="Tên đăng nhập:", anchor="w", fg="#ffffff", bg="#16213e", font=("Arial", 9)).pack(fill="x", padx=50)
        self.username_entry = self.create_entry(form_frame, self.email_icon)
        
        # Password entry
        Label(form_frame, text="Mật khẩu:", anchor="w", fg="#ffffff", bg="#16213e", font=("Arial", 9)).pack(fill="x", padx=50, pady=(10,0))
        self.password_entry = self.create_entry(form_frame, self.password_icon, "*")

        # Confirm Password entry
        Label(form_frame, text="Xác nhận mật khẩu:", anchor="w", fg="#ffffff", bg="#16213e", font=("Arial", 9)).pack(fill="x", padx=50, pady=(10,0))
        self.confirm_password_entry = self.create_entry(form_frame, self.password_icon, "*")

        # Role selection (chỉ admin mới có thể tạo tài khoản admin)
        self.role_var = StringVar(value="user") # Mặc định là user
        role_frame = Frame(form_frame, bg="#16213e")
        role_frame.pack(fill="x", pady=10, padx=50)
        Label(role_frame, text="Vai trò:", fg="#ffffff", bg="#16213e", font=("Arial", 9)).pack(side="left")
        
        # Kiểm tra nếu người dùng hiện tại là admin thì mới cho chọn vai trò admin
        # Giả định có một cách để lấy vai trò của người dùng đang đăng nhập (ví dụ: từ AuthController)
        current_user_role = self.auth_controller.get_current_user_role() 
        
        Radiobutton(role_frame, text="User", variable=self.role_var, value="user",
                    bg="#16213e", fg="#ffffff", selectcolor="#16213e", activebackground="#16213e",
                    font=("Arial", 9)).pack(side="left", padx=(10, 0))
        
        if current_user_role == "admin":
            Radiobutton(role_frame, text="Admin", variable=self.role_var, value="admin",
                        bg="#16213e", fg="#ffffff", selectcolor="#16213e", activebackground="#16213e",
                        font=("Arial", 9)).pack(side="left", padx=(10, 0))
        else:
            # Nếu không phải admin, ẩn lựa chọn admin và đảm bảo vai trò là user
            self.role_var.set("user")


        # Nút đăng ký
        register_button = Button(form_frame, text="ĐĂNG KÝ", command=self.handle_register,
                                 bg="#007bff", fg="#ffffff", # Màu xanh dương tươi sáng hơn (Bootstrap primary)
                                 font=("Arial", 12, "bold"),
                                 bd=0, relief="flat", cursor="hand2",
                                 activebackground="#0056b3", activeforeground="#ffffff", # Màu xanh dương đậm hơn khi hover
                                 width=20, height=1)
        register_button.pack(pady=15)

        # Nút quay lại
        back_button = Button(form_frame, text="Quay Lại Đăng Nhập", command=self.go_back_to_login,
                             bg="#4a69bd", fg="#ffffff", # Màu xanh lam nhẹ nhàng (muted blue)
                             font=("Arial", 9),
                             bd=0, relief="flat", cursor="hand2",
                             activebackground="#3b5998", activeforeground="#ffffff") # Màu xanh lam đậm hơn khi hover
        back_button.pack(pady=5)

        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.handle_register())
        
        self.username_entry.focus()

    def handle_register(self):
        """Xử lý logic đăng ký tài khoản"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            self.confirm_password_entry.delete(0, END)
            return

        # Gọi controller để xử lý đăng ký
        success = self.auth_controller.register_user(username, password, role)
        if success:
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            self.go_back_to_login() # Quay lại màn hình đăng nhập sau khi đăng ký thành công
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại hoặc có lỗi khi đăng ký.")

    def go_back_to_login(self):
        """Quay lại màn hình đăng nhập"""
        ScreenController.close_register_screen(self.root)
        ScreenController.open_login_screen()