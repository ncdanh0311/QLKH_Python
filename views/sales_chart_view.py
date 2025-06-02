# views/sales_chart_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import json
from collections import Counter
import os

class SalesChartView:
    def __init__(self, parent_window=None, json_data=None):
        
        self.parent_window = parent_window
        self.json_data = json_data  # Nhận dữ liệu trực tiếp
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title("Thống Kê Sản Phẩm Bán Chạy")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")
        
        # Biến để lưu loại biểu đồ hiện tại
        self.current_chart_type = "column"
        
        # Đặt cửa sổ ở giữa màn hình
        self.center_window()
        
        self.setup_ui()
        self.load_real_data()
        self.create_chart()
    
    def center_window(self):
        """Đặt cửa sổ ở giữa màn hình"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Header
        header_frame = tk.Frame(self.root, bg="#0f3460", height=80)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="📊 THỐNG KÊ SAN PHẨM BÁN CHẠY",
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#0f3460"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg="#16213e", height=80)
        control_frame.pack(fill="x", pady=(0, 10))
        control_frame.pack_propagate(False)
        
        # Buttons và controls trong control panel
        btn_frame = tk.Frame(control_frame, bg="#16213e")
        btn_frame.pack(pady=15)
        
        # Label cho loại biểu đồ
        chart_label = tk.Label(
            btn_frame,
            text="Loại biểu đồ:",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#16213e"
        )
        chart_label.pack(side="left", padx=(0, 10))
        
        # Buttons cho các loại biểu đồ
        column_btn = tk.Button(
            btn_frame,
            text="📊 Biểu đồ cột",
            font=("Segoe UI", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda: self.change_chart_type("column")
        )
        column_btn.pack(side="left", padx=(0, 5))
        
        pie_btn = tk.Button(
            btn_frame,
            text="🥧 Biểu đồ tròn",
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda: self.change_chart_type("pie")
        )
        pie_btn.pack(side="left", padx=(0, 5))
        
        bar_btn = tk.Button(
            btn_frame,
            text="📈 Biểu đồ ngang",
            font=("Segoe UI", 11, "bold"),
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda: self.change_chart_type("bar")
        )
        bar_btn.pack(side="left", padx=(0, 20))
        
        
        
        # Nút đóng
        close_btn = tk.Button(
            btn_frame,
            text="❌ Đóng",
            font=("Segoe UI", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.close_window
        )
        close_btn.pack(side="right")
        
        # Chart container
        self.chart_frame = tk.Frame(main_frame, bg="#1a1a2e")
        self.chart_frame.pack(fill="both", expand=True)
    
    
    def load_real_data(self):
        """Tải dữ liệu thực từ JSON"""
        try:
            # Nếu đã có dữ liệu được truyền vào
            if self.json_data:
                sales_data = self.json_data
            else:
                # Thử đọc từ các đường dẫn có thể
                sales_data = self.try_load_from_files()
            
            if not sales_data:
                # Nếu không có dữ liệu, tạo dữ liệu mẫu
                self.load_sample_data()
                return
            
            # Xử lý dữ liệu sản phẩm
            product_quantities = Counter()
            
            for record in sales_data:
                # Đếm số lượng sản phẩm
                product = record.get('product', 'Không xác định')
                quantity = 0
                
                # Xử lý quantity có thể là string hoặc int
                qty_str = record.get('quantity', '0')
                try:
                    if isinstance(qty_str, str):
                        quantity = int(qty_str.replace(',', ''))
                    else:
                        quantity = int(qty_str)
                except (ValueError, TypeError):
                    quantity = 0
                
                if quantity > 0:
                    product_quantities[product] += quantity
            
            # Lấy tất cả sản phẩm có bán (hoặc top 10 nếu quá nhiều)
            if len(product_quantities) > 10:
                top_products = product_quantities.most_common(10)
            else:
                top_products = list(product_quantities.items())
            
            if top_products:
                self.product_data = {
                    'products': [product for product, _ in top_products],
                    'quantities': [quantity for _, quantity in top_products]
                }
            else:
                self.load_sample_data()
                
        except Exception as e:
            print(f"Lỗi khi xử lý dữ liệu: {e}")
            self.load_sample_data()
    
    def try_load_from_files(self):
        """Thử đọc dữ liệu từ các file có thể"""
        possible_paths = [
            "data/customers.json",
            "customers.json", 
            "../data/customers.json",
            "data.json",
            "sales_data.json",
            "paste-2.txt"  # File được paste
        ]
        
        for file_path in possible_paths:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        # Nếu file bắt đầu bằng [, đó là JSON array
                        if content.startswith('['):
                            return json.loads(content)
                        # Nếu file bắt đầu bằng {, đó là JSON object
                        elif content.startswith('{'):
                            return [json.loads(content)]
            except Exception as e:
                print(f"Không thể đọc file {file_path}: {e}")
                continue
        
        return None
    
    def load_sample_data(self):
        """Tạo dữ liệu mẫu nếu không đọc được file"""
        self.product_data = {
            'products': ['💻 Laptop Gaming', '📱 iPhone 15 Pro', '🖥️ iMac 27"', '⌚ Apple Watch', '📷 Canon EOS M50', '🎧 AirPods Pro'],
            'quantities': [7, 2, 3, 6, 2, 2]
        }
    
    def change_chart_type(self, chart_type):
        """Thay đổi loại biểu đồ"""
        self.current_chart_type = chart_type
        self.create_chart()
    
    def create_chart(self):
        """Tạo biểu đồ theo loại được chọn"""
        # Xóa biểu đồ cũ
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if self.current_chart_type == "column":
            self.create_column_chart()
        elif self.current_chart_type == "pie":
            self.create_pie_chart()
        elif self.current_chart_type == "bar":
            self.create_bar_chart()
    
    def create_column_chart(self):
        """Tạo biểu đồ cột"""
        # Tạo figure và axis
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="#1a1a2e")
        ax.set_facecolor("#16213e")
        
        # Màu sắc cho từng cột
        colors = ['#e74c3c', '#3498db', '#f39c12', '#27ae60', '#9b59b6', '#34495e', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
        
        # Vẽ biểu đồ cột
        bars = ax.bar(self.product_data['products'], 
                     self.product_data['quantities'],
                     color=colors[:len(self.product_data['products'])], alpha=0.8)
        
        # Thêm giá trị lên đầu mỗi cột
        for bar, qty in zip(bars, self.product_data['quantities']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(self.product_data['quantities'])*0.01,
                   f'{qty}', ha='center', va='bottom', color='white', fontsize=12, fontweight='bold')
        
        ax.set_title("Biểu Đồ Cột - Sản Phẩm Bán Chạy", fontsize=18, color="white", pad=20, fontweight='bold')
        ax.set_xlabel("Sản phẩm", fontsize=14, color="white", fontweight='bold')
        ax.set_ylabel("Số lượng bán", fontsize=14, color="white", fontweight='bold')
        
        # Customization
        ax.tick_params(colors="white", rotation=45, labelsize=10)
        ax.grid(True, alpha=0.3, color="white", axis='y')
        for spine in ax.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Embed vào tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_pie_chart(self):
        """Tạo biểu đồ tròn"""
        # Tạo figure và axis
        fig, ax = plt.subplots(figsize=(10, 8), facecolor="#1a1a2e")
        ax.set_facecolor("#16213e")
        
        # Màu sắc cho biểu đồ tròn
        colors = ['#e74c3c', '#3498db', '#f39c12', '#27ae60', '#9b59b6', '#34495e', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
        
        # Vẽ biểu đồ tròn
        wedges, texts, autotexts = ax.pie(
            self.product_data['quantities'], 
            labels=self.product_data['products'],
            colors=colors[:len(self.product_data['products'])], 
            autopct='%1.1f%%',
            startangle=90, 
            textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'}
        )
        
        # Tùy chỉnh text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(11)
        
        ax.set_title("Biểu Đồ Tròn - Tỷ Lệ Sản Phẩm Bán Chạy", fontsize=18, color="white", pad=20, fontweight='bold')
        
        plt.tight_layout()
        
        # Embed vào tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_bar_chart(self):
        """Tạo biểu đồ ngang"""
        # Tạo figure và axis
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="#1a1a2e")
        ax.set_facecolor("#16213e")
        
        # Màu sắc cho từng thanh
        colors = ['#e74c3c', '#3498db', '#f39c12', '#27ae60', '#9b59b6', '#34495e', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
        
        # Vẽ biểu đồ ngang
        bars = ax.barh(self.product_data['products'], 
                      self.product_data['quantities'],
                      color=colors[:len(self.product_data['products'])], alpha=0.8)
        
        # Thêm giá trị vào cuối mỗi thanh
        for bar, qty in zip(bars, self.product_data['quantities']):
            width = bar.get_width()
            ax.text(width + max(self.product_data['quantities'])*0.01, bar.get_y() + bar.get_height()/2.,
                   f'{qty}', ha='left', va='center', color='white', fontsize=12, fontweight='bold')
        
        ax.set_title("Biểu Đồ Ngang - Sản Phẩm Bán Chạy", fontsize=18, color="white", pad=20, fontweight='bold')
        ax.set_xlabel("Số lượng bán", fontsize=14, color="white", fontweight='bold')
        ax.set_ylabel("Sản phẩm", fontsize=14, color="white", fontweight='bold')
        
        # Customization
        ax.tick_params(colors="white", labelsize=10)
        ax.grid(True, alpha=0.3, color="white", axis='x')
        for spine in ax.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Embed vào tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def close_window(self):
        """Đóng cửa sổ"""
        plt.close('all')  # Đóng tất cả figure matplotlib
        self.root.destroy()
        if self.parent_window:
            self.parent_window.deiconify()  # Hiện lại cửa sổ chính
    
    def run(self):
        self.root.lift()
        self.root.focus_force()
        self.root.mainloop()

# Cách sử dụng với dữ liệu trực tiếp
def run_sales_chart_with_data(parent_window=None, json_data=None):
    """Chạy biểu đồ với dữ liệu được truyền vào"""
    app = SalesChartView(parent_window, json_data)
    app.run()

# Test nếu chạy trực tiếp
if __name__ == "__main__":
    app = SalesChartView()
    app.run()