# Auto Add Friend Facebook

> Công cụ tự động gửi lời mời kết bạn từ danh sách **People You May Know** của Facebook, có giao diện đồ hoạ (Tkinter), tự động đăng nhập lại khi cookie hết hạn và hỗ trợ xác thực 2 yếu tố (TOTP).

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/python-3.8%2B-blue.svg">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
  <img alt="Status" src="https://img.shields.io/badge/status-active-success.svg">
</p>

---

## Mục lục

- [Tính năng](#tính-năng)
- [Ảnh chụp màn hình](#ảnh-chụp-màn-hình)
- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cách hoạt động](#cách-hoạt-động)
- [Cảnh báo & rủi ro](#cảnh-báo--rủi-ro)
- [FAQ](#faq)
- [Đóng góp](#đóng-góp)
- [Giấy phép](#giấy-phép)
- [Tác giả](#tác-giả)

---

## Tính năng

- ✅ **GUI Tkinter** — không cần thao tác trên terminal.
- ✅ **Tự động đăng nhập lại** khi cookie chết, dùng email/mật khẩu + 2FA key.
- ✅ **Xác thực 2 yếu tố (TOTP)** thông qua [`pyotp`](https://pypi.org/project/pyotp/).
- ✅ **Try/except toàn cục** cho mọi request → không crash khi mất mạng / Facebook trả lỗi.
- ✅ **Phát hiện auth-error** (mã `1357001`, `1357004`, …) và retry sau khi refresh phiên.
- ✅ **Log realtime** trong cửa sổ, có nút Start / Stop / Clear.
- ✅ **Sleep có thể ngắt** — bấm *Dừng* phản hồi tức thì.
- ✅ **Tuỳ chỉnh delay** giữa mỗi lượt gửi lời mời.


---

## Yêu cầu

- **Python** 3.8 trở lên
- Hệ điều hành: Windows / macOS / Linux (Tkinter mặc định kèm Python)
- Tài khoản Facebook hợp lệ (khuyến nghị tài khoản phụ để test)

### Thư viện Python

| Package | Mục đích |
| --- | --- |
| `requests` | Gửi HTTP request đến Facebook GraphQL & b-graph API |
| `pyotp` | Sinh mã 2FA TOTP |
| `attrs` | Sử dụng trong `formAll()` để tạo counter |

---

## Cài đặt

```bash
# 1. Clone repository
git clone https://github.com/<your-user>/addFriendAutomatic.git
cd addFriendAutomatic

# 2. (Khuyến nghị) tạo virtualenv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt
```

---

## Sử dụng

### Chạy GUI

```bash
python main.py
```

Trong cửa sổ:

1. **Cookie**: dán cookie Facebook (`c_user=...; xs=...; ...`).
2. **Email/SĐT/UID** + **Mật khẩu**: dùng để tự động đăng nhập lại khi cookie chết. Có thể bỏ trống nếu không cần.
3. **2FA Key**: secret TOTP (chuỗi base32 Facebook cấp khi bật xác thực 2 lớp). Bỏ trống nếu không bật 2FA.
4. **Delay (giây)**: thời gian chờ giữa mỗi lượt gửi lời mời (mặc định 5).
5. Bấm **Đăng nhập / Kiểm tra cookie** → khi thành công, nút **Bắt đầu add friend** sẽ kích hoạt.
6. Bấm **Dừng** bất kỳ lúc nào để tạm dừng tiến trình.

### Lấy cookie Facebook

1. Đăng nhập vào https://www.facebook.com trên trình duyệt.
2. Mở **DevTools** (`F12`) → tab **Application** → **Cookies** → `https://www.facebook.com`.
3. Copy toàn bộ cookie dưới dạng `name1=value1; name2=value2; ...`.

> 💡 Nên dùng các extension như **Cookie-Editor** để export nhanh hơn.

### Lấy 2FA key (nếu có)

Khi bật xác thực 2 yếu tố trên Facebook, chọn **Use authentication app** → Facebook hiển thị một chuỗi base32 (vd: `JBSWY3DPEHPK3PXP`). Copy chuỗi đó vào ô **2FA Key**.

---

## Cấu trúc dự án

```
addFriendAutomatic/
├── login.py        # Module đăng nhập Facebook qua b-graph API + 2FA
├── main.py         # Logic chính + GUI Tkinter
├── requirements.txt
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── .gitignore
└── screenshots/
```

---

## Cách hoạt động

```
┌──────────────┐    cookie     ┌──────────────────┐
│   GUI input  │ ───────────▶  │   dataGetHome()  │  ──► fb_dtsg, jazoest, FacebookID, ...
└──────┬───────┘                └────────┬─────────┘
       │ credentials                     │ cookie chết?
       ▼                                 ▼
┌──────────────┐  yes  ┌─────────────────────────┐
│ login.py     │ ◀─────│  refresh_session(...)   │
│ b-graph auth │       └────────────┬────────────┘
└──────┬───────┘                    │ cookie mới
       │                            ▼
       │                   ┌──────────────────┐
       └─────────────────▶ │ Loop add friend  │
                           │  - getSuggest    │
                           │  - sendAddFriend │
                           └──────────────────┘
```

- Mỗi request GraphQL được bọc qua `_post_graphql()` — phát hiện auth error sẽ tự gọi `refresh_session()` và retry **một lần**.
- `print()` ở scope module được redirect sang `queue.Queue` để hiển thị an toàn từ thread phụ.

---

## Cảnh báo & rủi ro

> ⚠️ **Đọc kỹ trước khi sử dụng.**

- Việc tự động hoá hành vi gửi lời mời kết bạn **vi phạm [Điều khoản dịch vụ của Facebook](https://www.facebook.com/legal/terms)**. Tài khoản của bạn có thể bị **tạm khoá / vô hiệu hoá vĩnh viễn**.
- Tool **chỉ phục vụ mục đích học tập, nghiên cứu reverse-engineering và tự động hoá cá nhân**. Tác giả **không chịu trách nhiệm** với bất kỳ hậu quả nào.
- **Không** dùng để spam, lừa đảo, thu thập dữ liệu trái phép, hoặc bất kỳ hành vi vi phạm pháp luật nào.
- **Không** chia sẻ cookie / mật khẩu / 2FA key của bạn với người khác.

---

## FAQ

**Q: Tool báo "Cookie không hợp lệ" liên tục.**
A: Cookie có thể đã hết hạn / bị logout từ thiết bị khác. Hãy lấy cookie mới hoặc nhập email + mật khẩu để auto re-login.

**Q: Có hỗ trợ proxy không?**
A: Hiện tại chưa, nhưng dễ mở rộng — bạn có thể thêm `proxies={"http": ..., "https": ...}` vào `mainRequests()` và `login.py`.

**Q: Vì sao phải có 2FA key thay vì OTP?**
A: OTP đổi 30s/lần → không thể nhập tay khi auto re-login. 2FA key (TOTP secret) cho phép `pyotp` sinh OTP đúng thời điểm.

**Q: Tool chạy headless / CLI được không?**
A: Phiên bản hiện tại chỉ có GUI. Bạn có thể tự gọi `getSuggestFriends()` / `sendAddFriend()` từ script riêng nếu muốn CLI.

---

## Đóng góp

Pull Request được hoan nghênh! Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) trước khi submit.

---

## Giấy phép

Dự án phát hành theo giấy phép [MIT](LICENSE).

---

## Tác giả

**Nguyễn Minh Huy (RainTee)**
- GitHub: [@MinhHuyDev](https://github.com/MinhHuyDev)
- Module `login.py` — Facebook Login V2 ([fbchat-v2](https://github.com/MinhHuyDev/fbchat-v2)) (28/12/2022, last update 15/4/2026)

---

<p align="center"><i>If you find this project useful, give it a ⭐ on GitHub!</i></p>
