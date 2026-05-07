# Security Policy

## Phiên bản được hỗ trợ

| Phiên bản | Hỗ trợ            |
| --------- | ----------------- |
| `main`    | :white_check_mark: |
| < 1.0     | :x:                |

## Báo cáo lỗ hổng bảo mật

Nếu bạn phát hiện lỗ hổng bảo mật trong dự án, **vui lòng KHÔNG mở issue công khai**.

Thay vào đó, hãy liên hệ riêng qua một trong các cách sau:

- 📧 Email: `security@example.com` *(cập nhật email thật của bạn)*
- 🔒 GitHub Security Advisories: [Report a vulnerability](https://github.com/<your-user>/addFriendAutomatic/security/advisories/new)

Bao gồm trong báo cáo:
- Mô tả chi tiết lỗ hổng
- Các bước tái hiện
- Tác động tiềm tàng
- Phiên bản bị ảnh hưởng
- (Tuỳ chọn) Đề xuất khắc phục

## Cam kết phản hồi

- Chúng tôi sẽ phản hồi trong vòng **72 giờ**.
- Đánh giá và cập nhật tiến độ sửa lỗi trong vòng **7 ngày**.
- Công bố advisory công khai sau khi đã có bản vá.

## Khuyến nghị bảo mật khi sử dụng

- ❌ **Không** commit cookie, mật khẩu, 2FA key vào source control.
- ❌ **Không** chia sẻ file `.env` hoặc cấu hình cá nhân.
- ✅ Sử dụng tài khoản **phụ** để test, tránh gây thiệt hại tài khoản chính.
- ✅ Đọc kỹ code trước khi chạy — đây là tool tương tác trực tiếp với tài khoản Facebook.
- ✅ Cập nhật `requests`, `pyotp`, `attrs` lên phiên bản mới nhất để vá lỗi bảo mật upstream.

## Phạm vi

Dự án này **không phải** sản phẩm chính thức của Meta/Facebook. Mọi rủi ro về tài khoản, dữ liệu khi sử dụng tool đều thuộc trách nhiệm của người dùng.
