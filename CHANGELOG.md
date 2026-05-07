# Changelog

Tất cả các thay đổi đáng chú ý của dự án sẽ được ghi lại trong file này.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
và dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]

### Added
- Hỗ trợ proxy (dự kiến)
- Chế độ CLI tuỳ chọn (dự kiến)

## [1.0.0] - 2026-05-08

### Added
- 🎉 Phát hành lần đầu.
- Giao diện đồ hoạ Tkinter với các nút Start / Stop / Clear log.
- Module `login.py` đăng nhập Facebook qua `b-graph.facebook.com/auth/login`.
- Hỗ trợ xác thực 2 yếu tố (TOTP) qua `pyotp`.
- Tự động phát hiện cookie chết và đăng nhập lại bằng credentials đã lưu.
- Wrapper `_post_graphql()` với try/except, retry 1 lần khi gặp auth error.
- Sleep có thể ngắt — phản hồi nút Dừng tức thì.
- Log realtime trong cửa sổ qua `queue.Queue`.

### Security
- Không lưu credentials xuống đĩa; chỉ giữ trong RAM khi chạy.

[Unreleased]: https://github.com/<your-user>/addFriendAutomatic/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/<your-user>/addFriendAutomatic/releases/tag/v1.0.0
