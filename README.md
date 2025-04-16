# QLDA_22NH10_G7_HTTPS
Quản Lý Dự Án 22NH10 Nhóm G7

Thành Viên:
1. Nguyễn Văn Huy_102220108
2. Nguyễn Phan Thanh_102220126
3. Lễ Viết Vĩnh Phú_102220120
4. Lê Nguyễn Phúc Sinh_102220123

### Web_caro

Trò chơi caro trực tuyến

### Hướng dẫn cài đặt

Bạn có thể cài đặt ứng dụng này bằng cách sử dụng [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch init_srv
bench install-app caro_game
```

### Đóng góp

Ứng dụng này sử dụng `pre-commit` để định dạng và kiểm tra mã nguồn. Vui lòng [cài đặt pre-commit](https://pre-commit.com/#installation) và kích hoạt nó cho repository này:

```bash
cd apps/caro_game
pre-commit install
```

Pre-commit được cấu hình để sử dụng các công cụ sau để kiểm tra và định dạng mã nguồn của bạn:

- ruff
- eslint
- prettier
- pyupgrade

### Giấy phép

agpl-3.0
