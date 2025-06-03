# ỨNG DỤNG QUẢN LÝ KHÁCH HÀNG

## 📝 Giới thiệu

Đây là một ứng dụng quản lý khách hàng đa năng được xây dựng bằng Python và thư viện Tkinter, giúp doanh nghiệp dễ dàng quản lý thông tin khách hàng, theo dõi doanh số, tạo báo cáo và phân tích thị trường.

## ✨ Tính năng chính

* **Quản lý Khách hàng (CRUD):** Thêm, sửa, xóa, tìm kiếm thông tin khách hàng một cách hiệu quả.
* **Thống kê & Báo cáo:** Cung cấp các báo cáo tổng quan và chi tiết về khách hàng, doanh thu.
* **Biểu đồ Doanh số:** Trực quan hóa dữ liệu bán hàng qua các loại biểu đồ sinh động.
* **Phân tích Thị trường:** Cập nhật thông tin thị trường theo thời gian thực (tỷ giá, giá sản phẩm, tiền điện tử, thời tiết).
* **Hệ thống Đăng nhập & Đăng ký:** Bảo mật ứng dụng bằng chức năng đăng nhập người dùng và cho phép tạo tài khoản mới.

## 🛠️ Công nghệ & Công cụ

* **Ngôn ngữ lập trình:** Python 3.x
* **Thư viện:**
    * `tkinter`: Xây dựng giao diện người dùng đồ họa.
    * `json`: Lưu trữ và quản lý dữ liệu tài khoản (`taikhoan.json`) và khách hàng (`customers.json`).
    * `Pillow` (PIL Fork): Xử lý hình ảnh (icon).
    * `matplotlib`: Vẽ biểu đồ (nếu có).
    * `numpy`: Hỗ trợ tính toán số học cho `matplotlib`.
    * `requests`: Gọi API (nếu có các tính năng phân tích thị trường).
    * `os`, `sys`, `datetime`, `collections`, `logging`, `messagebox`.
* **Kiến trúc:** Model-View-Controller (MVC).
* **IDE khuyến nghị:** Visual Studio Code, PyCharm.
* **Quản lý phiên bản:** Git/GitHub.
* **API sử dụng (ví dụ):**
    * `requests` được sử dụng cho chức năng phân tích thị trường (cần tích hợp API cụ thể như Exchange Rate API, CoinGecko API, OpenWeatherMap API).

## 🚀 Hướng dẫn Cài đặt & Chạy ứng dụng

Để chạy ứng dụng này trên máy tính của bạn, hãy làm theo các bước sau:

### 1. Yêu cầu hệ thống

* Đảm bảo bạn đã cài đặt **Python 3.x** trên máy tính. Bạn có thể tải Python từ trang chủ chính thức: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2. Cấu trúc thư mục (quan trọng)

Đảm bảo cấu trúc thư mục dự án của bạn giống như sau để ứng dụng có thể tìm thấy các thành phần và dữ liệu:


