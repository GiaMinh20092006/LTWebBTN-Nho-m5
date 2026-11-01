"""Khởi tạo Database cho Vapor Game Store API.

Tạo toàn bảng (Users, Categories, Games, Orders, Order_Details, Reviews,
WalletTransactions) rồi nạp dữ liệu mẫu: 120 game (games_seed.py),
người dùng dùng thử, đánh giá và hóa đơn demo.

Chạy:  python init_db.py   (XÓA database cũ nếu có!)
"""

import os
import random
import sqlite3
import sys
from datetime import datetime, timedelta

# Windows console mặc định dùng cp1252 — ép Python in tiếng Việt UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from werkzeug.security import generate_password_hash

# Scrypt (mặc định của werkzeug) mất ~10s/một lần verify trên Windows + Python 3.14,
# vượt timeout của client — dùng pbkdf2 cho demo nhanh.
PASSWORD_METHOD = "pbkdf2:sha256:100000"

from games_seed import GAMES

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_store.db")

CATEGORIES = [
    (1, "Action", "action", "⚔"),
    (2, "RPG", "rpg", "✦"),
    (3, "Strategy", "strategy", "♜"),
    (4, "Shooter", "shooter", "◎"),
    (5, "Horror", "horror", "☠"),
    (6, "Adventure", "adventure", "➤"),
    (7, "Racing", "racing", "≫"),
    (8, "Sports", "sports", "◆"),
    (9, "Puzzle", "puzzle", "✿"),
    (10, "Simulation", "simulation", "⚙"),
    (11, "Indie", "indie", "❋"),
    (12, "MMO", "mmo", "∞"),
]

CATEGORY_SLUG_TO_ID = {slug: cid for cid, _name, slug, _icon in CATEGORIES}

# Mật khẩu demo (sẽ được BẰNG HASH trước khi lưu vào DB):
#   admin / admin123  (role=admin)
#   minh  / minh1234  (role=user)
#   lanaplayer / vapor123 (role=user)
USERS = [
    ("admin", "admin123", "admin@vaporwave.vn", "admin", 9999999),
    ("minh", "minh1234", "minh@vaporwave.vn", "user", 1200000),
    ("lanaplayer", "vapor123", "lana@vaporwave.vn", "user", 650000),
]


