# views/bao_cao_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from collections import defaultdict

class BaoCaoView:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.root.state('zoomed')  # Full screen trên Windows
        self.root.title("📊 Báo cáo cửa hàng")
        self.root.configure(bg="#f0f2f5")
        
        self.customer_data = []
        self.stats = {}
        
        self.load_customer_data()
        self.setup_ui()
        
    def load_customer_data(self):
        """Tải dữ liệu khách hàng từ file JSON"""
        try:
            # Cập nhật danh sách đường dẫn file để tìm
            paths = [
                'customers.json',  # Tên file thực tế
                'data/customers.json',
                '../data/customers.json',
                'data/customer.json',  # Các tên file cũ (backup)
                'customer.json',
                '../data/customer.json'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    print(f"Đã tìm thấy file: {path}")  # Debug log
                    
                    # Kiểm tra file có rỗng không
                    if os.path.getsize(path) == 0:
                        print(f"File {path} rỗng, sử dụng dữ liệu mẫu")
                        self.use_sample_data()
                        return
                    
                    # Đọc file JSON
                    with open(path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        
                        # Kiểm tra dữ liệu có hợp lệ không
                        if isinstance(data, list) and len(data) > 0:
                            self.customer_data = data
                            print(f"Đã tải thành công {len(data)} khách hàng từ {path}")
                            return
                        else:
                            print(f"File {path} không có dữ liệu hợp lệ")
                            continue
            
            # Nếu không tìm thấy file nào hoặc file không hợp lệ
            print("Không tìm thấy file dữ liệu hợp lệ, sử dụng dữ liệu mẫu")
            self.use_sample_data()
            
        except json.JSONDecodeError as e:
            print(f"Lỗi định dạng JSON: {e}")
            messagebox.showwarning("Cảnh báo", f"File JSON có lỗi định dạng: {str(e)}\nSử dụng dữ liệu mẫu.")
            self.use_sample_data()
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
            messagebox.showwarning("Cảnh báo", f"Không thể tải dữ liệu: {str(e)}\nSử dụng dữ liệu mẫu.")
            self.use_sample_data()

    
    def use_sample_data(self):
        """Dữ liệu mẫu"""
        self.customer_data = [
        #     {"customer_id":"KH1001","name":"Nguyễn Văn An","group":"VIP","gender":"Nam","phone":"0987654321","email":"an@email.com","address":"Hà Nội","product":"💻 Laptop","quantity":"2","total_amount":"25000000"},
        #     {"customer_id":"KH1002","name":"Trần Thị Bình","group":"Thường","gender":"Nữ","phone":"0976543210","email":"binh@email.com","address":"TP.HCM","product":"📱 iPhone","quantity":"1","total_amount":"20000000"},
        #     {"customer_id":"KH1003","name":"Lê Văn Cường","group":"VIP","gender":"Nam","phone":"0965432109","email":"cuong@email.com","address":"Đà Nẵng","product":"🖥️ PC","quantity":"1","total_amount":"30000000"},
        #     {"customer_id":"KH1004","name":"Phạm Thị Dung","group":"Thường","gender":"Nữ","phone":"0911222333","email":"dung@email.com","address":"Cần Thơ","product":"📱 Samsung","quantity":"3","total_amount":"18000000"},
        #     {"customer_id":"KH1005","name":"Hoàng Văn Em","group":"VIP","gender":"Nam","phone":"0933444555","email":"em@email.com","address":"Huế","product":"💻 MacBook","quantity":"1","total_amount":"35000000"},
        #     {"customer_id":"KH1006","name":"Đỗ Thị Hoa","group":"Thường","gender":"Nữ","phone":"0900123456","email":"hoa@email.com","address":"Hà Nội","product":"🎧 Tai nghe","quantity":"2","total_amount":"2000000"},
        #     {"customer_id":"KH1007","name":"Ngô Văn Ích","group":"VIP","gender":"Nam","phone":"0912345678","email":"ich@email.com","address":"Hải Phòng","product":"📺 TV","quantity":"1","total_amount":"15000000"},
        #     {"customer_id":"KH1008","name":"Bùi Thị Lan","group":"Thường","gender":"Nữ","phone":"0923456789","email":"lan@email.com","address":"Quảng Ninh","product":"⌚ Đồng hồ","quantity":"1","total_amount":"5000000"},
        #     {"customer_id":"KH1009","name":"Trịnh Văn Mạnh","group":"VIP","gender":"Nam","phone":"0934567890","email":"manh@email.com","address":"Nha Trang","product":"📷 Camera","quantity":"1","total_amount":"10000000"},
        #     {"customer_id":"KH1010","name":"Cao Thị Nhung","group":"Thường","gender":"Nữ","phone":"0945678901","email":"nhung@email.com","address":"Bắc Ninh","product":"📀 Ổ cứng","quantity":"2","total_amount":"3000000"}
        ]
    
    def clean_number(self, value):
        """Làm sạch và chuyển đổi số"""
        if not value:
            return 0
        cleaned = ''.join(char for char in str(value) if char.isdigit())
        return int(cleaned) if cleaned else 0
    
    def calculate_stats(self):
        """Tính toán thống kê"""
        self.stats = {
            'total_customers': len(self.customer_data),
            'vip_count': 0,
            'male_count': 0,
            'female_count': 0,
            'total_revenue': 0,
            'total_quantity': 0,
            'products': defaultdict(int),
            'regions': defaultdict(int),
            'monthly_revenue': 0
        }
        
        for customer in self.customer_data:
            # Đếm VIP
            if customer.get('group', '').lower() == 'vip':
                self.stats['vip_count'] += 1
            
            # Đếm giới tính
            gender = customer.get('gender', '').lower()
            if gender in ['nam', 'male']:
                self.stats['male_count'] += 1
            elif gender in ['nữ', 'female']:
                self.stats['female_count'] += 1
            
            # Tính doanh thu và số lượng
            amount = self.clean_number(customer.get('total_amount', 0))
            quantity = self.clean_number(customer.get('quantity', 0))
            
            self.stats['total_revenue'] += amount
            self.stats['total_quantity'] += quantity
            
            # Thống kê sản phẩm và khu vực
            product = customer.get('product', 'Khác')
            region = customer.get('address', 'Khác')
            self.stats['products'][product] += 1
            self.stats['regions'][region] += 1
    
    def setup_ui(self):
        """Thiết lập giao diện chính"""
        self.calculate_stats()
        
        # Header
        self.create_header()
        
        # Main content với grid layout
        main_container = tk.Frame(self.root, bg="#f0f2f5")
        main_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Cấu hình grid cho layout cân đối
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=2)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Top section - Thống kê tổng quan (2 cột)
        self.create_overview_section(main_container)
        
        # Bottom left - Biểu đồ/thống kê sản phẩm
        self.create_product_section(main_container)
        
        # Bottom right - Bảng chi tiết
        self.create_detail_table(main_container)
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Tạo header"""
        header = tk.Frame(self.root, bg="#2c3e50", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Container cho header content
        header_content = tk.Frame(header, bg="#2c3e50")
        header_content.pack(expand=True, fill="both")
        
        # Tiêu đề chính
        tk.Label(
            header_content,
            text="📊 BÁO CÁO TỔNG HỢP CỬA HÀNG",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)
        
        # Thời gian
        time_str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        tk.Label(
            header_content,
            text=f"Cập nhật: {time_str}",
            font=("Arial", 10),
            fg="#bdc3c7",
            bg="#2c3e50"
        ).pack()
    
    def create_overview_section(self, parent):
        """Tạo section tổng quan - chiếm 2 cột trên cùng"""
        overview_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
        overview_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Tiêu đề
        tk.Label(
            overview_frame,
            text="📈 THỐNG KÊ TỔNG QUAN",
            font=("Arial", 14, "bold"),
            fg="#2c3e50",
            bg="white"
        ).pack(pady=10)
        
        # Container cho các thẻ thống kê
        cards_frame = tk.Frame(overview_frame, bg="white")
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        # Cấu hình grid 2x3 cho 6 thẻ
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1, uniform="cards")
        
        # Dữ liệu thống kê
        stats_data = [
            ("👥", "Tổng KH", self.stats['total_customers'], "#3498db"),
            ("💰", "Doanh thu", f"{self.stats['total_revenue']:,}", "#27ae60"),
            ("📦", "Sản phẩm", self.stats['total_quantity'], "#f39c12"),
            ("🏆", "KH VIP", self.stats['vip_count'], "#9b59b6"),
            ("👨", "Nam", self.stats['male_count'], "#34495e"),
            ("👩", "Nữ", self.stats['female_count'], "#e74c3c")
        ]
        
        for i, (icon, label, value, color) in enumerate(stats_data):
            row, col = i // 3, i % 3
            self.create_stat_card(cards_frame, icon, label, str(value), color, row, col)
    
    def create_stat_card(self, parent, icon, label, value, color, row, col):
        """Tạo thẻ thống kê"""
        card = tk.Frame(parent, bg="#f8f9fa", relief="solid", bd=1)
        card.grid(row=row, column=col, padx=8, pady=5, sticky="ew")
        
        tk.Label(card, text=icon, font=("Arial", 20), fg=color, bg="#f8f9fa").pack(pady=5)
        tk.Label(card, text=label, font=("Arial", 9, "bold"), fg="#7f8c8d", bg="#f8f9fa").pack()
        tk.Label(card, text=value, font=("Arial", 12, "bold"), fg=color, bg="#f8f9fa").pack(pady=5)
    
    def create_product_section(self, parent):
        """Tạo section thống kê sản phẩm"""
        product_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
        product_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Tiêu đề
        tk.Label(
            product_frame,
            text="📊 THỐNG KÊ SẢN PHẨM & KHU VỰC",
            font=("Arial", 12, "bold"),
            fg="#2c3e50",
            bg="white"
        ).pack(pady=10)
        
        # Scrollable content
        canvas = tk.Canvas(product_frame, bg="white")
        scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Top sản phẩm
        tk.Label(
            scrollable_frame,
            text="🏆 Top sản phẩm:",
            font=("Arial", 11, "bold"),
            fg="#2c3e50",
            bg="white"
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        sorted_products = sorted(self.stats['products'].items(), key=lambda x: x[1], reverse=True)[:5]
        colors = ["#e74c3c", "#f39c12", "#27ae60", "#3498db", "#9b59b6"]
        
        for i, (product, count) in enumerate(sorted_products):
            color = colors[i] if i < len(colors) else "#7f8c8d"
            tk.Label(
                scrollable_frame,
                text=f"{i+1}. {product}: {count}",
                font=("Arial", 10),
                fg=color,
                bg="white"
            ).pack(anchor="w", padx=25, pady=2)
        
        # Top khu vực
        tk.Label(
            scrollable_frame,
            text="🌍 Top khu vực:",
            font=("Arial", 11, "bold"),
            fg="#2c3e50",
            bg="white"
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        sorted_regions = sorted(self.stats['regions'].items(), key=lambda x: x[1], reverse=True)[:5]
        
        for i, (region, count) in enumerate(sorted_regions):
            color = colors[i] if i < len(colors) else "#7f8c8d"
            tk.Label(
                scrollable_frame,
                text=f"{i+1}. {region}: {count}",
                font=("Arial", 10),
                fg=color,
                bg="white"
            ).pack(anchor="w", padx=25, pady=2)
        
        # Thông tin bổ sung
        if self.stats['total_customers'] > 0:
            avg_revenue = self.stats['total_revenue'] / self.stats['total_customers']
            vip_percent = (self.stats['vip_count'] / self.stats['total_customers']) * 100
            
            tk.Label(
                scrollable_frame,
                text="📈 Phân tích:",
                font=("Arial", 11, "bold"),
                fg="#2c3e50",
                bg="white"
            ).pack(anchor="w", padx=15, pady=(15, 5))
            
            tk.Label(
                scrollable_frame,
                text=f"• TB doanh thu/KH: {avg_revenue:,.0f} VNĐ",
                font=("Arial", 10),
                fg="#27ae60",
                bg="white"
            ).pack(anchor="w", padx=25, pady=2)
            
            tk.Label(
                scrollable_frame,
                text=f"• Tỷ lệ VIP: {vip_percent:.1f}%",
                font=("Arial", 10),
                fg="#9b59b6",
                bg="white"
            ).pack(anchor="w", padx=25, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Bind mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def create_detail_table(self, parent):
        """Tạo bảng chi tiết giao dịch"""
        table_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
        table_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Tiêu đề
        tk.Label(
            table_frame,
            text="📋 CHI TIẾT GIAO DỊCH",
            font=("Arial", 12, "bold"),
            fg="#2c3e50",
            bg="white"
        ).pack(pady=10)
        
        # Treeview container
        tree_container = tk.Frame(table_frame, bg="white")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("ID", "Tên", "Sản phẩm", "SL", "Thành tiền")
        tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=15)
        
        # Cấu hình columns
        tree.heading("ID", text="Mã KH")
        tree.heading("Tên", text="Tên khách hàng")
        tree.heading("Sản phẩm", text="Sản phẩm")
        tree.heading("SL", text="SL")
        tree.heading("Thành tiền", text="Thành tiền (VNĐ)")
        
        tree.column("ID", width=80, anchor="center")
        tree.column("Tên", width=120)
        tree.column("Sản phẩm", width=120)
        tree.column("SL", width=40, anchor="center")
        tree.column("Thành tiền", width=100, anchor="e")
        
        # Thêm dữ liệu
        for customer in self.customer_data:
            amount = self.clean_number(customer.get('total_amount', 0))
            quantity = self.clean_number(customer.get('quantity', 0))
            
            tree.insert("", "end", values=(
                customer.get('customer_id', 'N/A'),
                customer.get('name', 'N/A')[:15] + "..." if len(customer.get('name', '')) > 15 else customer.get('name', 'N/A'),
                customer.get('product', 'N/A')[:15] + "..." if len(customer.get('product', '')) > 15 else customer.get('product', 'N/A'),
                quantity,
                f"{amount:,}"
            ))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
    
    def create_footer(self):
        """Tạo footer với các nút điều khiển"""
        footer = tk.Frame(self.root, bg="#ecf0f1", height=50)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        
        # Container cho buttons
        btn_frame = tk.Frame(footer, bg="#ecf0f1")
        btn_frame.pack(expand=True)
        
        # Nút làm mới
        refresh_btn = tk.Button(
            btn_frame,
            text="🔄 Làm mới",
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=8,
            command=self.refresh_data
        )
        refresh_btn.pack(side="left", padx=10)
        
        # Nút xuất báo cáo
        export_btn = tk.Button(
            btn_frame,
            text="📄 Xuất báo cáo",
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            command=self.export_report
        )
        export_btn.pack(side="left", padx=10)
        
        # Nút đóng
        close_btn = tk.Button(
            btn_frame,
            text="❌ Đóng",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
            command=self.close_window
        )
        close_btn.pack(side="right", padx=10)
    
    def refresh_data(self):
        """Làm mới dữ liệu"""
        try:
            self.load_customer_data()
            self.calculate_stats()
            # Đóng cửa sổ hiện tại và mở lại
            self.root.destroy()
            new_window = BaoCaoView(self.parent_window)
            new_window.run()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mới: {str(e)}")
    
    def export_report(self):
        """Xuất báo cáo (placeholder)"""
        messagebox.showinfo("Thông báo", "Chức năng xuất báo cáo sẽ được phát triển trong phiên bản sau!")
    
    def close_window(self):
        """Đóng cửa sổ"""
        self.root.destroy()
    
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

