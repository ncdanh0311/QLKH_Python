# views/market_analysis_view.py
import tkinter as tk
from tkinter import messagebox, ttk
import requests
import threading
from datetime import datetime
import json
import random

class MarketAnalysisView:
    def __init__(self, parent_window=None, on_back_callback=None):
        self.parent_window = parent_window
        self.on_back_callback = on_back_callback  # Callback để trở về
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.root.title("Đánh Giá Thị Trường")
        
        # Thiết lập fullscreen
        self.root.state('zoomed')  # Windows
        # Hoặc dùng: self.root.attributes('-fullscreen', True)  # Linux/Mac
        
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)
        
        # Bind phím ESC để thoát fullscreen
        self.root.bind('<Escape>', self.toggle_fullscreen)
        self.root.bind('<F11>', self.toggle_fullscreen)
        
        # Biến để theo dõi trạng thái fullscreen
        self.is_fullscreen = True
        
        # Data storage
        self.market_data = {}
        
        self.setup_ui()
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode với phím ESC hoặc F11"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.root.state('zoomed')  # Windows fullscreen
            # self.root.attributes('-fullscreen', True)  # Linux/Mac fullscreen
        else:
            self.root.state('normal')  # Windows windowed
            # self.root.attributes('-fullscreen', False)  # Linux/Mac windowed
            self.root.geometry("1000x700")
            self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
    
    def run(self):
        self.root.mainloop()
    
    def setup_ui(self):
        # HEADER
        header_frame = tk.Frame(self.root, bg="#0f3460", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="📈 ĐÁNH GIÁ THỊ TRƯỜNG CÔNG NGHỆ",
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#0f3460"
        )
        header_label.pack(pady=20)
        
        # MAIN CONTENT
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Control Panel
        control_frame = tk.Frame(main_frame, bg="#16213e", relief="raised", bd=2)
        control_frame.pack(fill="x", pady=(0, 20))
        
        control_label = tk.Label(
            control_frame,
            text="🎛️ Bảng Điều Khiển",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#16213e"
        )
        control_label.pack(pady=10)
        
        # Buttons Panel
        buttons_frame = tk.Frame(control_frame, bg="#16213e")
        buttons_frame.pack(pady=10)
        
        # Button style
        button_style = {
            "font": ("Segoe UI", 11, "bold"),
            "fg": "white",
            "relief": "flat",
            "bd": 0,
            "padx": 20,
            "pady": 8,
            "cursor": "hand2"
        }
        
        # Các nút chức năng
        btn_exchange = tk.Button(
            buttons_frame,
            text="💱 Tỷ Giá Ngoại Tệ",
            bg="#3498db",
            activebackground="#2980b9",
            command=self.get_exchange_rates,
            **button_style
        )
        btn_exchange.pack(side="left", padx=10)
        
        btn_tech = tk.Button(
            buttons_frame,
            text="💻 Giá Sản Phẩm Tech",
            bg="#9b59b6",
            activebackground="#8e44ad",
            command=self.get_tech_prices,
            **button_style
        )
        btn_tech.pack(side="left", padx=10)
        
        btn_crypto = tk.Button(
            buttons_frame,
            text="₿ Tiền Điện Tử",
            bg="#e74c3c",
            activebackground="#c0392b",
            command=self.get_crypto_prices,
            **button_style
        )
        btn_crypto.pack(side="left", padx=10)
        
        btn_weather = tk.Button(
            buttons_frame,
            text="🌤️ Thời Tiết",
            bg="#f39c12",
            activebackground="#e67e22",
            command=self.get_weather_data,
            **button_style
        )
        btn_weather.pack(side="left", padx=10)
        
        btn_refresh = tk.Button(
            buttons_frame,
            text="🔄 Làm Mới Tất Cả",
            bg="#27ae60",
            activebackground="#229954",
            command=self.refresh_all_data,
            **button_style
        )
        btn_refresh.pack(side="left", padx=10)
        btn_back = tk.Button(
            buttons_frame,
            text="🔙 Trở Về",
            bg="#95a5a6",
            activebackground="#7f8c8d",
            command=self.go_back,
            **button_style
        )
        btn_back.pack(side="right", padx=10)
        # Progress Bar
        self.progress = ttk.Progressbar(
            control_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(
            control_frame,
            text="⚡ Sẵn sàng lấy dữ liệu thị trường",
            font=("Segoe UI", 10),
            fg="#a8d8ea",
            bg="#16213e"
        )
        self.status_label.pack(pady=5)
        
        # DATA DISPLAY AREA
        display_frame = tk.Frame(main_frame, bg="#1a1a2e")
        display_frame.pack(fill="both", expand=True)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(display_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Style cho notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background="#1a1a2e")
        style.configure('TNotebook.Tab', background="#16213e", foreground="white", padding=[20, 10])
        
        # Tạo các tab
        self.create_tabs()
        
        # FOOTER
        footer_frame = tk.Frame(self.root, bg="#0f3460", height=40)
        footer_frame.pack(fill="x")
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text=f"📊 Cập nhật lần cuối: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            font=("Segoe UI", 9),
            fg="#a8d8ea",
            bg="#0f3460"
        )
        footer_label.pack(pady=10)
        self.footer_label = footer_label
    def go_back(self):
        """Trở về màn hình chọn chức năng"""
        try:
            if self.on_back_callback:
                # Gọi callback để hiển thị lại màn hình chọn chức năng
                self.on_back_callback()
            
            # Đóng cửa sổ hiện tại
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể trở về: {str(e)}")
    def create_tabs(self):
        # Tab 1: Tỷ giá ngoại tệ
        self.exchange_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(self.exchange_frame, text="💱 Tỷ Giá")
        
        # Tab 2: Sản phẩm công nghệ
        self.tech_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(self.tech_frame, text="💻 Tech")
        
        # Tab 3: Tiền điện tử
        self.crypto_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(self.crypto_frame, text="₿ Crypto")
        
        # Tab 4: Thời tiết
        self.weather_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(self.weather_frame, text="🌤️ Thời Tiết")
        
        # Initialize tab content
        self.init_tab_content()
    
    def init_tab_content(self):
        # Exchange Rate Tab
        exchange_label = tk.Label(
            self.exchange_frame,
            text="💱 Dữ liệu tỷ giá sẽ hiển thị ở đây",
            font=("Segoe UI", 14),
            fg="#a8d8ea",
            bg="#1a1a2e"
        )
        exchange_label.pack(pady=50)
        
        # Tech Tab
        tech_label = tk.Label(
            self.tech_frame,
            text="💻 Dữ liệu giá sản phẩm công nghệ sẽ hiển thị ở đây",
            font=("Segoe UI", 14),
            fg="#a8d8ea",
            bg="#1a1a2e"
        )
        tech_label.pack(pady=50)
        
        # Crypto Tab
        crypto_label = tk.Label(
            self.crypto_frame,
            text="₿ Dữ liệu tiền điện tử sẽ hiển thị ở đây",
            font=("Segoe UI", 14),
            fg="#a8d8ea",
            bg="#1a1a2e"
        )
        crypto_label.pack(pady=50)
        
        # Weather Tab
        weather_label = tk.Label(
            self.weather_frame,
            text="🌤️ Dữ liệu thời tiết sẽ hiển thị ở đây",
            font=("Segoe UI", 14),
            fg="#a8d8ea",
            bg="#1a1a2e"
        )
        weather_label.pack(pady=50)
    
    def start_loading(self, message):
        """Bắt đầu hiển thị loading"""
        self.status_label.config(text=f"⏳ {message}")
        self.progress.start(10)
    
    def stop_loading(self, message):
        """Dừng loading"""
        self.progress.stop()
        self.status_label.config(text=f"✅ {message}")
        self.footer_label.config(text=f"📊 Cập nhật lần cuối: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    def get_exchange_rates(self):
        """Lấy tỷ giá ngoại tệ từ API"""
        def fetch_data():
            try:
                self.start_loading("Đang lấy tỷ giá ngoại tệ...")
                
                # API miễn phí: exchangerate-api.com
                response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
                response.raise_for_status()
                
                data = response.json()
                self.market_data['exchange_rates'] = data
                
                # Update UI in main thread
                self.root.after(0, lambda: self.display_exchange_rates(data))
                
            except requests.exceptions.RequestException as e:
                self.root.after(0, lambda: self.handle_api_error("Tỷ giá", str(e)))
            except Exception as e:
                self.root.after(0, lambda: self.handle_api_error("Tỷ giá", f"Lỗi không xác định: {str(e)}"))
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def display_exchange_rates(self, data):
        """Hiển thị dữ liệu tỷ giá"""
        # Clear previous content
        for widget in self.exchange_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Label(
            self.exchange_frame,
            text=f"💱 TỶ GIÁ NGOẠI TỆ (Gốc: {data['base']})",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        header.pack(pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(self.exchange_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.exchange_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Important currencies for Vietnam
        important_currencies = {
            'VND': 'Việt Nam Đồng',
            'EUR': 'Euro',
            'GBP': 'Bảng Anh',
            'JPY': 'Yên Nhật',
            'CNY': 'Nhân dân tệ',
            'KRW': 'Won Hàn Quốc',
            'THB': 'Baht Thái',
            'SGD': 'Đô la Singapore'
        }
        
        rates = data.get('rates', {})
        
        row = 0
        for currency, name in important_currencies.items():
            if currency in rates:
                rate = rates[currency]
                
                # Currency frame
                curr_frame = tk.Frame(scrollable_frame, bg="#16213e", relief="raised", bd=1)
                curr_frame.grid(row=row//2, column=row%2, padx=10, pady=5, sticky="ew", ipadx=20, ipady=10)
                
                # Currency info
                curr_label = tk.Label(
                    curr_frame,
                    text=f"{currency} - {name}",
                    font=("Segoe UI", 12, "bold"),
                    fg="#ffffff",
                    bg="#16213e"
                )
                curr_label.pack()
                
                rate_label = tk.Label(
                    curr_frame,
                    text=f"1 USD = {rate:,.2f} {currency}" if currency != 'VND' else f"1 USD = {rate:,.0f} {currency}",
                    font=("Segoe UI", 11),
                    fg="#a8d8ea",
                    bg="#16213e"
                )
                rate_label.pack()
                
                row += 1
        
        # Configure grid
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.stop_loading("Đã cập nhật tỷ giá ngoại tệ")
    
    def get_tech_prices(self):
        """Lấy giá sản phẩm công nghệ từ API giả"""
        def fetch_data():
            try:
                self.start_loading("Đang lấy giá sản phẩm công nghệ...")
                
                # Tạo dữ liệu giả vì không có API miễn phí cho giá sản phẩm
                tech_products = {
                    "laptop_gaming": {
                        "name": "💻 Laptop Gaming RTX 4060",
                        "price": random.randint(25000000, 35000000),
                        "change": random.uniform(-5, 8),
                        "brand": "ASUS ROG",
                        "category": "Gaming Laptop"
                    },
                    "iphone_15_pro": {
                        "name": "📱 iPhone 15 Pro 256GB",
                        "price": random.randint(28000000, 32000000),
                        "change": random.uniform(-3, 5),
                        "brand": "Apple",
                        "category": "Smartphone"
                    },
                    "airpods_pro": {
                        "name": "🎧 AirPods Pro 2nd Gen",
                        "price": random.randint(5500000, 6500000),
                        "change": random.uniform(-2, 4),
                        "brand": "Apple",
                        "category": "Audio"
                    },
                    "apple_watch": {
                        "name": "⌚ Apple Watch Series 9",
                        "price": random.randint(9000000, 12000000),
                        "change": random.uniform(-1, 6),
                        "brand": "Apple",
                        "category": "Wearable"
                    },
                    "imac_27": {
                        "name": "🖥️ iMac 24\" M3 Chip",
                        "price": random.randint(35000000, 45000000),
                        "change": random.uniform(-4, 3),
                        "brand": "Apple",
                        "category": "Desktop"
                    },
                    "ipad_pro": {
                        "name": "📟 iPad Pro 12.9\" M2",
                        "price": random.randint(25000000, 35000000),
                        "change": random.uniform(-2, 7),
                        "brand": "Apple",
                        "category": "Tablet"
                    },
                    "ps5": {
                        "name": "🎮 PlayStation 5",
                        "price": random.randint(12000000, 15000000),
                        "change": random.uniform(-6, 10),
                        "brand": "Sony",
                        "category": "Gaming Console"
                    },
                    "xbox_series_x": {
                        "name": "🕹️ Xbox Series X",
                        "price": random.randint(12000000, 14000000),
                        "change": random.uniform(-4, 8),
                        "brand": "Microsoft",
                        "category": "Gaming Console"
                    }
                }
                
                # Simulate API delay
                threading.Event().wait(2)
                
                self.market_data['tech_prices'] = tech_products
                self.root.after(0, lambda: self.display_tech_prices(tech_products))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_api_error("Sản phẩm công nghệ", str(e)))
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def display_tech_prices(self, data):
        """Hiển thị giá sản phẩm công nghệ"""
        # Clear previous content
        for widget in self.tech_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Label(
            self.tech_frame,
            text="💻 GIÁ SẢN PHẨM CÔNG NGHỆ",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        header.pack(pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(self.tech_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tech_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        row = 0
        for product_id, product_data in data.items():
            # Product frame
            product_frame = tk.Frame(scrollable_frame, bg="#16213e", relief="raised", bd=2)
            product_frame.grid(row=row//2, column=row%2, padx=15, pady=10, sticky="nsew", ipadx=20, ipady=15)
            
            # Product name
            name_label = tk.Label(
                product_frame,
                text=product_data['name'],
                font=("Segoe UI", 14, "bold"),
                fg="#ffffff",
                bg="#16213e"
            )
            name_label.pack()
            
            # Brand
            brand_label = tk.Label(
                product_frame,
                text=f"🏷️ {product_data['brand']}",
                font=("Segoe UI", 10),
                fg="#a8d8ea",
                bg="#16213e"
            )
            brand_label.pack()
            
            # Price
            price_label = tk.Label(
                product_frame,
                text=f"{product_data['price']:,} VNĐ",
                font=("Segoe UI", 16, "bold"),
                fg="#27ae60",
                bg="#16213e"
            )
            price_label.pack(pady=5)
            
            # Price change
            change = product_data['change']
            change_color = "#27ae60" if change >= 0 else "#e74c3c"
            change_symbol = "📈" if change >= 0 else "📉"
            
            change_label = tk.Label(
                product_frame,
                text=f"{change_symbol} {change:+.2f}%",
                font=("Segoe UI", 11),
                fg=change_color,
                bg="#16213e"
            )
            change_label.pack()
            
            # Category
            category_label = tk.Label(
                product_frame,
                text=f"📂 {product_data['category']}",
                font=("Segoe UI", 9),
                fg="#95a5a6",
                bg="#16213e"
            )
            category_label.pack(pady=(5, 0))
            
            row += 1
        
        # Configure grid
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.stop_loading("Đã cập nhật giá sản phẩm công nghệ")
    
    def get_crypto_prices(self):
        """Lấy giá tiền điện tử từ API"""
        def fetch_data():
            try:
                self.start_loading("Đang lấy giá tiền điện tử...")
                
                # API miễn phí: CoinGecko
                response = requests.get(
                    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,cardano,solana&vs_currencies=usd&include_24hr_change=true",
                    timeout=10
                )
                response.raise_for_status()
                
                data = response.json()
                self.market_data['crypto_prices'] = data
                
                self.root.after(0, lambda: self.display_crypto_prices(data))
                
            except requests.exceptions.RequestException as e:
                self.root.after(0, lambda: self.handle_api_error("Tiền điện tử", str(e)))
            except Exception as e:
                self.root.after(0, lambda: self.handle_api_error("Tiền điện tử", str(e)))
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def display_crypto_prices(self, data):
        """Hiển thị giá tiền điện tử"""
        # Clear previous content
        for widget in self.crypto_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Label(
            self.crypto_frame,
            text="₿ GIÁ TIỀN ĐIỆN TỬ",
            font=("Segoe UI", 18, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        )
        header.pack(pady=20)
        
        # Crypto info
        crypto_info = {
            'bitcoin': {'name': 'Bitcoin', 'symbol': '₿', 'color': '#f7931a'},
            'ethereum': {'name': 'Ethereum', 'symbol': 'Ξ', 'color': '#627eea'},
            'binancecoin': {'name': 'BNB', 'symbol': 'BNB', 'color': '#f3ba2f'},
            'cardano': {'name': 'Cardano', 'symbol': 'ADA', 'color': '#0033ad'},
            'solana': {'name': 'Solana', 'symbol': 'SOL', 'color': '#9945ff'}
        }
        
        # Main container
        main_container = tk.Frame(self.crypto_frame, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        row = 0
        for crypto_id, info in crypto_info.items():
            if crypto_id in data:
                crypto_data = data[crypto_id]
                price = crypto_data.get('usd', 0)
                change_24h = crypto_data.get('usd_24h_change', 0)
                
                # Crypto frame
                crypto_frame = tk.Frame(main_container, bg="#16213e", relief="raised", bd=2)
                crypto_frame.grid(row=row//2, column=row%2, padx=15, pady=10, sticky="nsew", ipadx=20, ipady=15)
                
                # Crypto name and symbol
                name_label = tk.Label(
                    crypto_frame,
                    text=f"{info['symbol']} {info['name']}",
                    font=("Segoe UI", 14, "bold"),
                    fg=info['color'],
                    bg="#16213e"
                )
                name_label.pack()
                
                # Price
                price_label = tk.Label(
                    crypto_frame,
                    text=f"${price:,.2f}",
                    font=("Segoe UI", 16, "bold"),
                    fg="#ffffff",
                    bg="#16213e"
                )
                price_label.pack(pady=5)
                
                # 24h change
                change_color = "#27ae60" if change_24h >= 0 else "#e74c3c"
                change_symbol = "📈" if change_24h >= 0 else "📉"
                
                change_label = tk.Label(
                    crypto_frame,
                    text=f"{change_symbol} {change_24h:.2f}%",
                    font=("Segoe UI", 11),
                    fg=change_color,
                    bg="#16213e"
                )
                change_label.pack()
                
                row += 1
        
        # Configure grid
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        self.stop_loading("Đã cập nhật giá tiền điện tử")
    
    def get_weather_data(self):
        """Lấy dữ liệu thời tiết từ API"""
        def fetch_data():
            try:
                self.start_loading("Đang lấy dữ liệu thời tiết...")
                
                # API thời tiết miễn phí: OpenWeatherMap (cần API key)
                # Hoặc sử dụng dữ liệu giả cho demo
                weather_data = {
                    "location": "Hồ Chí Minh",
                    "temperature": random.randint(25, 35),
                    "humidity": random.randint(60, 85),
                    "description": random.choice(["Nắng", "Có mây", "Mưa nhẹ", "Nắng gắt"]),
                    "wind_speed": random.randint(5, 20),
                    "pressure": random.randint(1010, 1025),
                    "visibility": random.randint(8, 15)
                }
                
                # Simulate API delay
                threading.Event().wait(1.5)
                
                self.market_data['weather_data'] = weather_data
                self.root.after(0, lambda: self.display_weather_data(weather_data))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_api_error("Thời tiết", str(e)))
        
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def display_weather_data(self, data):
        """Hiển thị dữ liệu thời tiết"""
        # Clear previous content
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = tk.Frame(self.weather_frame, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Weather title
        title_frame = tk.Frame(main_container, bg="#1a1a2e")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text=f"🌤️ THỜI TIẾT {data['location'].upper()}",
            font=("Segoe UI", 20, "bold"),
            fg="#3498db",
            bg="#1a1a2e"
        )
        title_label.pack()
        
        # Weather info grid
        info_frame = tk.Frame(main_container, bg="#1a1a2e")
        info_frame.pack(pady=30)
        
        # Temperature
        temp_frame = tk.Frame(info_frame, bg="#16213e", relief="raised", bd=2)
        temp_frame.grid(row=0, column=0, padx=20, pady=10, ipadx=30, ipady=20)
        
        temp_label = tk.Label(
            temp_frame,
            text="🌡️ Nhiệt độ",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#16213e"
        )
        temp_label.pack()
        
        temp_value = tk.Label(
            temp_frame,
            text=f"{data['temperature']}°C",
            font=("Segoe UI", 18, "bold"),
            fg="#e74c3c",
            bg="#16213e"
        )
        temp_value.pack()
        
        # Humidity
        humidity_frame = tk.Frame(info_frame, bg="#16213e", relief="raised", bd=2)
        humidity_frame.grid(row=0, column=1, padx=20, pady=10, ipadx=30, ipady=20)
        
        humidity_label = tk.Label(
            humidity_frame,
            text="💧 Độ ẩm",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#16213e"
        )
        humidity_label.pack()
        
        humidity_value = tk.Label(
            humidity_frame,
            text=f"{data['humidity']}%",
            font=("Segoe UI", 18, "bold"),
            fg="#3498db",
            bg="#16213e"
        )
        humidity_value.pack()
        
        # Wind Speed
        wind_frame = tk.Frame(info_frame, bg="#16213e", relief="raised", bd=2)
        wind_frame.grid(row=1, column=0, padx=20, pady=10, ipadx=30, ipady=20)
        
        wind_label = tk.Label(
            wind_frame,
            text="💨 Gió",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#16213e"
        )
        wind_label.pack()
        
        wind_value = tk.Label(
            wind_frame,
            text=f"{data['wind_speed']} km/h",
            font=("Segoe UI", 18, "bold"),
            fg="#27ae60",
            bg="#16213e"
        )
        wind_value.pack()
        
        # Description
        desc_frame = tk.Frame(info_frame, bg="#16213e", relief="raised", bd=2)
        desc_frame.grid(row=1, column=1, padx=20, pady=10, ipadx=30, ipady=20)
        
        desc_label = tk.Label(
            desc_frame,
            text="☁️ Tình trạng",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#16213e"
        )
        desc_label.pack()
        
        desc_value = tk.Label(
            desc_frame,
            text=data['description'],
            font=("Segoe UI", 14, "bold"),
            fg="#f39c12",
            bg="#16213e"
        )
        desc_value.pack()
        
        # Additional info
        additional_frame = tk.Frame(main_container, bg="#1a1a2e")
        additional_frame.pack(pady=30)
        
        # Pressure
        pressure_frame = tk.Frame(additional_frame, bg="#16213e", relief="raised", bd=2)
        pressure_frame.grid(row=0, column=0, padx=20, pady=10, ipadx=30, ipady=15)
        
        pressure_label = tk.Label(
            pressure_frame,
            text=f"📊 Áp suất: {data['pressure']} hPa",
            font=("Segoe UI", 12),
            fg="#a8d8ea",
            bg="#16213e"
        )
        pressure_label.pack()
        
        # Visibility
        visibility_frame = tk.Frame(additional_frame, bg="#16213e", relief="raised", bd=2)
        visibility_frame.grid(row=0, column=1, padx=20, pady=10, ipadx=30, ipady=15)
        
        visibility_label = tk.Label(
            visibility_frame,
            text=f"👁️ Tầm nhìn: {data['visibility']} km",
            font=("Segoe UI", 12),
            fg="#a8d8ea",
            bg="#16213e"
        )
        visibility_label.pack()
        
        self.stop_loading("Đã cập nhật dữ liệu thời tiết")
    
    def refresh_all_data(self):
        """Làm mới tất cả dữ liệu"""
        def refresh_sequence():
            try:
                self.start_loading("Đang làm mới tất cả dữ liệu...")
                
                # Refresh exchange rates
                response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.market_data['exchange_rates'] = data
                    self.root.after(0, lambda: self.display_exchange_rates(data))
                
                threading.Event().wait(1)
                
                # Refresh crypto prices
                response = requests.get(
                    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,cardano,solana&vs_currencies=usd&include_24hr_change=true",
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    self.market_data['crypto_prices'] = data
                    self.root.after(0, lambda: self.display_crypto_prices(data))
                
                threading.Event().wait(1)
                
                # Refresh tech prices (simulated data)
                tech_products = {
                    "laptop_gaming": {
                        "name": "💻 Laptop Gaming RTX 4060",
                        "price": random.randint(25000000, 35000000),
                        "change": random.uniform(-5, 8),
                        "brand": "ASUS ROG",
                        "category": "Gaming Laptop"
                    },
                    "iphone_15_pro": {
                        "name": "📱 iPhone 15 Pro 256GB",
                        "price": random.randint(28000000, 32000000),
                        "change": random.uniform(-3, 5),
                        "brand": "Apple",
                        "category": "Smartphone"
                    },
                    "airpods_pro": {
                        "name": "🎧 AirPods Pro 2nd Gen",
                        "price": random.randint(5500000, 6500000),
                        "change": random.uniform(-2, 4),
                        "brand": "Apple",
                        "category": "Audio"
                    },
                    "apple_watch": {
                        "name": "⌚ Apple Watch Series 9",
                        "price": random.randint(9000000, 12000000),
                        "change": random.uniform(-1, 6),
                        "brand": "Apple",
                        "category": "Wearable"
                    },
                    "imac_27": {
                        "name": "🖥️ iMac 24\" M3 Chip",
                        "price": random.randint(35000000, 45000000),
                        "change": random.uniform(-4, 3),
                        "brand": "Apple",
                        "category": "Desktop"
                    },
                    "ipad_pro": {
                        "name": "📟 iPad Pro 12.9\" M2",
                        "price": random.randint(25000000, 35000000),
                        "change": random.uniform(-2, 7),
                        "brand": "Apple",
                        "category": "Tablet"
                    },
                    "ps5": {
                        "name": "🎮 PlayStation 5",
                        "price": random.randint(12000000, 15000000),
                        "change": random.uniform(-6, 10),
                        "brand": "Sony",
                        "category": "Gaming Console"
                    },
                    "xbox_series_x": {
                        "name": "🕹️ Xbox Series X",
                        "price": random.randint(12000000, 14000000),
                        "change": random.uniform(-4, 8),
                        "brand": "Microsoft",
                        "category": "Gaming Console"
                    }
                }
                
                self.market_data['tech_prices'] = tech_products
                self.root.after(0, lambda: self.display_tech_prices(tech_products))
                
                threading.Event().wait(1)
                
                # Refresh weather data (simulated)
                weather_data = {
                    "location": "Hồ Chí Minh",
                    "temperature": random.randint(25, 35),
                    "humidity": random.randint(60, 85),
                    "description": random.choice(["Nắng", "Có mây", "Mưa nhẹ", "Nắng gắt"]),
                    "wind_speed": random.randint(5, 20),
                    "pressure": random.randint(1010, 1025),
                    "visibility": random.randint(8, 15)
                }
                
                self.market_data['weather_data'] = weather_data
                self.root.after(0, lambda: self.display_weather_data(weather_data))
                
                self.root.after(0, lambda: self.stop_loading("Đã làm mới tất cả dữ liệu thành công"))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_api_error("Làm mới dữ liệu", str(e)))
        
        threading.Thread(target=refresh_sequence, daemon=True).start()
    
    def handle_api_error(self, api_name, error_message):
        """Xử lý lỗi API"""
        self.stop_loading(f"Lỗi khi lấy dữ liệu {api_name}")
        
        error_msg = f"Không thể lấy dữ liệu {api_name}:\n{error_message}"
        messagebox.showerror("Lỗi API", error_msg)
    
    def export_data(self):
        """Xuất dữ liệu ra file JSON"""
        try:
            if not self.market_data:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
                return
            
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Lưu dữ liệu thị trường"
            )
            
            if filename:
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": self.market_data
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu:\n{str(e)}")
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ - không cần hỏi xác nhận"""
        self.root.quit()
        self.root.destroy()

# Main execution
if __name__ == "__main__":
    try:
        app = MarketAnalysisView()
        app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.run()
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")
        import traceback
        traceback.print_exc()