def create_schema(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'user',
            balance REAL NOT NULL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE,
            icon TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL DEFAULT 0,
            description TEXT,
            image_url TEXT,
            developer TEXT,
            release_date DATE,
            rating REAL DEFAULT 0.0,
            platforms TEXT,
            tags TEXT,
            sales INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES Categories(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total_amount REAL,
            status TEXT DEFAULT 'Success',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Order_Details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            game_id INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES Orders(id),
            FOREIGN KEY (game_id) REFERENCES Games(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            user_id INTEGER,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES Games(id),
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS WalletTransactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            kind TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)


def seed_data(conn, cursor):
    # --- Users (mật khẩu được hash, KHÔNG lưu plain text) ---
    for username, password, email, role, balance in USERS:
        cursor.execute(
            "INSERT INTO Users (username, password, email, role, balance) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, generate_password_hash(password, method=PASSWORD_METHOD), email, role, balance),
        )

    cursor.executemany(
        "INSERT INTO Categories (id, name, slug, icon) VALUES (?, ?, ?, ?)",
        CATEGORIES,
    )

    # --- Games: 120 tựa game từ games_seed.py ---
    random.seed(42)
    for (
        title, slug, price, description, developer,
        release_date, rating, platforms, tags,
    ) in GAMES:
        cursor.execute(
            "INSERT INTO Games (title, category_id, price, description, image_url, "
            "developer, release_date, rating, platforms, tags, sales) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                title,
                CATEGORY_SLUG_TO_ID[slug],
                price,
                description,
                None,  # image_url để trống -> Client tự vẽ cover SVG neon
                developer,
                release_date,
                rating,
                platforms,
                tags,
                random.randint(50, 4800),
            ),
        )

    conn.commit()


def seed_reviews_and_orders(conn, cursor):
    review_comments = [
        "Siêu phẩm, đồ họa neon đẹp mê hồn, chơi không muốn đứng lên.",
        "Gameplay mượt, nhạc synthwave cực cuốn, đáng từng đồng.",
        "Hay nhưng hơi ngắn, mong phần tiếp theo sớm.",
        "Bug hiếm, tối ưu tốt trên PC, 10/10 sẽ mua lại.",
        "Cốt truyện hấp dẫn, nhân vật xây dựng rất có chiều sâu.",
        "Điều khiển hơi khó quen lúc đầu nhưng về sau rất phê.",
        "Giá rẻ mà chất lượng AAA, Vapor deal hời quá!",
        "Đồ họa retro pixel đẹp, phong cách Vaporwave đúng gu.",
    ]

    games = cursor.execute("SELECT id FROM Games ORDER BY id").fetchall()
    users = cursor.execute("SELECT id FROM Users WHERE role = 'user'").fetchall()

    # Mỗi game nhận 0-3 đánh giá từ người dùng demo
    for game in games:
        for user in users:
            if random.random() < 0.28:
                cursor.execute(
                    "INSERT INTO Reviews (game_id, user_id, rating, comment, created_at) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (
                        game[0],
                        user[0],
                        random.randint(3, 5),
                        random.choice(review_comments),
                        (datetime.now() - timedelta(days=random.randint(1, 120)))
                        .strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )

    # 25 hóa đơn demo rải trong 6 tháng gần nhất (cho biểu đồ doanh thu admin)
    all_games = cursor.execute(
        "SELECT id, price FROM Games ORDER BY id"
    ).fetchall()

    for _ in range(25):
        user = random.choice(users + [(1,)])
        order_date = datetime.now() - timedelta(
            days=random.randint(1, 180), hours=random.randint(0, 23)
        )
        chosen = random.sample(all_games, k=random.randint(1, 4))
        total = sum(g[1] for g in chosen)

        cursor.execute(
            "INSERT INTO Orders (user_id, total_amount, status, order_date) "
            "VALUES (?, ?, 'Success', ?)",
            (user[0], total, order_date.strftime("%Y-%m-%d %H:%M:%S")),
        )
        order_id = cursor.lastrowid

        for game_id, price in chosen:
            cursor.execute(
                "INSERT INTO Order_Details (order_id, game_id, price) VALUES (?, ?, ?)",
                (order_id, game_id, price),
            )
        cursor.execute(
            "INSERT INTO WalletTransactions (user_id, amount, kind, note, created_at) "
            "VALUES (?, ?, 'purchase', ?, ?)",
            (user[0], -total, f"Order #{order_id}",
             order_date.strftime("%Y-%m-%d %H:%M:%S")),
        )

    conn.commit()


def recreate_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Đã xóa database cũ: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Đang tạo schema (7 bảng)...")
    create_schema(cursor)

    print("Đang nạp người dùng, thể loại và 120 game mẫu...")
    seed_data(conn, cursor)

    print("Đang nạp đánh giá và hóa đơn demo...")
    seed_reviews_and_orders(conn, cursor)

    total_games = cursor.execute("SELECT COUNT(*) FROM Games").fetchone()[0]
    total_users = cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0]
    total_reviews = cursor.execute("SELECT COUNT(*) FROM Reviews").fetchone()[0]
    total_orders = cursor.execute("SELECT COUNT(*) FROM Orders").fetchone()[0]

    conn.close()

    print("=" * 52)
    print("TẠO DATABASE THÀNH CÔNG!")
    print(f"  Game      : {total_games}")
    print(f"  Người dùng: {total_users}  (admin/admin123, minh/minh1234, lanaplayer/vapor123)")
    print(f"  Đánh giá  : {total_reviews}")
    print(f"  Hóa đơn   : {total_orders}")
    print(f"  File DB   : {DB_PATH}")
    print("=" * 52)


if __name__ == "__main__":
    recreate_database()
