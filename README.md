# QLDA_22NH10_G7_HTTPS
Quản Lý Dự Án 22NH10 Nhóm G7

Thành Viên:
1. Nguyễn Văn Huy_102220108
2. Nguyễn Phan Thanh_102220126
3. Lễ Viết Vĩnh Phú_102220120
4. Lê Nguyễn Phúc Sinh_102220123

### Web_caro

Trò chơi caro trực tuyến

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch init_srv
bench install-app caro_game
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/caro_game
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

agpl-3.0
