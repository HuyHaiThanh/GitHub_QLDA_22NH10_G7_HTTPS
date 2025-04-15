# QLDA_22NH10_G7_HTTPS
Quản Lý Dự Án 22NH10 Nhóm G7

Thành Viên:
1. Nguyễn Văn Huy_102220108
2. Nguyễn Phan Thanh_102220126
3. Lễ Viết Vĩnh Phú_102220120
4. Lê Nguyễn Phúc Sinh_102220123

## Ứng dụng Caro Online với Frappe Framework

### Thông tin đăng nhập
- **Username**: Administrator
- **Password**: 12345

### Các bước cài đặt

1. **Cài đặt các gói phụ thuộc**
   ```bash
   sudo apt-get update
   sudo apt-get install -y git python3-dev python3-pip python3-setuptools python3-venv redis-server
   sudo apt-get install -y nodejs npm
   sudo apt-get install -y pkg-config libmysqlclient-dev libssl-dev libzstd-dev
   ```

2. **Cài đặt MariaDB**
   ```bash
   sudo apt-get install -y mariadb-server mariadb-client
   sudo mysql_secure_installation
   # Thiết lập mật khẩu root MariaDB: 12345
   ```

3. **Cài đặt bench**
   ```bash
   sudo apt-get install -y curl
   sudo pip3 install frappe-bench
   ```

4. **Tạo bench mới**
   ```bash
   bench init caro-bench
   cd caro-bench
   ```

5. **Tạo site mới**
   ```bash
   bench new-site caro.local --mariadb-root-username root --mariadb-root-password 12345 --admin-password 12345
   ```

6. **Tạo ứng dụng Caro mới**
   ```bash
   bench new-app caro_game
   bench --site caro.local install-app caro_game
   ```

7. **Cấu hình local DNS**
   - Thêm dòng sau vào file `/etc/hosts` hoặc `C:\Windows\System32\drivers\etc\hosts`:
   ```
   127.0.0.1 caro.local
   ```

8. **Chạy ứng dụng**
   ```bash
   bench start
   ```

### Sử dụng ứng dụng

1. **Truy cập ứng dụng**
   - Mở trình duyệt và truy cập: http://caro.local:8001
   - Đăng nhập với tài khoản Administrator và mật khẩu 12345

2. **Tạo DocType cho ứng dụng Caro**
   - Trên giao diện Frappe Desk, tìm "DocType" và tạo các loại dữ liệu:
     - Caro Game Board
     - Caro Game Session
     - Caro Game Move
     - ...

3. **Phát triển giao diện trò chơi**
   - Tạo trang web và giao diện người dùng
   - Tạo API cho logic trò chơi

### Kết nối và đóng góp
- GitHub: [https://github.com/your-username/caro-game](https://github.com/your-username/caro-game)
