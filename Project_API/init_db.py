import sqlite3
import os

DB_PATH = 'game_store.db'

def create_database():
    print("Đang khởi tạo Database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Bảng Users (Người dùng)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user' -- 'user' hoặc 'admin'
        )
    ''')

    # 2. Bảng Categories (Thể loại game)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # 3. Bảng Games (Thông tin game)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT,
            FOREIGN KEY (category_id) REFERENCES Categories(id)
        )
    ''')

    # 4. Bảng Orders (Đơn hàng)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL,
            status TEXT DEFAULT 'Pending', -- Pending, Completed, Cancelled
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # 5. Bảng Order_Details (Chi tiết đơn hàng)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Order_Details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            game_id INTEGER,
            price REAL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (order_id) REFERENCES Orders(id),
            FOREIGN KEY (game_id) REFERENCES Games(id)
        )
    ''')

    # --- NẠP DỮ LIỆU MẪU (INSERT DATA) ---
    
    # Thêm Users (1 Admin, 1 Khách)
    cursor.execute("INSERT OR IGNORE INTO Users (id, username, password, email, role) VALUES (1, 'admin', '123', 'admin@gmail.com', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO Users (id, username, password, email, role) VALUES (2, 'minh', '123', 'minh@gmail.com', 'user')")

    # Thêm Categories
    cursor.execute("INSERT OR IGNORE INTO Categories (id, name) VALUES (1, 'Action')")
    cursor.execute("INSERT OR IGNORE INTO Categories (id, name) VALUES (2, 'RPG')")
    cursor.execute("INSERT OR IGNORE INTO Categories (id, name) VALUES (3, 'Strategy')")

    # Thêm Games (Giả lập vài tựa game hot)
    games_data = [
        ('Grand Theft Auto V', 1, 500000, 'Game thế giới mở đỉnh cao', 'https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png'),
        ('The Witcher 3: Wild Hunt', 2, 400000, 'Siêu phẩm nhập vai', 'https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg'),
        ('Age of Empires IV', 3, 800000, 'Game chiến thuật thời gian thực', 'https://upload.wikimedia.org/wikipedia/en/e/e2/Age_of_Empires_IV_cover_art.jpg'),
        ('Elden Ring', 2, 1200000, 'Game Souls-like đình đám', 'https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg')
    ]
    
    # Dùng INSERT OR IGNORE để tránh lỗi nếu chạy code nhiều lần
    for game in games_data:
        cursor.execute("INSERT INTO Games (title, category_id, price, description, image_url) VALUES (?, ?, ?, ?, ?)", game)

    conn.commit()
    conn.close()
    print("Tạo Database và nạp dữ liệu mẫu THÀNH CÔNG!")

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH) # Xóa DB cũ nếu muốn làm mới hoàn toàn
        print("Đã xóa Database cũ.")
    create_database()
