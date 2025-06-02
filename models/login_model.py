import json
import os

class LoginModel:
    def __init__(self):
        self.data_file = "data/taikhoan.json"  # Đường dẫn đến file dữ liệu người dùng
        self.ensure_data_file_exists() # Đảm bảo file tồn tại khi khởi tạo

    def ensure_data_file_exists(self):
        """Đảm bảo thư mục 'data' và file 'taikhoan.json' tồn tại.
        Nếu file không tồn tại, tạo nó với dữ liệu admin và user mặc định."""
        data_dir = os.path.dirname(self.data_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Đã tạo thư mục: {data_dir}")

        if not os.path.exists(self.data_file) or os.path.getsize(self.data_file) == 0:
            initial_users = [
                {"username": "admin", "password": "123", "role": "admin"},
                {"username": "user", "password": "123", "role": "user"}
            ]
            try:
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump(initial_users, file, ensure_ascii=False, indent=2)
                print(f"Đã tạo file '{self.data_file}' với dữ liệu mặc định.")
            except Exception as e:
                print(f"Lỗi khi tạo file dữ liệu mặc định: {e}")

    def authenticate(self, username, password):
        """Xác thực thông tin đăng nhập"""
        try:
            if not os.path.exists(self.data_file):
                print(f"File {self.data_file} không tồn tại sau khi khởi tạo!")
                return False

            with open(self.data_file, 'r', encoding='utf-8') as file:
                users = json.load(file)

            for user in users:
                if user['username'] == username and user['password'] == password:
                    return True  # Đăng nhập thành công
            
            return False  # Đăng nhập thất bại
            
        except json.JSONDecodeError:
            print("Lỗi: File JSON không hợp lệ hoặc trống!")
            self.ensure_data_file_exists() # Thử tạo lại file mặc định nếu lỗi
            return False
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
            return False

    def get_user_role(self, username):
        """Lấy vai trò của người dùng"""
        try:
            if not os.path.exists(self.data_file):
                return None
            with open(self.data_file, 'r', encoding='utf-8') as file:
                users = json.load(file)
            for user in users:
                if user['username'] == username:
                    return user.get('role', 'user') # Mặc định là 'user' nếu không có vai trò
            return None
        except Exception as e:
            print(f"Lỗi khi lấy vai trò người dùng: {e}")
            return None

    def add_user(self, username, password, role="user"):
        """Thêm người dùng mới vào file JSON"""
        try:
            # Đảm bảo file tồn tại và không trống
            self.ensure_data_file_exists()

            with open(self.data_file, 'r', encoding='utf-8') as file:
                users = json.load(file)
            
            # Kiểm tra trùng tên đăng nhập
            if any(user['username'] == username for user in users):
                print(f"Tên đăng nhập '{username}' đã tồn tại.")
                return False

            new_user = {"username": username, "password": password, "role": role}
            users.append(new_user)

            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(users, file, ensure_ascii=False, indent=2)
            print(f"Đã thêm người dùng '{username}' với vai trò '{role}'.")
            return True
        except Exception as e:
            print(f"Lỗi khi thêm người dùng: {e}")
            return False