![Screenshot 2025-06-03 090542](https://github.com/user-attachments/assets/4b33a1c8-5e8e-4f95-b9fd-20852dcf16b4)

### 3. Tải mã nguồn

* **Cách 1: Sao chép (Clone) từ GitHub (Nếu dự án của bạn nằm trên GitHub)**
    ```bash
    git clone [đường_dẫn_đến_repo_của_bạn]
    cd [tên_thư_mục_dự_án]
    ```
* **Cách 2: Tải xuống file ZIP (Nếu bạn có file ZIP)**
    * Tải xuống file ZIP chứa mã nguồn của dự án.
    * Giải nén file ZIP vào một thư mục bất kỳ trên máy tính của bạn.

### 4. Cài đặt các thư viện cần thiết

* Mở Terminal (trên macOS/Linux) hoặc Command Prompt/PowerShell (trên Windows).
* Điều hướng đến thư mục gốc của dự án (nơi chứa file `main.py`).
* Chạy lệnh sau để cài đặt tất cả các thư viện:
    ```bash
    pip install Pillow matplotlib numpy requests
    ```
    (Lưu ý: `tkinter` thường được cài đặt sẵn cùng Python)

### 5. Chuẩn bị dữ liệu

* Ứng dụng sẽ tự động tạo file `data/taikhoan.json` và `data/customers.json` nếu chúng không tồn tại, với dữ liệu mặc định.
* **Tài khoản mặc định ban đầu:**
    * `admin` / `123`
    * `user` / `123`

### 6. Chạy ứng dụng

* Trong Terminal/Command Prompt/PowerShell, đảm bảo bạn đang ở thư mục gốc của dự án.
* Chạy lệnh sau:
    ```bash
    python main.py
    ```

## 🖥️ Hướng dẫn Sử dụng ứng dụng

### 1. Màn hình Đăng nhập

* Khi ứng dụng khởi chạy, bạn sẽ thấy màn hình đăng nhập.
* **Tên đăng nhập & Mật khẩu:** Nhập thông tin đăng nhập vào các ô tương ứng.
* Nhấn nút **"ĐĂNG NHẬP"** hoặc nhấn phím **Enter** để đăng nhập.
* **"Nhớ mật khẩu"**: Một ô checkbox, chức năng này hiện tại chỉ là placeholder và chưa được triển khai lưu trữ an toàn.
* **"Tạo tài khoản mới"**: Nhấn vào nút này để chuyển đến màn hình đăng ký tài khoản mới.

### 2. Màn hình Đăng ký Tài khoản mới

* Màn hình này cho phép bạn tạo một tài khoản người dùng mới.
* **Tên đăng nhập**: Nhập tên đăng nhập bạn muốn tạo (phải là duy nhất).
* **Mật khẩu**: Nhập mật khẩu.
* **Xác nhận mật khẩu**: Nhập lại mật khẩu để đảm bảo khớp.
* **Vai trò**:
    * Nếu bạn đang đăng nhập với tài khoản `admin` và truy cập màn hình này, bạn có thể chọn vai trò cho tài khoản mới là `User` hoặc `Admin`.
    * Nếu bạn truy cập màn hình này từ màn hình đăng nhập (chưa đăng nhập với vai trò `admin`), bạn chỉ có thể tạo tài khoản `User`.
* Nhấn nút **"ĐĂNG KÝ"** hoặc nhấn phím **Enter** để hoàn tất đăng ký.
* Nếu đăng ký thành công, một thông báo sẽ hiện ra và bạn sẽ được tự động đưa trở lại màn hình đăng nhập.
* Nhấn nút **"Quay Lại Đăng Nhập"** để hủy và trở về màn hình đăng nhập.

### 3. Màn hình Chọn chức năng chính

* Sau khi đăng nhập thành công, bạn sẽ được đưa đến màn hình chính để lựa chọn các chức năng:
    * **Quản lý Khách hàng:** Mở giao diện quản lý thông tin khách hàng (thêm, sửa, xóa, tìm kiếm).
    * **Đánh giá Thị trường:** Mở giao diện để phân tích dữ liệu thị trường (dữ liệu mẫu hoặc từ API).
    * **Báo cáo Cửa hàng:** Mở giao diện hiển thị các báo cáo thống kê về khách hàng và doanh thu.
    * **Thống kê Sản phẩm:** Mở giao diện biểu đồ thống kê sản phẩm bán chạy.
    * **Đăng xuất:** Đăng xuất khỏi hệ thống và quay lại màn hình đăng nhập.
* Cửa sổ sẽ tự động chuyển sang chế độ toàn màn hình.

### 4. Các chức năng chi tiết

#### 4.1. Quản lý Khách hàng

* **Thêm khách hàng:**
    * Điền đầy đủ thông tin vào các trường nhập liệu (ID khách hàng sẽ được tạo tự động).
    * Nhấn nút **"Thêm khách hàng"**.
* **Sửa thông tin khách hàng:**
    * Chọn một hàng dữ liệu của khách hàng trên bảng danh sách.
    * Thông tin của khách hàng sẽ tự động điền vào các trường nhập liệu.
    * Chỉnh sửa thông tin cần thiết.
    * Nhấn nút **"Cập nhật"**.
* **Xóa khách hàng:**
    * Chọn một hoặc nhiều hàng dữ liệu của khách hàng trên bảng.
    * Nhấn nút **"Xóa khách hàng"**. Sẽ có một hộp thoại xác nhận.
* **Tìm kiếm khách hàng:**
    * Nhập từ khóa (ví dụ: tên, email, số điện thoại) vào ô tìm kiếm.
    * Nhấn nút **"Tìm kiếm"** hoặc nhấn phím **Enter**. Danh sách khách hàng trên bảng sẽ được lọc theo kết quả tìm kiếm.
* **Tải lại:** Nhấn nút này để làm mới và hiển thị toàn bộ danh sách khách hàng.
* **Xuất Excel:** Nhấn nút này để xuất dữ liệu khách hàng hiện có trong bảng ra file Excel (`.xlsx`).
* **Thoát:** Nhấn nút này để quay lại màn hình chọn chức năng chính.

#### 4.2. Đánh giá Thị trường

* Màn hình này cho phép bạn xem các đánh giá về thị trường công nghệ.
* **Tải Dữ liệu Mẫu**: Nhấn nút này để hiển thị dữ liệu thị trường giả định cho mục đích thử nghiệm.
* **Tải Dữ liệu Thực (API)**: Nhấn nút này để thử gọi API và lấy dữ liệu thị trường thực tế (chức năng này cần được cấu hình API cụ thể trong mã nguồn). Quá trình tải dữ liệu sẽ chạy ngầm để tránh làm treo ứng dụng.
* **Biểu đồ**: Biểu đồ phân tích dữ liệu sẽ được hiển thị dựa trên dữ liệu đã tải.
* **Quay lại**: Nhấn nút này để trở về màn hình chọn chức năng.

#### 4.3. Báo cáo Cửa hàng

* Màn hình này hiển thị các số liệu thống kê tổng quan về khách hàng và doanh thu của cửa hàng.
* **Số liệu**: Bao gồm tổng số khách hàng, tổng doanh thu, khách hàng mới trong tháng, sản phẩm bán chạy nhất, v.v.
* **Biểu đồ**: Các biểu đồ (ví dụ: biểu đồ cột, biểu đồ tròn) có thể được hiển thị để trực quan hóa dữ liệu thống kê.
* **Báo cáo theo thời gian**: Tùy chọn để lọc báo cáo theo các khoảng thời gian cụ thể (ví dụ: theo tháng, quý, năm).
* **Quay lại**: Nhấn nút này để trở về màn hình chọn chức năng.

#### 4.4. Thống kê Sản phẩm Bán chạy

* Màn hình này hiển thị biểu đồ thống kê các sản phẩm được bán ra dựa trên dữ liệu khách hàng.
* **Tải dữ liệu**: Dữ liệu sẽ được tải từ file `customers.json` hoặc từ dữ liệu khách hàng đang có.
* **Loại biểu đồ**: Bạn có thể chọn loại biểu đồ để hiển thị (ví dụ: biểu đồ cột, biểu đồ tròn) để trực quan hóa doanh số sản phẩm.
* **Quay lại**: Nhấn nút này để trở về màn hình chọn chức năng.



