import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from controllers.auth_controller import AuthController
from views.chon_chuc_nang_view import chon_chuc_nang
from controllers.bat_tat_screen_controller import ScreenController

class LoginView:
    def __init__(self, root):
        self.root = root
        self.auth_controller = AuthController()
        
        # Cấu hình cửa sổ
        self.root.geometry("800x500+540+260")
        self.root.resizable(0, 0)
        self.root.configure(bg="#1a1a2e")
        self.root.title("Quản Lí Khách Hàng - Đăng Nhập")
        
        # Load ảnh
        self.load_images()
        
        # Tạo giao diện
        self.build_ui()
    
    def load_images(self):
        """Load các ảnh cần thiết"""
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
        """Tạo entry đơn giản"""
        entry_frame = Frame(parent, bg="#2d2d54", bd=1, relief="solid")
        entry_frame.pack(fill="x", pady=10, padx=50)
        
        inner_frame = Frame(entry_frame, bg="#2d2d54")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=12)
        
        if icon:
            icon_label = Label(inner_frame, image=icon, bg="#2d2d54")
            icon_label.pack(side="left", padx=(0, 10))
        
        entry = Entry(inner_frame, font=("Arial", 12), bg="#2d2d54", 
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
    
    def create_login_button(self, parent):
        """Tạo nút đăng nhập với gradient"""
        btn_frame = Frame(parent, bg=parent.cget('bg'))
        btn_frame.pack(pady=10)
        
        # Tạo canvas để vẽ gradient
        canvas = Canvas(btn_frame, width=300, height=50)
        canvas.pack()
        button = Button(canvas, text="ĐĂNG NHẬP", command=self.handle_login,
                       bg="#007bff", fg="#ffffff", font=("Arial", 12, "bold"), # Màu nền mặc định
                       bd=0, relief="flat", cursor="hand2",
                       activebackground="#0056b3", activeforeground="#ffffff") # Màu nền khi click
        
        canvas.create_window(150, 25, window=button, width=290, height=45)
        def on_enter(e):
            canvas.delete("all")
            
            for i in range(50):
                ratio = i / 50
                r = int(0 + (0 - 0) * ratio)
                g = int(191 + (154 - 191) * ratio) #
                b = int(255 + (205 - 255) * ratio)
                color = f"#{r:02x}{g:02x}{b:02x}"
                canvas.create_line(0, i, 300, i, fill=color, width=1)
            canvas.create_window(150, 25, window=button, width=290, height=45)
        
        def on_leave(e):
            canvas.delete("all")
            for i in range(50):
                ratio = i / 50
                r = int(0 + (0 - 0) * ratio)
                g = int(123 + (86 - 123) * ratio) 
                b = int(255 + (179 - 255) * ratio)
                color = f"#{r:02x}{g:02x}{b:02x}"
                canvas.create_line(0, i, 300, i, fill=color, width=1)
            canvas.create_window(150, 25, window=button, width=290, height=45)
        
        canvas.bind("<Enter>", on_enter)
        canvas.bind("<Leave>", on_leave)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def build_ui(self):
        """Xây dựng giao diện chính"""
        # Container chính
        main_frame = Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True)
        
        # Card đăng nhập
        login_card = Frame(main_frame, bg="#16213e", relief="flat", bd=0)
        login_card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=520) 
        
        # Phần trái - Welcome (giữ nguyên)
        left_frame = Frame(login_card, bg="#0f3460")
        left_frame.pack(side="left", fill="both", expand=True)
        
        welcome_frame = Frame(left_frame, bg="#0f3460")
        welcome_frame.pack(expand=True)
        
        Label(welcome_frame, text="CHÀO MỪNG", 
              font=("Arial", 24, "bold"), 
              fg="#ffffff", bg="#0f3460").pack(pady=(0, 10))
        
        Label(welcome_frame, text="Hệ Thống Quản Lý Khách Hàng", 
              font=("Arial", 14), 
              fg="#b3d9ff", bg="#0f3460").pack(pady=(0, 5))
        
        Label(welcome_frame, text="tk: admin || pass: 123", 
              font=("Arial", 14), 
              fg="#d38716", bg="#0f3460").pack()
        
        # Tạo logo đơn giản
        logo_canvas = Canvas(welcome_frame, width=60, height=60, bg="#0f3460", highlightthickness=0)
        logo_canvas.pack(pady=20)
        logo_canvas.create_oval(10, 10, 50, 50, fill="#4facfe", outline="#00f2fe", width=2)
        logo_canvas.create_text(30, 30, text="KH", font=("Arial", 16, "bold"), fill="#ffffff")
        
        # Phần phải - Form đăng nhập
        right_frame = Frame(login_card, bg="#16213e")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Container form
        form_frame = Frame(right_frame, bg="#16213e")
        form_frame.pack(expand=True, fill="both", padx=20, pady=40)
        
        # Tiêu đề
        Label(form_frame, text="Đăng Nhập", 
              font=("Arial", 20, "bold"), 
              fg="#ffffff", bg="#16213e").pack(pady=(0, 30))
        
        # Form fields
        fields_frame = Frame(form_frame, bg="#16213e")
        fields_frame.pack(fill="x", pady=20)
        
        # Username entry
        self.user_entry = self.create_entry(fields_frame, self.email_icon)
        
        # Password entry
        self.password_entry = self.create_entry(fields_frame, self.password_icon, "*")
        
        # Nút đăng nhập
        self.login_button = self.create_login_button(fields_frame)
        
        # Checkbox "Nhớ mật khẩu"
        remember_me_frame = Frame(fields_frame, bg="#16213e")
        remember_me_frame.pack(pady=(0, 10), anchor="w", padx=50) 
        
        self.remember_me_var = IntVar()
        remember_me_checkbox = Checkbutton(remember_me_frame, text="Nhớ mật khẩu",
                                           variable=self.remember_me_var,
                                           bg="#16213e", fg="#ffffff",
                                           selectcolor="#16213e", 
                                           activebackground="#16213e", 
                                           font=("Arial", 9))
        remember_me_checkbox.pack(side="left")
        
        # Nút "Tạo tài khoản mới"
        create_account_frame = Frame(fields_frame, bg="#16213e")
        create_account_frame.pack(pady=10) 
        
        create_account_button = Button(create_account_frame, text="Tạo tài khoản mới",
                                       command=self.handle_create_account, 
                                       bg="#28a745", fg="#ffffff", 
                                       font=("Arial", 10, "bold"),
                                       bd=0, relief="flat", cursor="hand2",
                                       activebackground="#218838", activeforeground="#ffffff", # Màu xanh lá cây đậm hơn khi hover
                                       width=25, height=2) 
        create_account_button.pack()
        
        # Footer
        Label(form_frame, text="© 2024 Customer Management System", 
              font=("Arial", 8), 
              fg="#666699", bg="#16213e").pack(side="bottom", pady=(20, 0))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.handle_login())
        
        # Focus vào username
        self.user_entry.focus()
    
    def handle_login(self):
        """Xử lý đăng nhập - giữ nguyên logic backend"""
        username = self.user_entry.get()
        password = self.password_entry.get()
        
        if not username.strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập!")
            self.user_entry.focus()
            return
        
        if not password.strip():
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu!")
            self.password_entry.focus()
            return
        
        self.auth_controller.handle_login(username, password, self.root, self.password_entry)

    def handle_create_account(self):
        """Xử lý khi nhấn nút 'Tạo tài khoản mới' - Mở màn hình đăng ký"""
        ScreenController.close_login_screen(self.root)
        ScreenController.open_register_screen()