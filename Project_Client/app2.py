from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = "vapor_secret_key_change_before_deploy"
API_URL = 'http://127.0.0.1:5000/api'

# Hàm hỗ trợ lấy dữ liệu từ API
def fetch_api(endpoint):
    try:
        response = requests.get(f'{API_URL}/{endpoint}')
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        print("Lỗi: Không thể kết nối tới API (Cổng 5000)")
    return []

@app.route("/")
def index():
    games = fetch_api('games')
    categories = fetch_api('categories')
    
    # Xử lý tìm kiếm & lọc (Có thể lọc ngay trên API, nhưng ở đây lọc qua Python cho nhanh)
    keyword = request.args.get("q", "").strip().lower()
    category_id = request.args.get("category", "").strip()

    if keyword:
        games = [g for g in games if keyword in g['title'].lower() or keyword in g['description'].lower()]
    if category_id.isdigit():
        games = [g for g in games if g['category_id'] == int(category_id)]

    logged_in_user = session.get('user')
    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template("index.html", 
                           games=games, 
                           categories=categories,
                           keyword=request.args.get("q", ""),
                           selected_category=category_id,
                           logged_in_user=logged_in_user,
                           cart_count=cart_count)

@app.route("/game/<int:game_id>")
def game_detail(game_id):
    # Gọi API lấy chi tiết 1 game
    response = requests.get(f'{API_URL}/games/{game_id}')
    if response.status_code != 200:
        return "Không tìm thấy game", 404
    
    game = response.json()
    games = fetch_api('games') # Lấy toàn bộ để làm "Game liên quan"
    
    related_games = [g for g in games if g['id'] != game_id and g['category_id'] == game['category_id']][:3]
    
    logged_in_user = session.get('user')
    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template("game_detail.html", game=game, related_games=related_games, logged_in_user=logged_in_user, cart_count=cart_count)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }
        # Gọi API Đăng nhập
        response = requests.post(f'{API_URL}/login', json=data)
        
        if response.status_code == 200:
            user_data = response.json()['user']
            session['user'] = user_data
            flash("Đăng nhập thành công! Chào mừng đến với Vapor.", "success")
            return redirect(url_for('index'))
        else:
            flash("Sai tài khoản hoặc mật khẩu!", "error")
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'email': request.form.get('email')
        }
        # Gọi API Đăng ký
        response = requests.post(f'{API_URL}/register', json=data)
        if response.status_code == 201:
            flash("Đăng ký thành công! Hãy đăng nhập.", "success")
            return redirect(url_for('login'))
        else:
            flash(response.json().get('error', 'Lỗi đăng ký'), "error")
            
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("Đã đăng xuất.", "success")
    return redirect(url_for('index'))

# ==========================================
# PHẦN VIỆC CỦA ĐỨC HIẾU (GIỎ HÀNG & ADMIN)
# ==========================================

@app.route("/cart")
def cart():
    cart_dict = session.get('cart', {})
    cart_items = []
    total_amount = 0
    
    # Lấy thông tin từng game từ API để hiển thị
    if cart_dict:
        all_games = fetch_api('games')
        for game_id, quantity in cart_dict.items():
            game = next((g for g in all_games if g['id'] == int(game_id)), None)
            if game:
                game_copy = game.copy()
                game_copy['quantity'] = quantity
                cart_items.append(game_copy)
                total_amount += game['price'] * quantity

    logged_in_user = session.get('user')
    return render_template("cart.html", items=cart_items, total=total_amount, logged_in_user=logged_in_user, cart_count=sum(cart_dict.values()))

@app.route("/cart/add/<int:game_id>", methods=["POST"])
def add_to_cart(game_id):
    cart = session.get('cart', {})
    game_id_str = str(game_id)
    
    if game_id_str in cart:
        cart[game_id_str] += 1
    else:
        cart[game_id_str] = 1
        
    session['cart'] = cart
    flash("Đã thêm game vào giỏ hàng!", "success")
    return redirect(request.referrer or url_for('index'))

@app.route("/cart/remove/<int:game_id>")
def remove_from_cart(game_id):
    cart = session.get('cart', {})
    if str(game_id) in cart:
        del cart[str(game_id)]
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route("/checkout", methods=["POST"])
def checkout():
    if 'user' not in session:
        flash("Vui lòng đăng nhập để thanh toán!", "error")
        return redirect(url_for('login'))
        
    cart_dict = session.get('cart', {})
    if not cart_dict:
        return redirect(url_for('cart'))

    # Chuẩn bị data gửi lên API Checkout
    cart_game_ids = [int(k) for k in cart_dict.keys()]
    data = {
        'user_id': session['user']['id'],
        'cart': cart_game_ids
    }
    
    response = requests.post(f'{API_URL}/checkout', json=data)
    
    if response.status_code == 201:
        session.pop('cart', None) # Xóa giỏ hàng sau khi mua thành công
        flash("Thanh toán thành công! Game đã được thêm vào thư viện của bạn.", "success")
        return redirect(url_for('index'))
    else:
        flash("Có lỗi xảy ra khi thanh toán.", "error")
        return redirect(url_for('cart'))

@app.route("/admin")
def admin_dashboard():
    # Chỉ admin mới được vào
    if 'user' not in session or session['user']['role'] != 'admin':
        flash("Bạn không có quyền truy cập trang này!", "error")
        return redirect(url_for('index'))
        
    games = fetch_api('games')
    try:
        stats = requests.get(f'{API_URL}/admin/stats').json()
    except:
        stats = {"total_users": 0, "total_games": 0, "total_revenue": 0}

    return render_template("admin.html", games=games, stats=stats, logged_in_user=session['user'], cart_count=sum(session.get('cart', {}).values()))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
