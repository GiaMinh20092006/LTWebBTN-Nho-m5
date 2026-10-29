from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'game_store.db'

# Hàm hỗ trợ kết nối Database
def get_db_connection():
    # Nếu file DB không tồn tại, nhắc nhở chạy init_db.py
    if not os.path.exists(DB_PATH):
        print("CẢNH BÁO: Chưa có file Database. Hãy chạy file init_db.py trước!")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Giúp trả về dữ liệu dạng Dictionary (key: value)
    return conn

# ==========================================
# 1. API CHO NGƯỜI DÙNG (USERS)
# ==========================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Vui lòng nhập đủ username và password"}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()

    if user:
        # Trả về thông tin user (ẩn password đi cho bảo mật)
        user_info = dict(user)
        del user_info['password']
        return jsonify({"message": "Đăng nhập thành công", "user": user_info}), 200
    else:
        return jsonify({"error": "Sai tài khoản hoặc mật khẩu"}), 401


# ==========================================
# 2. API CHO THỂ LOẠI (CATEGORIES)
# ==========================================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM Categories').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in categories])


# ==========================================
# 3. API CHO GAME (GAMES - CRUD)
# ==========================================

# Lấy toàn bộ danh sách Game (kèm theo tên thể loại)
@app.route('/api/games', methods=['GET'])
def get_games():
    conn = get_db_connection()
    # Dùng JOIN để lấy thêm tên thể loại (Category name) thay vì chỉ có ID
    query = '''
        SELECT Games.*, Categories.name as category_name 
        FROM Games 
        LEFT JOIN Categories ON Games.category_id = Categories.id
    '''
    games = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in games])

# Lấy chi tiết 1 Game theo ID
@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM Games WHERE id = ?', (game_id,)).fetchone()
    conn.close()
    
    if game is None:
        return jsonify({"error": "Không tìm thấy Game"}), 404
    return jsonify(dict(game))

# Thêm Game mới (Dành cho Admin)
@app.route('/api/games', methods=['POST'])
def add_game():
    data = request.json
    # Kiểm tra dữ liệu đầu vào cơ bản
    if not data.get('title') or not data.get('price'):
        return jsonify({"error": "Thiếu thông tin (title, price)"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Games (title, category_id, price, description, image_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (data.get('title'), data.get('category_id'), data.get('price'), 
          data.get('description', ''), data.get('image_url', '')))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"message": "Thêm Game thành công", "id": new_id}), 201

# Cập nhật thông tin Game (Dành cho Admin)
@app.route('/api/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Kiểm tra xem game có tồn tại không
    game = cursor.execute('SELECT * FROM Games WHERE id = ?', (game_id,)).fetchone()
    if not game:
        conn.close()
        return jsonify({"error": "Không tìm thấy Game"}), 404

    cursor.execute('''
        UPDATE Games 
        SET title = ?, category_id = ?, price = ?, description = ?, image_url = ?
        WHERE id = ?
    ''', (data.get('title'), data.get('category_id'), data.get('price'), 
          data.get('description'), data.get('image_url'), game_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Cập nhật Game thành công"}), 200

# Xóa Game (Dành cho Admin)
@app.route('/api/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM Games WHERE id = ?', (game_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    if rows_affected == 0:
        return jsonify({"error": "Không tìm thấy Game để xóa"}), 404
        
    return jsonify({"message": f"Đã xóa Game có ID {game_id}"}), 200


# Chạy Server API
if __name__ == '__main__':
    # Chạy ở cổng 5000
    app.run(debug=True, port=5000)
