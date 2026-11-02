# ◢ VAPOR GAME STORE — LTWebBTN-Nho-m5

Dự án Web Lập trình (Group Project) — **Game Store phong cách Vaporwave / Synthwave / Cyberpunk**
kiến trúc **2 ứng dụng Flask tách biệt**: `Project_API` (Backend REST + SQLite) và
`Project_Client` (Frontend Web gọi API qua HTTP).

- **API (cổng 5000)**: xác thực, CRUD game/thể loại, tìm kiếm – lọc – sắp xếp – phân trang,
  đánh giá (reviews), ví điện tử (wallet + lịch sử giao dịch), đơn hàng, thư viện game, thống kê admin.
- **Client (cổng 5001)**: toàn bộ UI Vaporwave — nền **3D Perspective Grid** chạy vô tận,
  hiệu ứng **Polychromatic Blur** (tách kênh RGB + blur nhiều lớp), nút **GLITCH/NEON MODE
  Toggle**, tiêu đề kiểu **glitch text** restructuring, kho 120+ game với **poster SVG neon
  tự vẽ**, và **Vapor-Radio** — music player góc màn hình tự tổng hợp âm thanh bằng WebAudio
  (4 đài synthwave, không cần file nhạc, hoạt động offline).

---

## 📁 Cấu trúc thư mục dự án

```text
LTWebBTN-Nho-m5/
│
├── Project_API/                  # Backend REST API + Database (cổng 5000)
│   ├── app.py                    # Flask API: users, games, categories, reviews,
│   │                             # wallet, orders, library, admin stats
│   ├── init_db.py                # Tạo schema 7 bảng + nạp dữ liệu mẫu
│   ├── games_seed.py             # Danh sách 120 game thật (title/price/desc/dev/rating...)
│   ├── requirements.txt          # flask
│   └── game_store.db             # SQLite (tự sinh khi chạy init_db.py — đã gitignore)
│
├── Project_Client/               # Frontend Web Client (cổng 5001)
│   ├── app.py                    # Flask client — gọi API qua HTTP (requests),
│   │                             # session đăng nhập/giỏ hàng, vẽ cover SVG neon
│   ├── requirements.txt          # flask + requests
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css         # Theme Vaporwave + layout toàn site
│   │   │   └── vapor-fx.css      # 3D grid, glitch text, polychromatic blur,
│   │   │                         # neon mode toggle, Vapor-Radio
│   │   └── js/
│   │       ├── vapor.js          # Toggle Glitch/Neon (localStorage), alerts, wallet chips
│   │       └── radio.js          # Vapor-Radio: synth 4 đài bằng WebAudio API
│   └── templates/
│       ├── base.html             # Layout chung: header, nền grid, footer, radio player
│       ├── index.html            # Trang chủ: hero glitch, thể loại, search/sort/filter/paging
│       ├── game_detail.html      # Chi tiết game + đánh giá + game liên quan
│       ├── cart.html             # Giỏ hàng + thanh toán bằng ví Vapor
│       ├── orders.html           # Lịch sử đơn hàng
│       ├── library.html          # Thư viện game đã sở hữu
│       ├── wallet.html           # Ví: số dư, nạp tiền, lịch sử giao dịch
│       ├── login.html            # Đăng nhập
│       ├── register.html         # Đăng ký
│       ├── admin.html            # Dashboard: thống kê, biểu đồ doanh thu, CRUD game/thể loại
│       ├── 404.html              # Trang lỗi 404 neon
│       └── 503.html              # Trang báo API chưa chạy
│
└── README.md                     # File bạn đang đọc
```

## 🔑 Tài khoản demo

| Tài khoản  | Mật khẩu   | Quyền  | Ghi chú               |
|------------|-----------|--------|-----------------------|
| `admin`    | `admin123`   | Admin  | Mở mục ⚡ Admin trên menu |
| `minh`     | `minh1234`   | User   | Có sẵn 1.200.000đ trong ví |
| `lanaplayer` | `vapor123` | User   | Có sẵn 650.000đ trong ví   |

Mật khẩu trong DB được **hash** bằng `werkzeug.generate_password_hash` — không lưu plain text.

## 🗄️ Database (7 bảng)

`Users` (kèm `role`, `balance`) · `Categories` (12 thể loại, kèm `icon`) ·
`Games` (120+ game: giá VND, developer, phát hành, rating, platforms, tags, sales) ·
`Orders` · `Order_Details` · `Reviews` · `WalletTransactions`

Dữ liệu mẫu gồm 3 user, 120 game, hàng chục đánh giá và 25 hóa đơn rải trong 6 tháng
(phục vụ biểu đồ doanh thu admin).

---

# 🚀 Chạy project bằng GitHub Codespaces (khuyến nghị)

> Codespaces = máy ảo Linux chạy ngay trong trình duyệt, có sẵn Python —
> không cần cài gì trên máy cá nhân.

### Bước 0 — Đưa repo lên GitHub (làm 1 lần)

```bash
# Chạy tại máy của bạn (Git Bash / Terminal), cd vào thư mục dự án:
cd LTWebBTN-Nho-m5
git init
git add .
git commit -m "Vapor Game Store: API + Client + 120 games"
# Tạo repo trống trên github.com (VD: LTWebBTN-Nho-m5), rồi:
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```

(`*.db` đã nằm trong `.gitignore` — database sẽ được tạo mới trong Codespaces.)

### Bước 1 — Khởi tạo Codespace

