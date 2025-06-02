import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random  # Thêm import này ở đầu file
from controllers.khach_hang_controller import CustomerController
import tkinter.font as tkFont

class CustomerManagementView(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.customer_controller = CustomerController()

        # Danh sách sản phẩm công nghệ với giá
        self.tech_products = {
            "💻 Laptop Gaming": 25000000,
            "📱 iPhone 15 Pro": 30000000,
            "🎧 AirPods Pro": 6000000,
            "⌚ Apple Watch": 12000000,
            "🖥️ iMac 27\"": 45000000,
            "📟 iPad Pro": 28000000,
            "🎮 PlayStation 5": 15000000,
            "🕹️ Xbox Series X": 13000000,
            "📺 Smart TV 4K": 18000000,
            "🔊 HomePod": 8000000,
            "💾 SSD 1TB": 3000000,
            "🖱️ Magic Mouse": 2500000,
            "⌨️ Mechanical Keyboard": 4000000,
            "📷 Canon DSLR": 22000000,
            "🎤 Microphone Pro": 5000000
        }

        # Set để lưu trữ các ID đã sử dụng
        self.used_ids = set()

        # Cấu hình Frame để chiếm toàn bộ không gian trong master
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.setup_window()
        self.setup_styles()
        self.create_header()
        self.create_main_content()
        self.load_sample_customers()

        # Tạo ID ngẫu nhiên khi khởi tạo
        self.generate_new_customer_id()

        self.all_customers_data = []
        self.show_all_customers()  # load danh sách khách hàng để tìm kiếm hoạt động

    def generate_customer_id(self):
        """Tạo ID khách hàng tự động và duy nhất"""
        while True:
            new_id = f"KH{random.randint(1000, 9999)}"
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id

    def generate_new_customer_id(self):
        """Tạo ID mới và hiển thị trong form"""
        new_id = self.generate_customer_id()
        if hasattr(self, 'entries') and 'customer_id' in self.entries:
            self.entries['customer_id'].config(state='normal')
            self.entries['customer_id'].delete(0, tk.END)
            self.entries['customer_id'].insert(0, new_id)
            self.entries['customer_id'].config(state='readonly')

    def setup_window(self):
        """Thiết lập cửa sổ chính với style hiện đại"""
        self.master.title("🏢 Hệ Thống Quản Lý Khách Hàng")
        
        # Cách 1: Full màn hình (ẩn thanh tiêu đề và taskbar)
        self.master.attributes("-fullscreen", True)
        
        # Nếu bạn muốn vừa có thanh tiêu đề, vừa full màn hình thì thay bằng:
        # width = self.master.winfo_screenwidth()
        # height = self.master.winfo_screenheight()
        # self.master.geometry(f"{width}x{height}+0+0")
        
        self.master.configure(bg="#0f3460")
        self.master.minsize(1200, 700)
        
        try:
            self.master.iconbitmap("")
        except:
            pass
    
    def setup_styles(self):
        """Thiết lập style cho các component"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colors - Modern palette  
        self.colors = {
            'primary': '#4472C4',      # Blue
            'secondary': '#70AD47',    # Green
            'accent': '#FFC000',       # Yellow
            'danger': '#E74C3C',       # Red
            'light': '#F8F9FA',        # Light gray
            'dark': '#2C3E50',         # Dark gray
            'white': '#FFFFFF',
            'border': '#D1D5DB'        # Border gray
        }
        
        # Custom styles
        self.style.configure('Header.TLabel',
                           font=('Arial', 11, 'bold'),
                           foreground=self.colors['dark'])
        
        self.style.configure('Modern.TFrame',
                           background=self.colors['white'],
                           relief='solid',
                           borderwidth=1)
        
        # Treeview styling
        self.style.configure('Modern.Treeview',
                           background=self.colors['white'],
                           foreground=self.colors['dark'],
                           rowheight=25,
                           fieldbackground=self.colors['white'],
                           borderwidth=1,
                           font=('Arial', 9))
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Arial', 9, 'bold'),
                           background=self.colors['primary'],
                           foreground='white',
                           relief='flat')

    def exit_app(self):
        # Đóng màn hình quản lý chính
        self.master.destroy()
        
        # Mở lại màn hình chọn chức năng
        from controllers.bat_tat_screen_controller import ScreenController
        ScreenController.open_main_screen()

    def create_header(self):
        """Tạo header với thông tin thời gian"""
        header_frame = tk.Frame(self.master, height=60, bg=self.colors['white'], relief='solid', bd=1)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Left side - Logo và title
        left_frame = tk.Frame(header_frame, bg=self.colors['white'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)
        
        title_label = tk.Label(
            left_frame,
            text="",
            bg=self.colors['white'],
            fg=self.colors['primary'],
            font=('Arial', 1, 'bold')
        )
        title_label.pack(anchor='w')
        
        # Center - Main title
        center_frame = tk.Frame(header_frame, bg=self.colors['white'])
        center_frame.pack(expand=True, fill=tk.BOTH)

        main_title = tk.Label(
            center_frame,
            text="Quản lý thông tin khách hàng",
            bg=self.colors['white'],
            fg=self.colors['dark'],
            font=('Arial', 18, 'bold')
        )
        main_title.pack(expand=True)
        
        # Right side - Time
        right_frame = tk.Frame(header_frame, bg=self.colors['white'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=10)
        
        self.time_label = tk.Label(center_frame, text="🕒", bg="#34495e", fg="white", font=("Segoe UI", 9, "bold"))
        self.time_label.pack(side=tk.LEFT, padx=10, pady=4)

        self.date_label = tk.Label(center_frame, text="📅", bg="#34495e", fg="white", font=("Segoe UI", 9, "bold"))
        self.date_label.pack(side=tk.LEFT, padx=8, pady=4)
        exit_button = ttk.Button(center_frame, text="🔚 Trở về", command=self.exit_app)
        exit_button.place(relx=0.97, rely=0.02, anchor="ne")
        self.update_time()
    
    def update_time(self):
        """Cập nhật thời gian"""
        current_time = datetime.now().strftime('%H:%M:%S')
        current_date = datetime.now().strftime('%d-%m-%Y')
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.master.after(1000, self.update_time)

    def create_main_content(self):
        """Tạo nội dung chính với layout mới"""
        main_container = tk.Frame(self.master, bg="#f0f2f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Thông tin khách hàng
        self.create_customer_info_panel(main_container)
        
        # Right panel - Tìm kiếm và danh sách
        self.create_search_and_list_panel(main_container)

    def create_customer_info_panel(self, parent):
        """Tạo panel thông tin khách hàng bên trái"""
        # Main info frame
        info_frame = tk.Frame(parent, bg=self.colors['white'], relief='solid', bd=1)
        info_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=0)
        info_frame.configure(width=450)
        info_frame.pack_propagate(False)
        
        # Header
        header_frame = tk.Frame(info_frame, bg=self.colors['primary'], height=35)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Thông tin khách hàng",
            bg=self.colors['primary'],
            fg="white",
            font=('Arial', 12, 'bold')
        )
        header_label.pack(pady=8)
        
        # Form container
        form_frame = tk.Frame(info_frame, bg=self.colors['white'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.entries = {}
        self.create_customer_form(form_frame)
    

    def create_customer_form(self, parent):
        """Tạo form thông tin khách hàng"""
        # Thông tin cơ bản
        basic_frame = tk.LabelFrame(parent, text="Thông tin cơ bản", bg=self.colors['white'], 
                                  font=('Arial', 10, 'bold'), fg=self.colors['dark'])
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Row 1: Loại KH và Giới tính
        row1 = tk.Frame(basic_frame, bg=self.colors['white'])
        row1.pack(fill=tk.X, padx=10, pady=5)
        
        # Loại khách hàng
        tk.Label(row1, text="Loại KH:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['customer_type'] = ttk.Combobox(row1, values=['Thường', 'VIP'], 
                                                   state='readonly', width=12, font=('Arial', 9))
        self.entries['customer_type'].set('Thường')
        self.entries['customer_type'].pack(side=tk.LEFT, padx=(5, 20))
        
        # Giới tính
        tk.Label(row1, text="Giới tính:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.gender_var = tk.StringVar(value="Nam")
        gender_frame = tk.Frame(row1, bg=self.colors['white'])
        gender_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(gender_frame, text="Nam", variable=self.gender_var, value="Nam",
                      bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Nữ", variable=self.gender_var, value="Nữ",
                      bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Row 2: ID và Tên
        row2 = tk.Frame(basic_frame, bg=self.colors['white'])
        row2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row2, text="ID Khách hàng:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['customer_id'] = tk.Entry(row2, width=15, font=('Arial', 9), state='readonly', bg=self.colors['light'])
        self.entries['customer_id'].pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(row2, text="Tên KH:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['name'] = tk.Entry(row2, width=20, font=('Arial', 9))
        self.entries['name'].pack(side=tk.LEFT, padx=5)
        
        # Row 3: Lớp và CMND
        row3 = tk.Frame(basic_frame, bg=self.colors['white'])
        row3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row3, text="Nhóm KH:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['group'] = tk.Entry(row3, width=15, font=('Arial', 9))
        self.entries['group'].pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(row3, text="CMND:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['cmnd'] = tk.Entry(row3, width=15, font=('Arial', 9))
        self.entries['cmnd'].pack(side=tk.LEFT, padx=5)
        
        # Row 4: Email và Ngày sinh
        row4 = tk.Frame(basic_frame, bg=self.colors['white'])
        row4.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row4, text="Email:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['email'] = tk.Entry(row4, width=20, font=('Arial', 9))
        self.entries['email'].pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(row4, text="Ngày sinh:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['birth_date'] = tk.Entry(row4, width=12, font=('Arial', 9))
        self.entries['birth_date'].pack(side=tk.LEFT, padx=5)
        
        # Row 5: Địa chỉ và SĐT
        row5 = tk.Frame(basic_frame, bg=self.colors['white'])
        row5.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(row5, text="Địa chỉ:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['address'] = tk.Entry(row5, width=25, font=('Arial', 9))
        self.entries['address'].pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(row5, text="SĐT:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['phone'] = tk.Entry(row5, width=12, font=('Arial', 9))
        self.entries['phone'].pack(side=tk.LEFT, padx=5)
        
        # Thông tin sản phẩm
        product_frame = tk.LabelFrame(parent, text="Thông tin sản phẩm", bg=self.colors['white'],
                                    font=('Arial', 10, 'bold'), fg=self.colors['dark'])
        product_frame.pack(fill=tk.X, pady=(10, 10))
        
        # Row 1: Sản phẩm và Số lượng
        prod_row1 = tk.Frame(product_frame, bg=self.colors['white'])
        prod_row1.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(prod_row1, text="Sản phẩm:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['product'] = ttk.Combobox(prod_row1, values=list(self.tech_products.keys()), 
                                             state='readonly', width=25, font=('Arial', 9))
        self.entries['product'].pack(side=tk.LEFT, padx=(5, 10))
        self.entries['product'].bind('<<ComboboxSelected>>', self.on_product_change)
        
        tk.Label(prod_row1, text="SL:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['quantity'] = tk.Spinbox(prod_row1, from_=1, to=100, width=5, font=('Arial', 9),
                                            command=self.calculate_total)
        self.entries['quantity'].pack(side=tk.LEFT, padx=5)
        self.entries['quantity'].bind('<KeyRelease>', self.calculate_total)
        
        # Row 2: Đơn giá và Tổng tiền  
        prod_row2 = tk.Frame(product_frame, bg=self.colors['white'])
        prod_row2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(prod_row2, text="Đơn giá:", bg=self.colors['white'], font=('Arial', 9)).pack(side=tk.LEFT)
        self.entries['unit_price'] = tk.Entry(prod_row2, width=15, font=('Arial', 9), 
                                            state='readonly', bg=self.colors['light'])
        self.entries['unit_price'].pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(prod_row2, text="Tổng tiền:", bg=self.colors['white'], font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.entries['total_amount'] = tk.Entry(prod_row2, width=15, font=('Arial', 9, 'bold'),
                                              state='readonly', bg=self.colors['light'])
        self.entries['total_amount'].pack(side=tk.LEFT, padx=5)
        
        # Buttons
        self.create_buttons(parent)

    def create_buttons(self, parent):
        """Tạo các nút chức năng"""
        button_frame = tk.Frame(parent, bg=self.colors['white'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Button configuration
        btn_config = {
            'font': ('Arial', 10, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'cursor': 'hand2',
            'width': 12,
            'height': 1
        }
        
        # Row 1
        row1 = tk.Frame(button_frame, bg=self.colors['white'])
        row1.pack(fill=tk.X, pady=(0, 5))
        
        tk.Button(row1, text="Lưu", bg=self.colors['secondary'], fg='white',
                 command=self.add_customer, **btn_config).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(row1, text="Sửa", bg=self.colors['accent'], fg='black',
                 command=self.update_customer, **btn_config).pack(side=tk.LEFT, padx=5)
        
        tk.Button(row1, text="Xóa", bg=self.colors['danger'], fg='white',
                 command=self.delete_customer, **btn_config).pack(side=tk.LEFT, padx=5)
        
        # Row 2
        row2 = tk.Frame(button_frame, bg=self.colors['white'])
        row2.pack(fill=tk.X)
        
        tk.Button(row2, text="Data mẫu", bg=self.colors['primary'], fg='white',
                 command=self.load_sample_data, **btn_config).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(row2, text="Tạo ID", bg='#6C757D', fg='white',
                command=self.new_customer, **btn_config).pack(side=tk.LEFT, padx=5)

    def new_customer(self):
        """Chuẩn bị form để thêm khách hàng mới"""
        self.clear_form()  # Xóa trắng toàn bộ form

        # Tạo ID mới và đưa vào ô customer_id
        new_id = self.generate_customer_id()
        self.entries['customer_id'].config(state='normal')
        self.entries['customer_id'].delete(0, tk.END)
        self.entries['customer_id'].insert(0, new_id)
        self.entries['customer_id'].config(state='readonly')


    def clear_form(self):
        """Xóa dữ liệu form"""
        # Xóa các entry
        for key, entry in self.entries.items():
            if key not in ['customer_type', 'product']:  # Không xóa combobox
                if hasattr(entry, 'config'):
                    entry.config(state='normal')
                entry.delete(0, tk.END)
                if key in ['customer_id', 'unit_price', 'total_amount']:
                    entry.config(state='readonly')
        
        # Reset combobox
        self.entries['customer_type'].set('Thường')
        self.entries['product'].set('')
        
        # Reset radio button
        self.gender_var.set("Nam")
        
        # Tạo ID mới
        new_id = self.generate_customer_id()
        self.entries['customer_id'].config(state='normal')
        self.entries['customer_id'].insert(0, new_id)
        self.entries['customer_id'].config(state='readonly')

    def add_customer(self):
        """Thêm khách hàng mới"""
        # Validate dữ liệu
        if not self.validate_form():
            return
        
        try:
            customer_data = self.get_form_data()
            
            # Thêm vào controller (giả lập)
            self.customer_controller.add_customer(customer_data)
            
            # Thêm vào tree
            self.add_to_tree(customer_data)
            
            # Update group filter
            self.update_group_filter()
            
            messagebox.showinfo("Thành công", "Đã thêm khách hàng thành công!")
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm khách hàng: {str(e)}")

    # Các phương thức khác giữ nguyên như trong code gốc...
    def on_product_change(self, event=None):
        """Xử lý khi thay đổi sản phẩm"""
        product = self.entries['product'].get()
        if product in self.tech_products:
            price = self.tech_products[product]
            self.entries['unit_price'].config(state='normal')
            self.entries['unit_price'].delete(0, tk.END)
            self.entries['unit_price'].insert(0, f"{price:,}")
            self.entries['unit_price'].config(state='readonly')
            self.calculate_total()

    def calculate_total(self, event=None):
        """Tính tổng tiền"""
        try:
            quantity = int(self.entries['quantity'].get())
            unit_price_str = self.entries['unit_price'].get().replace(',', '')
            if unit_price_str:
                unit_price = float(unit_price_str)
                total = quantity * unit_price
                
                self.entries['total_amount'].config(state='normal')
                self.entries['total_amount'].delete(0, tk.END)
                self.entries['total_amount'].insert(0, f"{total:,.0f}")
                self.entries['total_amount'].config(state='readonly')
        except ValueError:
            pass

    def validate_form(self):
        """Kiểm tra tính hợp lệ của form"""
        required_fields = {
            'name': 'Tên khách hàng',
            'phone': 'Số điện thoại',
            'email': 'Email',
            'product': 'Sản phẩm'
        }
        
        for field, label in required_fields.items():
            if not self.entries[field].get().strip():
                messagebox.showerror("Lỗi", f"Vui lòng nhập {label}")
                self.entries[field].focus()
                return False
        
        # Validate email
        email = self.entries['email'].get().strip()
        if '@' not in email or '.' not in email:
            messagebox.showerror("Lỗi", "Email không hợp lệ")
            return False
        
        # Validate phone
        phone = self.entries['phone'].get().strip()
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Lỗi", "Số điện thoại phải có ít nhất 10 chữ số")
            return False
        
        return True

    def get_form_data(self):
        """Lấy dữ liệu từ form"""
        try:
            def parse_number(value):
                # Xử lý số với dấu phân cách thập phân
                try:
                    # Loại bỏ dấu phẩy và chuyển thành số
                    return float(value.replace(',', '').replace('.', '', 1))
                except ValueError:
                    return 0  # Nếu không phải số hợp lệ thì trả về 0

            return {
                'customer_id': self.entries['customer_id'].get().strip(),
                'name': self.entries['name'].get().strip(),
                'group': self.entries['group'].get().strip() or "Mặc định",
                'gender': self.gender_var.get(),
                'phone': self.entries['phone'].get().strip(),
                'email': self.entries['email'].get().strip(),
                'customer_type': self.entries['customer_type'].get(),
                'cmnd': self.entries['cmnd'].get().strip(),
                'birth_date': self.entries['birth_date'].get().strip(),
                'address': self.entries['address'].get().strip(),
                'product': self.entries['product'].get(),
                'quantity': parse_number(self.entries['quantity'].get().strip()),
                'total_amount': parse_number(self.entries['total_amount'].get().strip())
            }
        except Exception as e:
            print(f"Error in get_form_data: {e}")
            return {}


    def add_to_tree(self, data):
        """Thêm dữ liệu vào tree"""
        values = (
            data['customer_id'],
    data['name'],
    data['group'],
    data['gender'],
    data['phone'],
    data['email'],
    data['customer_type'],
    data['product'],
    data['quantity'],
    data['total_amount'],
    data['cmnd'],
    data['birth_date'],  # ✅ đúng vị trí
    data['address']
        )
        print("DEBUG - Số trường trong values khi thêm mới:", len(values))  # 👈 Thêm dòng này tại đây
        self.tree.insert('', tk.END, values=values)


    # Phần còn lại của code sẽ được thêm trong phần tiếp theo...
    def create_search_and_list_panel(self, parent):
        """Tạo panel tìm kiếm và danh sách bên phải"""
        right_panel = tk.Frame(parent, bg=self.colors['white'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=0, padx=(5, 0))
        
        # Search panel
        self.create_search_panel(right_panel)
        
        # List panel  
        self.create_list_section(right_panel)

    def create_search_panel(self, parent):
        """Tạo panel tìm kiếm"""
        search_frame = tk.Frame(parent, bg=self.colors['white'], relief='solid', bd=1)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Header
        search_header = tk.Frame(search_frame, bg=self.colors['primary'], height=35)
        search_header.pack(fill=tk.X)
        search_header.pack_propagate(False)
        
        tk.Label(search_header, text="Hệ Thống Tìm Kiếm", bg=self.colors['primary'],
                fg="white", font=('Arial', 12, 'bold')).pack(pady=8)
        
        # Search content
        search_content = tk.Frame(search_frame, bg=self.colors['white'])
        search_content.pack(fill=tk.X, padx=15, pady=10)
        
        # Search row
        search_row = tk.Frame(search_content, bg=self.colors['white'])
        search_row.pack(fill=tk.X)
        
        tk.Label(search_row, text="Tìm kiếm theo:", bg=self.colors['white'], 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        self.search_type = ttk.Combobox(search_row, values=['ID Khách hàng', 'Tên KH', 'SĐT', 'Email'], 
                                      state='readonly', width=15, font=('Arial', 9))
        self.search_type.set('ID Khách hàng')
        self.search_type.pack(side=tk.LEFT, padx=(10, 20))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_row, textvariable=self.search_var, width=20, font=('Arial', 9))
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(search_row, text="Tìm kiếm", bg=self.colors['primary'], fg='white',
                 font=('Arial', 9, 'bold'), command=self.search_customers).pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_row, text="Xem tất cả", bg=self.colors['secondary'], fg='white',
                 font=('Arial', 9, 'bold'), command=self.show_all_customers).pack(side=tk.LEFT, padx=5)

    def create_list_section(self, parent):
        """Tạo phần danh sách khách hàng"""
        list_frame = tk.Frame(parent, bg=self.colors['white'], relief='solid', bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        list_header = tk.Frame(list_frame, bg=self.colors['primary'], height=35)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)

        header_content = tk.Frame(list_header, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        tk.Label(header_content, text="Quản lý khách hàng", bg=self.colors['primary'],
                fg="white", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)

        # Management section in header
        mgmt_frame = tk.Frame(header_content, bg=self.colors['primary'])
        mgmt_frame.pack(side=tk.RIGHT)

        # Nhóm filter
        tk.Label(mgmt_frame, text="Nhóm:", bg=self.colors['primary'], fg="white",
                font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.group_filter = ttk.Combobox(mgmt_frame, width=10, font=('Arial', 8), state='readonly')
        self.group_filter.pack(side=tk.LEFT, padx=(0, 10))

        # Loại KH filter
        tk.Label(mgmt_frame, text="Loại KH:", bg=self.colors['primary'], fg="white",
                font=('Arial', 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.type_filter = ttk.Combobox(mgmt_frame, width=10, font=('Arial', 8), state='readonly')
        self.type_filter['values'] = ['Thường', 'VIP']
        self.type_filter.pack(side=tk.LEFT, padx=(0, 10))

        # Nút lọc theo loại KH
        tk.Button(mgmt_frame, text="Lọc loại KH", bg='white', fg=self.colors['primary'],
                font=('Arial', 8, 'bold'), command=self.filter_by_customer_type).pack(side=tk.LEFT, padx=2)

        # Nút xem tất cả
        tk.Button(mgmt_frame, text="Xem tất cả", bg='white', fg=self.colors['primary'],
                font=('Arial', 8, 'bold'), command=self.show_all_customers).pack(side=tk.LEFT, padx=2)

        # Treeview
        tree_frame = tk.Frame(list_frame, bg=self.colors['white'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Create Treeview
        columns = (
    'ID', 'Tên', 'Nhóm', 'Giới tính', 'SĐT', 'Email', 'Loại KH',
    'Sản phẩm', 'Số lượng', 'Tổng tiền', 'CMND', 'Ngày sinh', 'Địa chỉ'
)


        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                style='Modern.Treeview',
                                yscrollcommand=v_scrollbar.set,
                                xscrollcommand=h_scrollbar.set)

        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)

        # Pack scrollbars and tree
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure columns
        column_widths = {
    'ID': 60, 'Tên': 120, 'Nhóm': 80, 'Giới tính': 70, 'SĐT': 100,
    'Email': 150, 'Loại KH': 70, 'Sản phẩm': 150, 'Số lượng': 80,
    'Tổng tiền': 100, 'CMND': 100, 'Ngày sinh': 100, 'Địa chỉ': 150
}


        for col in columns:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, width=column_widths[col], anchor='center')


        # Bind events
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)

        # Bottom management section
        self.create_bottom_management(list_frame)


    def create_bottom_management(self, parent):
        """Tạo phần quản lý dưới cùng"""
        bottom_frame = tk.Frame(parent, bg=self.colors['white'])
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Management controls
        mgmt_frame = tk.LabelFrame(bottom_frame, text="Quản lý khách hàng", bg=self.colors['white'],
                                 font=('Arial', 10, 'bold'))
        mgmt_frame.pack(fill=tk.X, pady=5)
        
        # Controls row
        controls_row = tk.Frame(mgmt_frame, bg=self.colors['white'])
        controls_row.pack(fill=tk.X, padx=10, pady=8)
        
        tk.Label(controls_row, text="Nhóm:", bg=self.colors['white'], 
                font=('Arial', 9)).pack(side=tk.LEFT)
        
        self.manage_group = tk.Entry(controls_row, width=15, font=('Arial', 9))
        self.manage_group.pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(controls_row, text="Tên nhóm:", bg=self.colors['white'], 
                font=('Arial', 9)).pack(side=tk.LEFT)
        
        self.manage_group_name = tk.Entry(controls_row, width=20, font=('Arial', 9))
        self.manage_group_name.pack(side=tk.LEFT, padx=(5, 20))
        
        # Management buttons
        btn_config = {'font': ('Arial', 9, 'bold'), 'relief': 'raised', 'bd': 1, 'cursor': 'hand2'}
        
        tk.Button(controls_row, text="Thêm mới", bg=self.colors['secondary'], fg='white',
                 **btn_config).pack(side=tk.LEFT, padx=2)
        
        tk.Button(controls_row, text="Xóa", bg=self.colors['danger'], fg='white',
                 **btn_config).pack(side=tk.LEFT, padx=2)
        
        tk.Button(controls_row, text="Cập nhật", bg=self.colors['accent'], fg='black',
                 **btn_config).pack(side=tk.LEFT, padx=2)
        
        tk.Button(controls_row, text="Làm mới", bg=self.colors['primary'], fg='white',
                 **btn_config, command= self.load_sample_customers).pack(side=tk.LEFT, padx=2)
    def on_product_change(self, event=None):
        """Xử lý khi thay đổi sản phẩm"""
        product = self.entries['product'].get()
        if product in self.tech_products:
            price = self.tech_products[product]
            self.entries['unit_price'].config(state='normal')
            self.entries['unit_price'].delete(0, tk.END)
            self.entries['unit_price'].insert(0, f"{price:,}")
            self.entries['unit_price'].config(state='readonly')
            self.calculate_total()

    def calculate_total(self, event=None):
        """Tính tổng tiền"""
        try:
            quantity = int(self.entries['quantity'].get())
            unit_price_str = self.entries['unit_price'].get().replace(',', '')
            if unit_price_str:
                unit_price = float(unit_price_str)
                total = quantity * unit_price
                
                self.entries['total_amount'].config(state='normal')
                self.entries['total_amount'].delete(0, tk.END)
                self.entries['total_amount'].insert(0, f"{total:,.0f}")
                self.entries['total_amount'].config(state='readonly')
        except ValueError:
            pass

    def generate_customer_id(self):
        """Tạo ID khách hàng tự động"""
        import random
        return f"KH{random.randint(1000, 9999)}"

    def clear_form(self):
        """Xóa dữ liệu form"""
        # Xóa các entry
        for key, entry in self.entries.items():
            if key not in ['customer_type', 'product']:  # Không xóa combobox
                if hasattr(entry, 'config'):
                    entry.config(state='normal')
                entry.delete(0, tk.END)
                if key in ['customer_id', 'unit_price', 'total_amount']:
                    entry.config(state='readonly')
        
        # Reset combobox
        self.entries['customer_type'].set('Thường')
        self.entries['product'].set('')
        
        # Reset radio button
        self.gender_var.set("Nam")
        
        # Tạo ID mới
        new_id = self.generate_customer_id()
        self.entries['customer_id'].config(state='normal')
        self.entries['customer_id'].insert(0, new_id)
        self.entries['customer_id'].config(state='readonly')

    def add_customer(self):
        """Thêm khách hàng mới"""
        # Validate dữ liệu
        if not self.validate_form():
            return

        try:
            customer_data = self.get_form_data()
            print(customer_data)  # In ra dữ liệu để kiểm tra

            # Thêm vào controller (giả lập)
            self.customer_controller.add_customer(customer_data)

            # Thêm vào tree
            self.add_to_tree(customer_data)

            # Update group filter
            self.update_group_filter()

            messagebox.showinfo("Thành công", "Đã thêm khách hàng thành công!")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm khách hàng: {str(e)}")


    def validate_form(self):
        """Kiểm tra tính hợp lệ của form"""
        required_fields = {
            'name': 'Tên khách hàng',
            'phone': 'Số điện thoại',
            'email': 'Email',
            'product': 'Sản phẩm'
        }
        
        for field, label in required_fields.items():
            if not self.entries[field].get().strip():
                messagebox.showerror("Lỗi", f"Vui lòng nhập {label}")
                self.entries[field].focus()
                return False
        
        # Validate email
        email = self.entries['email'].get().strip()
        if '@' not in email or '.' not in email:
            messagebox.showerror("Lỗi", "Email không hợp lệ")
            return False
        
        # Validate phone
        phone = self.entries['phone'].get().strip()
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Lỗi", "Số điện thoại phải có ít nhất 10 chữ số")
            return False
        
        return True

    def get_form_data(self):
        """Lấy dữ liệu từ form"""
        return {
            'customer_id': self.entries['customer_id'].get(),
            'name': self.entries['name'].get().strip(),
            'group': self.entries['group'].get().strip() or "Mặc định",
            'gender': self.gender_var.get(),
            'phone': self.entries['phone'].get().strip(),
            'email': self.entries['email'].get().strip(),
            'customer_type': self.entries['customer_type'].get(),
            'product': self.entries['product'].get(),
            'quantity': self.entries['quantity'].get(),
            'total_amount': self.entries['total_amount'].get(),
            'cmnd': self.entries['cmnd'].get().strip(),
            'birth_date': self.entries['birth_date'].get().strip(),
            'address': self.entries['address'].get().strip()
            
        }

    def add_to_tree(self, data):
        """Thêm dữ liệu vào tree"""
        values = (
            data['customer_id'],
            data['name'],
            data['group'],
            data['gender'],
            data['phone'],
            data['email'],
            data['customer_type'],
            data['product'],
            data['quantity'],
            data['total_amount'],
            data['cmnd'],
            data['birth_date'],
            data['address']
        )
        self.tree.insert('', tk.END, values=values)

    def on_tree_select(self, event):
        """Xử lý khi chọn item trong tree"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Fill form with selected data
            self.fill_form_from_tree(values)

    def fill_form_from_tree(self, values):
        """Điền dữ liệu đầy đủ vào form từ model"""
        if not values:
            return

        customer_id = values[0]
        full_data = self.customer_controller.get_customer_by_id(customer_id)

        if not full_data:
            return

        self.clear_form()

        # Điền dữ liệu mới sau khi clear
        self.entries['customer_id'].config(state='normal')
        self.entries['customer_id'].delete(0, tk.END)
        self.entries['customer_id'].insert(0, full_data['customer_id'])
        self.entries['customer_id'].config(state='disabled')

        self.entries['name'].delete(0, tk.END)
        self.entries['name'].insert(0, full_data['name'])

        self.entries['group'].delete(0, tk.END)
        self.entries['group'].insert(0, full_data['group'])

        self.gender_var.set(full_data['gender'])

        self.entries['phone'].delete(0, tk.END)
        self.entries['phone'].insert(0, full_data['phone'])

        self.entries['email'].delete(0, tk.END)
        self.entries['email'].insert(0, full_data['email'])

        self.entries['customer_type'].set(full_data['customer_type'])

        self.entries['cmnd'].delete(0, tk.END)
        self.entries['cmnd'].insert(0, full_data['cmnd'])

        self.entries['birth_date'].delete(0, tk.END)
        self.entries['birth_date'].insert(0, full_data['birth_date'])

        self.entries['address'].delete(0, tk.END)
        self.entries['address'].insert(0, full_data['address'])

        self.entries['product'].set(full_data['product'])

        self.entries['quantity'].delete(0, tk.END)
        self.entries['quantity'].insert(0, full_data['quantity'])

        self.entries['unit_price'].config(state='normal')
        self.entries['unit_price'].delete(0, tk.END)
        self.entries['unit_price'].insert(0, full_data['unit_price'])
        self.entries['unit_price'].config(state='readonly')

        self.entries['total_amount'].config(state='normal')
        self.entries['total_amount'].delete(0, tk.END)
        self.entries['total_amount'].insert(0, full_data['total_amount'])
        self.entries['total_amount'].config(state='readonly')



    def update_customer(self):
        """Cập nhật thông tin khách hàng"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần sửa")
            return

        if not self.validate_form():
            return

        try:
            customer_data = self.get_form_data()
            customer_id = customer_data['customer_id']
            print(">>> customer_id từ form:", repr(customer_id))
            print(">>> Danh sách ID trong model:", [repr(c['customer_id']) for c in self.customer_controller.model.customers])

            # ✅ Gọi controller để cập nhật dữ liệu trong model + lưu file JSON
            success = self.customer_controller.update_customer(customer_id, customer_data)
            if not success:
                messagebox.showerror("Lỗi", "Không thể cập nhật vào dữ liệu")
                return

            # ✅ Cập nhật TreeView
            item = selection[0]
            values = (
                customer_data.get('customer_id'),
                customer_data.get('name'),
                customer_data.get('group'),
                customer_data.get('gender'),
                customer_data.get('phone'),
                customer_data.get('email'),
                customer_data.get('customer_type'),
                customer_data.get('product'),
                customer_data.get('quantity'),
                customer_data.get('total_amount'),
                customer_data.get('cmnd'),
                customer_data.get('unit_price'),
                customer_data.get('address'),
                customer_data.get('birth_date')
                
            )
            self.tree.item(item, values=values)

            # ✅ Cập nhật lại lọc nhóm nếu có thay đổi
            self.update_group_filter()

            messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng!")

        except Exception as e:
            print("Chi tiết lỗi:", repr(e))  # 👉 dòng in lỗi chi tiết ra console
            messagebox.showerror("Lỗi", f"Không thể cập nhật okeoke: {str(e)}")


    def delete_customer(self):
        """Xóa khách hàng"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng cần xóa")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa khách hàng này?"):
            try:
                # Lấy customer_id từ item được chọn
                selected_item = selection[0]
                customer_id = self.tree.item(selected_item, 'values')[0]  # Cột đầu tiên là customer_id
                
                # Gọi hàm xóa trong controller
                self.customer_controller.delete_customer(customer_id)

                # Xóa trên giao diện
                self.tree.delete(selected_item)
                self.clear_form()
                self.update_group_filter()

                messagebox.showinfo("Thành công", "Đã xóa khách hàng!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")

    def search_customers(self):
        """Tìm kiếm khách hàng theo từ khóa mờ (partial match)"""
        search_type = self.search_type.get()
        search_value = self.search_var.get().strip().lower()

        if not search_value:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm")
            return

        # Xóa dữ liệu cũ trong TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ánh xạ loại tìm kiếm sang field
        search_columns = {
            'ID Khách hàng': 'customer_id',
            'Tên KH': 'name',
            'SĐT': 'phone',
            'Email': 'email'
        }

        field = search_columns.get(search_type, 'customer_id')
        found_count = 0

        # ✅ Duyệt danh sách gốc lưu trữ
        for customer in self.all_customers_data:
            field_value = str(customer.get(field, '')).lower()
            if search_value in field_value:
                values = (
                    customer['customer_id'],
                    customer['name'],
                    customer['group'],
                    customer['gender'],
                    customer['phone'],
                    customer['email'],
                    customer['customer_type'],
                    customer['product'],
                    customer['quantity'],
                    customer['total_amount'],
                    customer['cmnd'],
                    customer['birth_date'],
                    customer['address']
                )
                self.tree.insert('', tk.END, values=values)
                found_count += 1

        if found_count == 0:
            messagebox.showinfo("Kết quả", "Không tìm thấy khách hàng nào")
        else:
            messagebox.showinfo("Kết quả", f"Tìm thấy {found_count} khách hàng")


            
    def get_all_customers(self):
        """Lấy tất cả khách hàng từ TreeView"""
        customers = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            customers.append(values)
        return customers
    def show_all_customers(self):
        """Hiển thị tất cả khách hàng"""
        try:
            all_customers = self.customer_controller.get_all_customers()
            self.all_customers_data = all_customers
            print(f"DEBUG - Số khách hàng lấy được: {len(all_customers)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy danh sách khách hàng: {str(e)}")
            return

        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Hiển thị dữ liệu mới
        if all_customers:
            for customer_data in all_customers:
                try:
                    values = (
    customer_data.get('customer_id'),
    customer_data.get('name'),
    customer_data.get('group'),
    customer_data.get('gender'),
    customer_data.get('phone'),
    customer_data.get('email'),
    customer_data.get('customer_type'),
    customer_data.get('product'),
    customer_data.get('quantity'),
    customer_data.get('total_amount'),
    customer_data.get('cmnd'),
    customer_data.get('birth_date'),  # ✅ ngày sinh đúng vị trí
    customer_data.get('address')
)
                    self.tree.insert('', tk.END, values=values)
                except Exception as insert_err:
                    print(f"Lỗi khi hiển thị khách hàng: {insert_err}")
        else:
            self.load_sample_customers()


    def get_customers_from_tree(self):
        """Lấy dữ liệu hiện có trong TreeView (nếu cần xuất file, v.v.)"""
        customers = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            customers.append(values)
        return customers

    def filter_by_customer_type(self):
        """Lọc theo loại khách hàng (Thường/VIP)"""
        cust_type = self.type_filter.get()
        if not cust_type:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn loại khách hàng")
            return

        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lọc dữ liệu trong all_customers_data
        found = 0
        for customer in self.all_customers_data:
            if customer['customer_type'] == cust_type:
                values = (
                    customer['customer_id'],
                    customer['name'],
                    customer['group'],
                    customer['gender'],
                    customer['phone'],
                    customer['email'],
                    customer['customer_type'],
                    customer['product'],
                    customer['quantity'],
                    customer['total_amount'],
                    customer['cmnd'],
                    customer['birth_date'],
                    customer['address']
                )
                self.tree.insert('', tk.END, values=values)
                found += 1

        if found == 0:
            messagebox.showinfo("Kết quả", f"Không tìm thấy khách hàng loại '{cust_type}'")


    def update_group_filter(self):
        """Cập nhật combobox filter nhóm"""
        groups = set()
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if len(values) > 2 and values[2]:
                groups.add(values[2])
        
        self.group_filter['values'] = sorted(list(groups))
    def load_sample_data(self):
        """Tạo 10 dữ liệu mẫu và thêm vào hệ thống"""
        try:
            # Dữ liệu mẫu
            sample_customers = [
                {
                    'customer_id': f'KH{1001 + i}',
                    'name': name,
                    'group': group,
                    'gender': gender,
                    'phone': f'09{str(10000000 + i * 11111111)[:8]}',
                    'email': f'{name.lower().replace(" ", ".")}@email.com',
                    'customer_type': cust_type,
                    'cmnd': f'{200000000 + i * 11111111}',
                    'birth_date': birth_date,
                    'address': address,
                    'product': product,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_amount': quantity * unit_price
                }
                for i, (name, group, gender, cust_type, birth_date, address, product, quantity, unit_price) in enumerate([
                    ('Nguyễn Thị Lan', 'Thường', 'Nữ', 'Thường', '12/03/1990', 'Hà Nội', 'iMac 27"', 1, 45000000),
    ('Phạm Văn Bảo', 'VIP', 'Nam', 'VIP', '03/06/1986', 'HCM', 'PlayStation 5', 2, 15000000),
    ('Lê Thị Mai', 'Thường', 'Nữ', 'Thường', '25/12/1991', 'Cần Thơ', 'Xbox Series X', 1, 13000000),
    ('Trần Quang Huy', 'VIP', 'Nam', 'VIP', '09/09/1984', 'Đà Nẵng', 'Smart TV 4K', 1, 18000000),
    ('Đinh Thị Hạnh', 'Thường', 'Nữ', 'Thường', '17/05/1993', 'Hải Dương', 'HomePod', 2, 8000000),
    ('Hoàng Văn Khải', 'VIP', 'Nam', 'VIP', '11/08/1988', 'Huế', 'SSD 1TB', 3, 3000000),
    ('Trịnh Thị Nhung', 'Thường', 'Nữ', 'Thường', '19/02/1990', 'Vũng Tàu', 'Magic Mouse', 1, 2500000),
    ('Phan Văn Nhật', 'VIP', 'Nam', 'VIP', '28/04/1987', 'Quảng Ninh', 'Mechanical Keyboard', 2, 4000000),
    ('Đào Thị Oanh', 'Thường', 'Nữ', 'Thường', '06/07/1992', 'Đà Lạt', 'Canon DSLR', 1, 22000000),
    ('Nguyễn Văn Phúc', 'VIP', 'Nam', 'VIP', '15/11/1995', 'Bình Dương', 'Microphone Pro', 1, 5000000)
                ])
            ]
            
            # Xác nhận với người dùng
            if messagebox.askyesno("Xác nhận", "Bạn có muốn thêm 10 dữ liệu mẫu vào hệ thống?"):
                added_count = 0
                
                for customer_data in sample_customers:
                    try:
                        # Thêm vào controller
                        self.customer_controller.add_customer(customer_data)
                        
                        # Thêm vào tree
                        self.add_to_tree(customer_data)
                        added_count += 1
                        
                    except Exception as e:
                        print(f"Lỗi khi thêm khách hàng {customer_data['name']}: {str(e)}")
                        continue
                
                # Cập nhật giao diện
                self.update_group_filter()
                
                # Thông báo kết quả
                if added_count > 0:
                    messagebox.showinfo("Thành công", f"Đã thêm {added_count} khách hàng mẫu!")
                    self.clear_form()  # Làm trống form sau khi thêm
                else:
                    messagebox.showerror("Lỗi", "Không thể thêm dữ liệu mẫu")
                    
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo dữ liệu mẫu: {str(e)}")

# SỬA: Cập nhật hàm load_sample_customers để không gọi show_all_customers
    def load_sample_customers(self):
        

        # 💥 Hiển thị dữ liệu ngay sau khi thêm
        self.show_all_customers()
        self.update_group_filter()