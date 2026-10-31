import sqlite3
import os

DB_PATH = 'game_store.db'

def create_database():
    print("Đang khởi tạo Database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Bảng Users (Có thêm số dư ví, ngày tạo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT DEFAULT 'user',
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Bảng Categories (Thể loại)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE
        )
    ''')

    # 3. Bảng Games (Thông tin game siêu chi tiết)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT,
            developer TEXT,
            release_date DATE,
            rating REAL DEFAULT 0.0,
            FOREIGN KEY (category_id) REFERENCES Categories(id)
        )
    ''')

    # 4. Bảng Orders (Hóa đơn mua hàng)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total_amount REAL,
            status TEXT DEFAULT 'Success',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # 5. Bảng Order_Details (Chi tiết hóa đơn)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Order_Details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            game_id INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES Orders(id),
            FOREIGN KEY (game_id) REFERENCES Games(id)
        )
    ''')

    # 6. Bảng Reviews (Đánh giá game)
    cursor.execute('''
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
    ''')

    # --- NẠP DỮ LIỆU MẪU (INSERT DATA) ---
    
    # Passwords thực tế nên được hash, nhưng để đơn giản test API thì để plain text
    cursor.execute("INSERT OR IGNORE INTO Users (id, username, password, email, role) VALUES (1, 'admin', '123', 'admin@vapor.com', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO Users (id, username, password, email, role) VALUES (2, 'minh', '123', 'minh@vapor.com', 'user')")

    categories = [(1, 'Action', 'action'), (2, 'RPG', 'rpg'), (3, 'Strategy', 'strategy'), (4, 'Cyberpunk', 'cyberpunk'), (5, 'Synthwave', 'synthwave')]
    cursor.executemany("INSERT OR IGNORE INTO Categories (id, name, slug) VALUES (?, ?, ?)", categories)

    games_data = [
        ('Cyberpunk 2077', 4, 1200000, 'Open world action RPG.', 'https://image.api.playstation.com/vulcan/ap/rnd/202111/3013/cKjH4eX8i3P4a2r1z6G7rF8k7F9.jpg', 'CD Projekt', '2020-12-10', 4.5),
        ('Hotline Miami', 1, 150000, 'Top-down shooter with neon vibes.', 'https://upload.wikimedia.org/wikipedia/en/6/66/Hotline_Miami_cover.png', 'Dennaton Games', '2012-10-23', 4.8),
        ('Neon Drive', 5, 90000, 'Rhythm racing game.', 'https://cdn.cloudflare.steamstatic.com/steam/apps/433100/header.jpg', 'Fraoula', '2016-07-15', 4.2),
        ('Ghostrunner', 4, 500000, 'Cyberpunk parkour action.', 'https://cdn.cloudflare.steamstatic.com/steam/apps/1139900/header.jpg', 'One More Level', '2020-10-27', 4.4),
        ('Grand Theft Auto V', 1, 500000, 'Game thế giới mở đỉnh cao.', 'https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png', 'Rockstar North', '2013-09-17', 4.9),
        ('The Witcher 3: Wild Hunt', 2, 400000, 'Siêu phẩm nhập vai.', 'https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg', 'CD Projekt Red', '2015-05-19', 5.0),
        ('Age of Empires IV', 3, 800000, 'Game chiến thuật thời gian thực.', 'https://upload.wikimedia.org/wikipedia/en/e/e2/Age_of_Empires_IV_cover_art.jpg', 'Relic Ent.', '2021-10-28', 4.1),
        ('Elden Ring', 2, 1200000, 'Game Souls-like đình đám.', 'https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg', 'FromSoftware', '2022-02-25', 4.9),
        ('Vaporwave Simulator', 5, 50000, 'Aesthetic experience.', 'https://img.itch.zone/aW1nLzE5MjU5NjcucG5n/original/%2FhXz4h.png', 'VaporDev', '2023-01-01', 3.9),
        ('Red Dead Redemption 2', 1, 1500000, 'Cao bồi miền viễn Tây.', 'https://upload.wikimedia.org/wikipedia/en/4/44/Red_Dead_Redemption_II.jpg', 'Rockstar Games', '2018-10-26', 4.9),
        ('Hades', 2, 350000, 'Roguelike hành động.', 'https://upload.wikimedia.org/wikipedia/en/c/cc/Hades_cover_art.jpg', 'Supergiant Games', '2020-09-17', 4.7),
        ('Stardew Valley', 2, 200000, 'Nông trại thư giãn.', 'https://upload.wikimedia.org/wikipedia/en/f/fd/Logo_of_Stardew_Valley.svg', 'ConcernedApe', '2016-02-26', 4.9)
    ]
    cursor.executemany('''
        INSERT INTO Games (title, category_id, price, description, image_url, developer, release_date, rating) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', games_data)

    conn.commit()
    conn.close()
    print("Tạo Database và nạp dữ liệu mẫu THÀNH CÔNG!")

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Đã xóa Database cũ.")
    create_database()
