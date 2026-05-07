# Contributing

Cảm ơn bạn đã quan tâm đến dự án! Mọi đóng góp đều được chào đón — từ báo lỗi, đề xuất tính năng đến gửi Pull Request.

## Quy trình đóng góp

1. **Fork** repository này.
2. **Clone** fork về máy:
   ```bash
   git clone https://github.com/<your-user>/addFriendAutomatic.git
   cd addFriendAutomatic
   ```
3. Tạo branch mới cho thay đổi của bạn:
   ```bash
   git checkout -b feat/ten-tinh-nang
   ```
4. Cài môi trường:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   source .venv/bin/activate       # macOS/Linux
   pip install -r requirements.txt
   ```
5. Thực hiện thay đổi và **test cẩn thận** với tài khoản phụ.
6. Commit theo format [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: thêm hỗ trợ proxy
   fix: xử lý KeyError khi social_context null
   docs: cập nhật README
   ```
7. Push và mở **Pull Request** đến nhánh `main`.

## Coding style

- Tuân thủ **PEP 8** ở mức hợp lý.
- Indent **5 spaces** nếu sửa file `main.py` / `login.py` để đồng bộ với code hiện tại.
- Không thêm dependency nặng nếu không thực sự cần.
- Mọi request mạng phải có `try/except` và timeout hợp lý.
- Không log/print credentials, cookie, mật khẩu.

## Báo lỗi (Bug Report)

Khi mở issue, vui lòng cung cấp:
- Phiên bản Python (`python --version`)
- Hệ điều hành
- Các bước tái hiện lỗi
- Log lỗi (đã ẩn cookie/mật khẩu)
- Behavior mong đợi vs. behavior thực tế

## Đề xuất tính năng

Mở issue với prefix `[Feature Request]` và mô tả:
- Vấn đề bạn đang gặp
- Giải pháp đề xuất
- Lựa chọn thay thế đã cân nhắc

## Quy tắc ứng xử

Tham khảo [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