1. Mở repo trên GitHub → nút xanh **`<> Code`** → tab **Codespaces** → **Create codespace on main**.
2. Chờ ~1 phút để máy ảo Ubuntu khởi động, VS Code trên browser sẽ mở ra.
3. Mở terminal trong Codespaces ( `` Ctrl + ` `` ).

### Bước 2 — Cài Python & dependencies

Codespaces mặc định đã có Python 3; chỉ cần tạo venv và cài gói:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r Project_API/requirements.txt
```

`requests` đã có trong cùng requirements — client dùng chung venv này.

### Bước 3 — Tạo database (chỉ lần đầu, hoặc khi đổi seed)

```bash
cd Project_API
python init_db.py        # tự xóa DB cũ → tạo 7 bảng → nạp 120 game + user/reviews/orders
```

Bạn sẽ thấy: `TẠO DATABASE THÀNH CÔNG! Game: 120 ...`

### Bước 4 — Chạy API (terminal 1, cổng 5000)

```bash
# vẫn trong Project_API/
python app.py
```

Flask báo `Running on http://0.0.0.0:5000`.

> ⚠️ Codespaces đôi khi báo port 5000 đang bị dùng. Nếu vậy:
> `API_PORT=5100 python app.py` và khi chạy client đặt
> `API_BASE_URL=http://127.0.0.1:5100`.

### Bước 5 — Chạy Client (terminal 2, cổng 5001)

Bấm **`+`** trong panel terminal để mở terminal THỨ HAI (gitignore dùng lại venv):

```bash
source .venv/bin/activate
cd Project_Client
python app.py
```

### Bước 6 — Mở web bằng PORT FORWARDING của Codespaces

1. Codespaces tự phát hiện cổng → bảng **`Your application running on port 5001 is available`**
   bấm **Open in browser**. (Hoặc tab **Ports** → click vào URL của port `5001`.)
2. Web Vapor mở ra. API (port 5000) cũng forward được để test trực tiếp:
   tab **Ports** → port 5000 → mở `https://xxxx-5000.githubpreview.dev/api/health`
   phải thấy `{"status": "ok", ...}`.
3. Test nhanh: đăng nhập `minh / minh1234` → thêm game vào giỏ → thanh toán bằng ví →
   xem Thư viện/Đơn hàng. Đăng nhập `admin / admin123` → menu **⚡ Admin** để CRUD game,
   xem thống kê. Bật **GLITCH** toggle và bấm **▶** trên **Vapor-Radio** góc phải màn hình.

### (Tùy chọn) Gộp lệnh vào 1 lần chạy với `devcontainer`/tasks

`.vscode/tasks.json` mẫu (tạo 2 task Run API + Run Client):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run API (5000)",
      "type": "shell",
      "command": "cd ${workspaceFolder}/Project_API && ../.venv/bin/python app.py"
    },
    {
      "label": "Run Client (5001)",
      "type": "shell",
      "command": "cd ${workspaceFolder}/Project_Client && ../.venv/bin/python app.py",
      "dependsOn": []
    }
  ]
}
```

---

# 💻 Chạy local trên Windows (không cần Codespaces)

```powershell
# Yêu cầu: Python 3.10+ (bỏ chọn "Add python.exe to PATH" nếu bị xung đột Windows Store alias)
cd Project_API
pip install -r requirements.txt
python init_db.py
python app.py                 # Terminal 1 — API cổng 5000

cd Project_Client
pip install -r requirements.txt
python app.py                 # Terminal 2 — Client http://127.0.0.1:5001
```

Mở trình duyệt: **http://127.0.0.1:5001**

## ❓ Xử lý lỗi thường gặp

| Lỗi / hiện tượng | Nguyên nhân | Cách sửa |
|---|---|---|
| Trang web hiện **503 — API OFFLINE** | Chưa chạy `Project_API/app.py` | Chạy terminal 1 trước, đúng cổng |
| `Chưa có file Database. Hãy chạy init_db.py trước!` | DB chưa được tạo | `cd Project_API && python init_db.py` |
| `python` trên Windows mở Microsoft Store | Windows App Execution Alias | Dùng `py app.py` hoặc tắt alias trong Settings |
| Codespaces báo port 5000 busy | Service demo chiếm cổng | `API_PORT=5100 python app.py` + `API_BASE_URL=http://127.0.0.1:5100 python app.py` (client) |
| Không nghe thấy nhạc radio | Trình duyệt chặn autoplay | Bấm nút **▶** trên Vapor-Radio (góc phải dưới) |
| Đăng nhập demo fail sau khi chỉnh seed | DB cũ đã reset | Chạy lại `init_db.py` rồi đăng nhập `minh / minh1234` |

## ✨ Checklist tính năng

**Client UI:** 3D Perspective Grid nền · Polychromatic Blur (card/ảnh) · Glitch/Neon Mode
toggle (nhớ trạng thái) · Title restructuring (glitch text 2 lớp RGB) · Vapor-Radio 4 đài
WebAudio + volume + minimize + visualizer · trang chủ search/filter/sort/paging · chi tiết
game + chấm sao đánh giá · giỏ hàng + ví điện tử · thư viện/đơn hàng · dashboard admin ·
responsive + tôn trọng `prefers-reduced-motion`.

**API:** 25+ endpoint REST · mật khẩu hash · phân quyền admin (`require_admin`) · kiểm tra số dư ví
khi checkout, chống mua trùng game, cập nhật `sales` + average rating · xóa game kèm dọn
reviews/order details · error handler JSON · health check.

---

© 2026 VAPOR GAME STORE — PLAY BEYOND REALITY ◈
