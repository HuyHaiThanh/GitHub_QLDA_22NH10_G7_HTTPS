# QLDA_22NH10_G7_HTTPS
Quản Lý Dự Án 22NH10 Nhóm G7

Thành Viên:
1. Nguyễn Văn Huy_102220108
2. Nguyễn Phan Thanh_102220126
3. Lễ Viết Vĩnh Phú_102220120
4. Lê Nguyễn Phúc Sinh_102220123

### Web_caro

Trò chơi caro trực tuyến

## Website

- Local development URL: http://caro.local:8000
- Production URL: [Coming soon]

## API Documentation

### Game APIs

1. **Get Game State**
   - URL: `/api/method/caro_game.game.api.get_game_state`
   - Method: GET
   - Parameters: `game_id`
   - Description: Lấy trạng thái hiện tại của trò chơi caro

2. **Make Move**
   - URL: `/api/method/caro_game.game.api.make_move`
   - Method: POST
   - Parameters: `game_id`, `row`, `col`
   - Description: Thực hiện nước đi trên bàn cờ

3. **Surrender Game**
   - URL: `/api/method/caro_game.game.api.surrender_game`
   - Method: POST
   - Parameters: `game_id`
   - Description: Đầu hàng trong trò chơi hiện tại

4. **Propose Draw**
   - URL: `/api/method/caro_game.game.api.propose_draw`
   - Method: POST
   - Parameters: `game_id`
   - Description: Đề xuất hòa trận với đối thủ

### Authentication APIs

1. **Login**
   - URL: `/api/method/caro_game.authentication.api.login`
   - Method: POST
   - Parameters: `usr`, `pwd`
   - Description: Đăng nhập vào hệ thống

2. **Register**
   - URL: `/api/method/caro_game.authentication.api.register`
   - Method: POST
   - Parameters: `username`, `email`, `password`
   - Description: Đăng ký tài khoản mới

### AI APIs

1. **Get AI Move**
   - URL: `/api/method/caro_game.ai.api.get_ai_move`
   - Method: POST
   - Parameters: `game_id`, `difficulty`
   - Description: Lấy nước đi tiếp theo từ AI dựa trên độ khó

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
