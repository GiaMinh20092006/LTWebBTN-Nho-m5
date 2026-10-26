# LTWebBTN-Nho-m5

Never gonna give you up, never gonna let you down

## 📁 Cấu trúc thư mục dự án

```text
LTWebBTN-Nho-m5/
│
├── Project_API/                  # Chứa Backend & Database
│   ├── app.py                    # Code chạy API (Cổng 5000)
│   ├── init_db.py                # Script tạo Database và nạp data mẫu
│   └── game_store.db             # File Database (sẽ tự sinh ra khi chạy init_db.py)
│
├── Project_Client/               # Chứa Frontend & Web Client
│   ├── app.py                    # Code chạy Web gọi API (Cổng 5001)
│   ├── static/                   # Chứa file CSS, JS, Images
│   │   └── css/
│   │       └── style.css
│   └── templates/                # Chứa các file HTML
│       ├── base.html             # Layout chung (Header, Footer)
│       ├── index.html            # Trang chủ (hiển thị danh sách game)
│       ├── cart.html             # Trang giỏ hàng
│       ├── login.html            # Trang đăng nhập
│       └── admin.html            # Trang quản trị
│
└── README.md
