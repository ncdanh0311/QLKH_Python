# views/chon_chuc_nang_view.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from views.quan_li_chinh_view import CustomerManagementView
from views.sales_chart_view import SalesChartView  # Import SalesChartView

class chon_chuc_nang:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title("Quản Lí Danh Sách Khách Hàng")
        self.root.configure(bg="#1a1a2e")
        self.setup_ui()
        self.update_time()
        self.fade_in()
    
    def run(self):
        self.root.mainloop()
    
    def handle_logout(self):
        """Xử lý đăng xuất"""
        result = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?")
        if result:
            from controllers.bat_tat_screen_controller import ScreenController
            ScreenController.logout_to_login(self.root)
    
    def open_sales_chart(self):
        """Mở cửa sổ thống kê bán hàng"""
        try:
            sales_view = SalesChartView(parent_window=self.root)
            sales_view.run()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở cửa sổ thống kê: {str(e)}")
    
    def setup_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # HEADER với gradient effect
        header_frame = tk.Frame(self.root, bg="#0f3460", height=100)
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.grid_propagate(False)

        # Header content frame
        header_content = tk.Frame(header_frame, bg="#0f3460")
        header_content.pack(fill="both", expand=True, padx=40, pady=20)

        # Title với icon lớn hơn
        title_frame = tk.Frame(header_content, bg="#0f3460")
        title_frame.pack(side=tk.LEFT, fill="y")

        title_label = tk.Label(
            title_frame,
            text="🏪 QUẢN LÍ DANH SÁCH KHÁCH HÀNG",
            font=("Segoe UI", 28, "bold"),
            fg="#ffffff",
            bg="#0f3460"
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            title_frame,
            text="Manchester United 🔱👹",
            font=("Segoe UI", 12),
            fg="#a8d8ea",
            bg="#0f3460"
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))

        # Time info ở header
        time_frame = tk.Frame(header_content, bg="#0f3460")
        time_frame.pack(side=tk.RIGHT, fill="y", padx=(0, 20))

        self.time_label = tk.Label(
            time_frame, 
            text="🕒 00:00:00", 
            bg="#0f3460", 
            fg="#a8d8ea", 
            font=("Segoe UI", 12, "bold")
        )
        self.time_label.pack(anchor="e")

        self.date_label = tk.Label(
            time_frame, 
            text="📅 01-01-2025", 
            bg="#0f3460", 
            fg="#a8d8ea", 
            font=("Segoe UI", 12, "bold")
        )
        self.date_label.pack(anchor="e", pady=(5, 0))

        # Logout button với hiệu ứng đẹp hơn
        logout_btn = tk.Button(
            time_frame,
            text="🚪 Đăng xuất",
            font=("Segoe UI", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.handle_logout
        )
        logout_btn.pack(anchor="e", pady=(15, 0))
        
        # Hiệu ứng hover cho nút logout
        def on_logout_enter(e):
            logout_btn.configure(bg="#c0392b", relief="raised")
        def on_logout_leave(e):
            logout_btn.configure(bg="#e74c3c", relief="flat")
        
        logout_btn.bind("<Enter>", on_logout_enter)
        logout_btn.bind("<Leave>", on_logout_leave)

        # MAIN CONTENT với background gradient
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=60, pady=40)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Container cho các nút - SỬ DỤNG GRID THAY VÌ PLACE
        buttons_container = tk.Frame(main_frame, bg="#1a1a2e")
        buttons_container.grid(row=0, column=0)
        
        # Configure grid cho buttons_container
        buttons_container.grid_rowconfigure(0, weight=1)
        buttons_container.grid_rowconfigure(1, weight=1)
        buttons_container.grid_columnconfigure(0, weight=1)
        buttons_container.grid_columnconfigure(1, weight=1)

        # Tạo 4 nút với layout 2x2 - PHIÊN BẢN ĐƠN GIẢN VÀ HIỆU QUẢ
        def create_modern_button(parent, text, icon, command, bg_color, hover_color, row, col):
            # Tạo text hiển thị
            button_text = f"{icon}\n\n{text}"
            
            # Tạo button chính
            button = tk.Button(
                parent,
                text=button_text,
                font=("Segoe UI", 18, "bold"),
                width=15,
                height=8,
                bg="#16213e",
                fg="#ffffff",
                activebackground=hover_color,
                activeforeground="#ffffff",
                relief="flat",
                bd=2,
                cursor="hand2",
                command=command,
                wraplength=200
            )
            button.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")
            
            # Hiệu ứng hover
            def on_enter(event):
                button.configure(bg=hover_color, relief="raised", bd=3)
            
            def on_leave(event):
                button.configure(bg="#16213e", relief="flat", bd=2)
            
            def on_click(event):
                button.configure(relief="sunken", bd=1)
                button.after(100, lambda: button.configure(relief="raised", bd=3))
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            button.bind("<Button-1>", on_click)
            
            return button

        # Data cho 4 nút - ĐÃ THAY ĐỔI LỆNH CHO NÚT THỐNG KÊ
        buttons_data = [
            ("Quản Lí Chính", "🏠", self.open_customer_management, "#3498db", "#2980b9", 0, 0),
            ("Thống Kê", "📊", self.open_sales_chart, "#e74c3c", "#c0392b", 0, 1),  # Đã thay đổi command
            ("Đánh Giá Thị Trường", "📈", self.open_market_analysis, "#f39c12", "#e67e22", 1, 0),
            ("Báo Cáo", "📝", self.open_bao_cao, "#27ae60", "#229954", 1, 1)
        ]

        # Tạo các nút
        for text, icon, command, bg_color, hover_color, row, col in buttons_data:
            create_modern_button(buttons_container, text, icon, command, bg_color, hover_color, row, col)

        # FOOTER với gradient
        footer_frame = tk.Frame(self.root, bg="#0f3460", height=50)
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="© 2025 Store Management System - Thực hiện bởi: Kiều Tấn Phát & Ngô Công Danh",
            font=("Segoe UI", 10),
            fg="#a8d8ea",
            bg="#0f3460"
        )
        footer_label.pack(pady=15)

        # Hiệu ứng mờ
        self.root.attributes('-alpha', 0.0)
    def open_market_analysis(self):
        """Mở cửa sổ đánh giá thị trường và ẩn màn hình hiện tại"""
        try:
            # Ẩn cửa sổ hiện tại
            self.root.withdraw()
            
            from views.market_analysis_view import MarketAnalysisView
            
            # Tạo callback để hiển thị lại màn hình chọn chức năng
            def show_main_screen():
                self.root.deiconify()  # Hiển thị lại cửa sổ chính
                
            # Mở market analysis với callback
            market_view = MarketAnalysisView(
                parent_window=self.root, 
                on_back_callback=show_main_screen
            )
            
            # Đặt sự kiện khi đóng cửa sổ market analysis
            market_view.root.protocol("WM_DELETE_WINDOW", lambda: [
                show_main_screen(),  # Hiển thị lại màn hình chính
                market_view.on_closing()  # Đóng cửa sổ market analysis
            ])
            
            market_view.run()
            
        except Exception as e:
            # Nếu có lỗi, hiển thị lại màn hình chính
            self.root.deiconify()
            messagebox.showerror("Lỗi", f"Không thể mở cửa sổ đánh giá thị trường: {str(e)}")
    def open_bao_cao(self):
        """Mở cửa sổ báo cáo tổng hợp"""
        try:
            from views.bao_cao_view import BaoCaoView
            bao_cao_view = BaoCaoView(parent_window=self.root)
            bao_cao_view.run()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở cửa sổ báo cáo: {str(e)}")
    def update_time(self):
        if self.root.winfo_exists():
            current_time = time.strftime("%H:%M:%S")
            current_date = time.strftime("%d-%m-%Y")
            self.time_label.config(text=f"🕒 {current_time}")
            self.date_label.config(text=f"📅 {current_date}")
            self.root.after(1000, self.update_time)

    def fade_in(self):
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            self.root.attributes('-alpha', alpha + 0.03)
            self.root.after(20, self.fade_in)

    def open_customer_management(self):
        from controllers.bat_tat_screen_controller import ScreenController
        ScreenController.open_customer_management_screen(self.root)