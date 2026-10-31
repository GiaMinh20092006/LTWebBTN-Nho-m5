from flask import Flask, request, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_PATH = 'game_store.db'

def get_db_connection():
    if not os.path.exists(DB_PATH):
        print("CẢNH BÁO: Chưa có file Database. Hãy chạy file init_db.py trước!")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# 1. API CHO NGƯỜI DÙNG (USERS)
# ==========================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Vui lòng nhập đủ thông tin"}), 400

    hashed_pw = generate_password_hash(password)

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO Users (username, password, email) VALUES (?, ?, ?)', (username, hashed_pw, email))
        conn.commit()
        return jsonify({"message": "Đăng ký thành công"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Tên đăng nhập hoặc email đã tồn tại"}), 409
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        user_info = dict(user)
        del user_info['password'] # Bảo mật
        return jsonify({"message": "Đăng nhập thành công", "user": user_info}), 200
    
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
# 3. API CHO GAME (GAMES - NÂNG CAO)
# ==========================================

@app.route('/api/games', methods=['GET'])
def get_games():
    # Hỗ trợ Tìm kiếm, Lọc theo thể loại, và Sắp xếp
    keyword = request.args.get('q', '')
    category_id = request.args.get('category', '')
    sort_by = request.args.get('sort', 'id_desc') # Mặc định là mới nhất

    conn = get_db_connection()
    query = '''
        SELECT Games.*, Categories.name as category_name 
        FROM Games 
        LEFT JOIN Categories ON Games.category_id = Categories.id
        WHERE 1=1
    '''
    params = []

    if keyword:
        query += " AND (Games.title LIKE ? OR Games.developer LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    
    if category_id:
        query += " AND Games.category_id = ?"
        params.append(category_id)

    # Xử lý sắp xếp
    if sort_by == 'price_asc':
        query += " ORDER BY Games.price ASC"
    elif sort_by == 'price_desc':
        query += " ORDER BY Games.price DESC"
    elif sort_by == 'rating':
        query += " ORDER BY Games.rating DESC"
    else:
        query += " ORDER BY Games.id DESC"

    games = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in games])

@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game_detail(game_id):
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM Games WHERE id = ?', (game_id,)).fetchone()
    
    if not game:
        conn.close()
        return jsonify({"error": "Không tìm thấy Game"}), 404
        
    # Lấy thêm reviews của game này
    reviews = conn.execute('''
        SELECT Reviews.*, Users.username 
        FROM Reviews JOIN Users ON Reviews.user_id = Users.id 
        WHERE Reviews.game_id = ?
    ''', (game_id,)).fetchall()
    conn.close()

    game_data = dict(game)
    game_data['reviews'] = [dict(r) for r in reviews]
    
    return jsonify(game_data)

# ==========================================
# 4. API CHO ĐƠN HÀNG (CHECKOUT)
# ==========================================

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    user_id = data.get('user_id')
    cart_items = data.get('cart') # List các game_id

    if not user_id or not cart_items:
        return jsonify({"error": "Thiếu thông tin đơn hàng"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    total_amount = 0
    # Tính tổng tiền
    for game_id in cart_items:
        game = cursor.execute('SELECT price FROM Games WHERE id = ?', (game_id,)).fetchone()
        if game:
            total_amount += game['price']

    # Tạo Order
    cursor.execute('INSERT INTO Orders (user_id, total_amount) VALUES (?, ?)', (user_id, total_amount))
    order_id = cursor.lastrowid

    # Thêm Order_Details
    for game_id in cart_items:
        game = cursor.execute('SELECT price FROM Games WHERE id = ?', (game_id,)).fetchone()
        if game:
            cursor.execute('INSERT INTO Order_Details (order_id, game_id, price) VALUES (?, ?, ?)', (order_id, game_id, game['price']))

    conn.commit()
    conn.close()
    return jsonify({"message": "Thanh toán thành công", "order_id": order_id, "total": total_amount}), 201

# ==========================================
# 5. API CHO ADMIN THỐNG KÊ
# ==========================================

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    conn = get_db_connection()
    total_users = conn.execute('SELECT COUNT(*) FROM Users').fetchone()[0]
    total_games = conn.execute('SELECT COUNT(*) FROM Games').fetchone()[0]
    total_revenue = conn.execute('SELECT SUM(total_amount) FROM Orders').fetchone()[0] or 0
    conn.close()
    
    return jsonify({
        "total_users": total_users,
        "total_games": total_games,
        "total_revenue": total_revenue
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
