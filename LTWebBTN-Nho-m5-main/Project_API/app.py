"""VAPOR GAME STORE — Backend REST API (Flask + SQLite).

Chạy độc lập trên cổng 5000, Project_Client (cổng 5001) gọi sang đây qua HTTP.

Routes:
  Auth      : /api/register, /api/login, /api/users/<id>
  Games     : /api/games (search/filter/sort/paging), /api/games/<id>,
              POST/PUT/DELETE /api/games (admin)
  Categories: /api/categories (+ CRUD admin)
  Reviews   : /api/games/<id>/reviews (GET/POST)
  Wallet    : /api/wallet/deposit, /api/users/<id>/transactions
  Orders    : /api/checkout, /api/users/<id>/orders, /api/orders/<id>,
              /api/users/<id>/library
  Admin     : /api/admin/stats, /api/admin/revenue-monthly,
              /api/admin/top-games, /api/admin/orders
  Health    : /api/health

Khởi tạo dữ liệu:  python init_db.py
Chạy server      :  python app.py
"""

import math
import os
import sqlite3
import sys

from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

# Xem ghi chú trong init_db.py — pbkdf2 nhanh hơn scrypt nhiều lần trên Windows.
PASSWORD_METHOD = "pbkdf2:sha256:100000"

# Console Windows cp1252 không in được tiếng Việt — chuyển stream sang UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("VAPOR_DB_PATH", os.path.join(BASE_DIR, "game_store.db"))


# ==========================================
# HELPERS
# ==========================================

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise RuntimeError(
            "Chưa có file Database. Hãy chạy 'python init_db.py' trước!"
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def error(message, status=400):
    return jsonify({"error": message}), status


def public_user(row):
    """Loại bỏ mật khẩu khỏi thông tin trả về client."""
    user = dict(row)
    user.pop("password", None)
    return user


def get_user_or_none(conn, user_id):
    if user_id is None or str(user_id).strip() == "":
        return None
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    return conn.execute(
        "SELECT * FROM Users WHERE id = ?", (user_id,)
    ).fetchone()


def require_admin(conn, user_id):
    """Trả về (user, None) nếu hợp lệ, hoặc (None, response lỗi)."""
    user = get_user_or_none(conn, user_id)
    if user is None:
        return None, error("Không tìm thấy người dùng. Vui lòng đăng nhập!", 401)
    if user["role"] != "admin":
        return None, error("Quyền truy cập bị từ chối: chỉ Admin mới được thao tác này!", 403)
    return user, None


# ==========================================
# 0. HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "VAPOR GAME STORE API",
        "database": os.path.basename(DB_PATH),
    })


# ==========================================
# 1. API CHO NGƯỜI DÙNG (AUTH + PROFILE)
# ==========================================

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    email = (data.get("email") or "").strip().lower()

    if not username or not password or not email:
        return error("Vui lòng nhập đủ tên đăng nhập, email và mật khẩu!")

    if len(username) < 3:
        return error("Tên đăng nhập phải có ít nhất 3 ký tự!")

    if len(password) < 6:
        return error("Mật khẩu phải có ít nhất 6 ký tự!")

    if "@" not in email or "." not in email.split("@")[-1]:
        return error("Địa chỉ email không hợp lệ!")

    conn = get_db_connection()
    try:
        exists = conn.execute(
            "SELECT id FROM Users WHERE username = ? OR email = ?",
            (username, email),
        ).fetchone()
        if exists:
            return error("Tên đăng nhập hoặc email đã tồn tại!", 409)

        cursor = conn.execute(
            "INSERT INTO Users (username, password, email, role, balance) "
            "VALUES (?, ?, ?, 'user', 0)",
            (username, generate_password_hash(password, method=PASSWORD_METHOD), email),
        )
        conn.commit()

        new_user = conn.execute(
            "SELECT * FROM Users WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return jsonify({
            "message": "Đăng ký thành công",
            "user": public_user(new_user),
        }), 201
    finally:
        conn.close()


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return error("Vui lòng nhập tên đăng nhập và mật khẩu!")

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM Users WHERE username = ? OR email = ?",
            (username, username.lower()),
        ).fetchone()

        if user is None or not check_password_hash(user["password"], password):
            return error("Sai tài khoản hoặc mật khẩu!", 401)

        return jsonify({
            "message": "Đăng nhập thành công",
            "user": public_user(user),
        })
    finally:
        conn.close()


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM Users WHERE id = ?", (user_id,)).fetchone()
        if user is None:
            return error("Không tìm thấy người dùng!", 404)
        return jsonify(public_user(user))
    finally:
        conn.close()


# ==========================================
# 2. VÍ TIỀN (WALLET)
# ==========================================

@app.route("/api/wallet/deposit", methods=["POST"])
def wallet_deposit():
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        user = get_user_or_none(conn, data.get("user_id"))
        if user is None:
            return error("Không tìm thấy người dùng!", 404)

        try:
            amount = float(data.get("amount", 0))
        except (TypeError, ValueError):
            return error("Số tiền nạp không hợp lệ!")

        if amount <= 0 or amount > 50000000:
            return error("Số tiền nạp phải lớn hơn 0 và tối đa 50.000.000đ!")

        conn.execute(
            "UPDATE Users SET balance = balance + ? WHERE id = ?",
            (amount, user["id"]),
        )
        conn.execute(
            "INSERT INTO WalletTransactions (user_id, amount, kind, note) "
            "VALUES (?, ?, 'deposit', ?)",
            (user["id"], amount, data.get("note") or "Nạp tiền vào ví Vapor"),
        )
        conn.commit()
        fresh = conn.execute("SELECT * FROM Users WHERE id = ?", (user["id"],)).fetchone()
        return jsonify({"message": "Nạp tiền thành công", "user": public_user(fresh)}), 201
    finally:
        conn.close()


@app.route("/api/users/<int:user_id>/transactions", methods=["GET"])
def wallet_transactions(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM WalletTransactions WHERE user_id = ? "
            "ORDER BY id DESC LIMIT 50",
            (user_id,),
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


# ==========================================
# 3. API CHO THỂ LOẠI (CATEGORIES)
# ==========================================

@app.route("/api/categories", methods=["GET"])
def get_categories():
    conn = get_db_connection()
    try:
        rows = conn.execute("""
            SELECT Categories.*,
                   COUNT(Games.id) AS game_count
            FROM Categories
            LEFT JOIN Games ON Games.category_id = Categories.id
            GROUP BY Categories.id
            ORDER BY Categories.name ASC
        """).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route("/api/categories", methods=["POST"])
def create_category():
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, data.get("user_id"))
        if err:
            return err

        name = (data.get("name") or "").strip()
        slug = (data.get("slug") or "").strip().lower().replace(" ", "-")
        if not name or not slug:
            return error("Thể loại cần có cả tên và slug!")

        try:
            conn.execute(
                "INSERT INTO Categories (name, slug, icon) VALUES (?, ?, ?)",
                (name, slug, data.get("icon") or "◆"),
            )
            conn.commit()
            return jsonify({"message": "Đã tạo thể loại mới"}), 201
        except sqlite3.IntegrityError:
            return error("Slug thể loại đã tồn tại!", 409)
    finally:
        conn.close()


@app.route("/api/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, data.get("user_id"))
        if err:
            return err

        category = conn.execute(
            "SELECT * FROM Categories WHERE id = ?", (category_id,)
        ).fetchone()
        if category is None:
            return error("Không tìm thấy thể loại!", 404)

        name = (data.get("name") or category["name"]).strip()
        slug = (data.get("slug") or category["slug"]).strip().lower()
        icon = data.get("icon") or category["icon"]

        try:
            conn.execute(
                "UPDATE Categories SET name = ?, slug = ?, icon = ? WHERE id = ?",
                (name, slug, icon, category_id),
            )
            conn.commit()
            return jsonify({"message": "Đã cập nhật thể loại"})
        except sqlite3.IntegrityError:
            return error("Slug thể loại đã tồn tại!", 409)
    finally:
        conn.close()


@app.route("/api/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, request.args.get("user_id"))
        if err:
            return err

        used = conn.execute(
            "SELECT COUNT(*) FROM Games WHERE category_id = ?", (category_id,)
        ).fetchone()[0]
        if used > 0:
            return error(
                f"Không thể xóa: vẫn còn {used} game thuộc thể loại này!", 409
            )

        conn.execute("DELETE FROM Categories WHERE id = ?", (category_id,))
        conn.commit()
        return jsonify({"message": "Đã xóa thể loại"})
    finally:
        conn.close()


# ==========================================
# 4. API CHO GAME (SEARCH / FILTER / SORT / PAGING + CRUD)
# ==========================================

SORT_CLAUSES = {
    "newest": "Games.id DESC",
    "price_asc": "Games.price ASC",
    "price_desc": "Games.price DESC",
    "rating": "Games.rating DESC",
    "popular": "Games.sales DESC",
    "az": "Games.title ASC",
}


@app.route("/api/games", methods=["GET"])
def get_games():
    keyword = request.args.get("q", "").strip()
    category_id = request.args.get("category", "").strip()
    sort_by = request.args.get("sort", "newest")
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    free_only = request.args.get("free", "").strip() == "1"

    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    try:
        limit = min(120, max(1, int(request.args.get("limit", 24))))
    except ValueError:
        limit = 24

    conn = get_db_connection()
    try:
        query = """
            SELECT Games.*, Categories.name AS category_name,
                   Categories.slug AS category_slug,
                   Categories.icon AS category_icon
            FROM Games
            LEFT JOIN Categories ON Games.category_id = Categories.id
            WHERE 1=1
        """
        count_query = "SELECT COUNT(*) FROM Games LEFT JOIN Categories ON Games.category_id = Categories.id WHERE 1=1"
        params = []

        if keyword:
            like = f"%{keyword}%"
            condition = (
                " AND (Games.title LIKE ? OR Games.developer LIKE ? "
                "OR Games.description LIKE ? OR Games.tags LIKE ?)"
            )
            query += condition
            count_query += condition
            params.extend([like, like, like, like])

        if category_id:
            if category_id.isdigit():
                condition = " AND Games.category_id = ?"
                value = int(category_id)
            else:
                condition = (
                    " AND Games.category_id IN "
                    "(SELECT id FROM Categories WHERE slug = ?)"
                )
                value = category_id.lower()
            query += condition
            count_query += condition
            params.append(value)

        if free_only:
            query += " AND Games.price = 0"
            count_query += " AND Games.price = 0"
        else:
            if min_price.isdigit():
                query += " AND Games.price >= ?"
                count_query += " AND Games.price >= ?"
                params.append(int(min_price))
            if max_price.isdigit():
                query += " AND Games.price <= ?"
                count_query += " AND Games.price <= ?"
                params.append(int(max_price))

        total = conn.execute(count_query, params).fetchone()[0]
        pages = max(1, math.ceil(total / limit))
        page = min(page, pages)

        order = SORT_CLAUSES.get(sort_by, SORT_CLAUSES["newest"])
        query += f" ORDER BY {order} LIMIT ? OFFSET ?"
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, params + [limit, (page - 1) * limit]).fetchall()

        return jsonify({
            "items": [dict(r) for r in rows],
            "total": total,
            "page": page,
            "pages": pages,
            "limit": limit,
        })
    finally:
        conn.close()


@app.route("/api/games/<int:game_id>", methods=["GET"])
def get_game_detail(game_id):
    conn = get_db_connection()
    try:
        game = conn.execute("""
            SELECT Games.*, Categories.name AS category_name,
                   Categories.slug AS category_slug
            FROM Games
            LEFT JOIN Categories ON Games.category_id = Categories.id
            WHERE Games.id = ?
        """, (game_id,)).fetchone()

        if game is None:
            return error("Không tìm thấy Game!", 404)

        reviews = conn.execute("""
            SELECT Reviews.*, Users.username
            FROM Reviews
            JOIN Users ON Reviews.user_id = Users.id
            WHERE Reviews.game_id = ?
            ORDER BY Reviews.id DESC
            LIMIT 30
        """, (game_id,)).fetchall()

        review_count = conn.execute(
            "SELECT COUNT(*) FROM Reviews WHERE game_id = ?", (game_id,)
        ).fetchone()[0]

        related = conn.execute("""
            SELECT Games.*, Categories.name AS category_name
            FROM Games
            LEFT JOIN Categories ON Games.category_id = Categories.id
            WHERE Games.category_id = ? AND Games.id != ?
            ORDER BY Games.rating DESC
            LIMIT 4
        """, (game["category_id"], game_id)).fetchall()

        game_data = dict(game)
        game_data["reviews"] = [dict(r) for r in reviews]
        game_data["review_count"] = review_count
        game_data["related"] = [dict(r) for r in related]
        return jsonify(game_data)
    finally:
        conn.close()


@app.route("/api/games", methods=["POST"])
def create_game():
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, data.get("user_id"))
        if err:
            return err

        title = (data.get("title") or "").strip()
        if not title:
            return error("Tên game không được để trống!")

        try:
            price = float(data.get("price", 0))
        except (TypeError, ValueError):
            return error("Giá game không hợp lệ!")
        if price < 0:
            return error("Giá game không được âm!")

        category_id = data.get("category_id")
        if category_id and conn.execute(
            "SELECT id FROM Categories WHERE id = ?", (category_id,)
        ).fetchone() is None:
            return error("Thể loại không tồn tại!", 404)

        cursor = conn.execute("""
            INSERT INTO Games (title, category_id, price, description, image_url,
                               developer, release_date, rating, platforms, tags, sales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            title,
            int(category_id) if category_id else None,
            price,
            (data.get("description") or "").strip(),
            (data.get("image_url") or "").strip() or None,
            (data.get("developer") or "").strip(),
            data.get("release_date") or None,
            float(data.get("rating") or 0),
            data.get("platforms") or "PC",
            data.get("tags") or "",
        ))
        conn.commit()
        new_game = conn.execute(
            "SELECT * FROM Games WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return jsonify({"message": "Đã thêm game mới", "game": dict(new_game)}), 201
    finally:
        conn.close()


@app.route("/api/games/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, data.get("user_id"))
        if err:
            return err

        game = conn.execute("SELECT * FROM Games WHERE id = ?", (game_id,)).fetchone()
        if game is None:
            return error("Không tìm thấy Game!", 404)

        try:
            fields = {
                "title": (data.get("title") or game["title"]).strip(),
                "price": float(data.get("price", game["price"])),
                "description": data.get("description", game["description"]),
                "image_url": data.get("image_url", game["image_url"]),
                "developer": data.get("developer", game["developer"]),
                "release_date": data.get("release_date", game["release_date"]),
                "rating": float(data.get("rating", game["rating"])),
                "platforms": data.get("platforms", game["platforms"]),
                "tags": data.get("tags", game["tags"]),
            }
        except (TypeError, ValueError):
            return error("Dữ liệu cập nhật không hợp lệ!")

        if data.get("category_id") not in (None, ""):
            fields["category_id"] = int(data["category_id"])
        else:
            fields["category_id"] = game["category_id"]

        conn.execute("""
            UPDATE Games SET title=:title, price=:price, description=:description,
                image_url=:image_url, developer=:developer, release_date=:release_date,
                rating=:rating, platforms=:platforms, tags=:tags,
                category_id=:category_id
            WHERE id=:game_id
        """, {**fields, "game_id": game_id})
        conn.commit()

        updated = conn.execute("SELECT * FROM Games WHERE id = ?", (game_id,)).fetchone()
        return jsonify({"message": "Đã cập nhật game", "game": dict(updated)})
    finally:
        conn.close()


@app.route("/api/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, request.args.get("user_id"))
        if err:
            return err

        game = conn.execute("SELECT * FROM Games WHERE id = ?", (game_id,)).fetchone()
        if game is None:
            return error("Không tìm thấy Game!", 404)

        conn.execute("DELETE FROM Order_Details WHERE game_id = ?", (game_id,))
        conn.execute("DELETE FROM Reviews WHERE game_id = ?", (game_id,))
        conn.execute("DELETE FROM Games WHERE id = ?", (game_id,))
        conn.commit()
        return jsonify({"message": f"Đã xóa game '{game['title']}'"})
    finally:
        conn.close()


# ==========================================
# 5. API ĐÁNH GIÁ (REVIEWS)
# ==========================================

@app.route("/api/games/<int:game_id>/reviews", methods=["POST"])
def add_review(game_id):
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        user = get_user_or_none(conn, data.get("user_id"))
        if user is None:
            return error("Vui lòng đăng nhập để đánh giá game!", 401)

        game = conn.execute("SELECT id FROM Games WHERE id = ?", (game_id,)).fetchone()
        if game is None:
            return error("Không tìm thấy Game!", 404)

        try:
            rating = int(data.get("rating", 0))
        except (TypeError, ValueError):
            return error("Sao đánh giá không hợp lệ!")
        if rating < 1 or rating > 5:
            return error("Đánh giá phải từ 1 đến 5 sao!")

        comment = (data.get("comment") or "").strip()
        if not comment:
            return error("Vui lòng viết nhận xét cho game!")

        conn.execute(
            "INSERT INTO Reviews (game_id, user_id, rating, comment) VALUES (?, ?, ?, ?)",
            (game_id, user["id"], rating, comment[:1000]),
        )

        # Cập nhật lại điểm trung bình của game theo đánh giá thực tế
        conn.execute("""
            UPDATE Games SET rating = (
                SELECT ROUND(AVG(Reviews.rating), 1) FROM Reviews WHERE Reviews.game_id = Games.id
            ) WHERE id = ?
        """, (game_id,))
        conn.commit()

        return jsonify({"message": "Cảm ơn bạn đã đánh giá!"}), 201
    finally:
        conn.close()


# ==========================================
# 6. API ĐƠN HÀNG (CHECKOUT + LIBRARY)
# ==========================================

@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    try:
        user = get_user_or_none(conn, data.get("user_id"))
        if user is None:
            return error("Vui lòng đăng nhập để thanh toán!", 401)

        cart_items = data.get("cart") or []
        if not isinstance(cart_items, list) or not cart_items:
            return error("Giỏ hàng trống — không có gì để thanh toán!", 400)

        cursor = conn.cursor()
        total_amount = 0
        valid_ids = []

        for game_id in cart_items:
            try:
                game_id = int(game_id)
            except (TypeError, ValueError):
                continue
            game = cursor.execute(
                "SELECT * FROM Games WHERE id = ?", (game_id,)
            ).fetchone()
            if game is None:
                return error(f"Game #{game_id} không còn tồn tại trong cửa hàng!", 404)

            # Game đã sở hữu thì bỏ qua, không tính tiền 2 lần
            owned = cursor.execute(
                """SELECT 1 FROM Order_Details od
                   JOIN Orders o ON od.order_id = o.id
                   WHERE od.game_id = ? AND o.user_id = ?""",
                (game_id, user["id"]),
            ).fetchone()
            if owned:
                continue

            valid_ids.append(game_id)
            total_amount += game["price"]

        if user["balance"] < total_amount:
            return error(
                f"Số dư ví không đủ (cần {total_amount:,.0f}đ, bạn còn {user['balance']:,.0f}đ). "
                "Hãy nạp thêm tiền vào ví Vapor!",
                400,
            )

        if not valid_ids:
            return error("Tất cả game trong giỏ bạn đã sở hữu rồi!", 400)

        cursor.execute(
            "INSERT INTO Orders (user_id, total_amount, status) VALUES (?, ?, 'Success')",
            (user["id"], total_amount),
        )
        order_id = cursor.lastrowid

        for game_id in valid_ids:
            game = cursor.execute("SELECT price FROM Games WHERE id = ?", (game_id,)).fetchone()
            cursor.execute(
                "INSERT INTO Order_Details (order_id, game_id, price) VALUES (?, ?, ?)",
                (order_id, game_id, game["price"]),
            )
            cursor.execute(
                "UPDATE Games SET sales = sales + 1 WHERE id = ?", (game_id,)
            )

        cursor.execute(
            "UPDATE Users SET balance = balance - ? WHERE id = ?",
            (total_amount, user["id"]),
        )
        cursor.execute(
            "INSERT INTO WalletTransactions (user_id, amount, kind, note) VALUES (?, ?, 'purchase', ?)",
            (user["id"], -total_amount, f"Thanh toán đơn hàng #{order_id} ({len(valid_ids)} game)"),
        )
        conn.commit()

        return jsonify({
            "message": "Thanh toán thành công!",
            "order_id": order_id,
            "total": total_amount,
            "games": valid_ids,
            "new_balance": user["balance"] - total_amount,
        }), 201
    finally:
        conn.close()


@app.route("/api/users/<int:user_id>/orders", methods=["GET"])
def get_user_orders(user_id):
    conn = get_db_connection()
    try:
        orders = conn.execute(
            "SELECT * FROM Orders WHERE user_id = ? ORDER BY id DESC", (user_id,)
        ).fetchall()

        result = []
        for order in orders:
            items = conn.execute("""
                SELECT od.price, g.id AS game_id, g.title, g.image_url, g.rating
                FROM Order_Details od
                JOIN Games g ON od.game_id = g.id
                WHERE od.order_id = ?
            """, (order["id"],)).fetchall()
            data = dict(order)
            data["items"] = [dict(i) for i in items]
            result.append(data)

        return jsonify(result)
    finally:
        conn.close()


@app.route("/api/users/<int:user_id>/library", methods=["GET"])
def get_user_library(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute("""
            SELECT DISTINCT g.*, c.name AS category_name
            FROM Order_Details od
            JOIN Orders o ON od.order_id = o.id
            JOIN Games g ON od.game_id = g.id
            LEFT JOIN Categories c ON g.category_id = c.id
            WHERE o.user_id = ?
            ORDER BY g.title ASC
        """, (user_id,)).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


# ==========================================
# 7. API CHO ADMIN THỐNG KÊ
# ==========================================

@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, request.args.get("user_id"))
        if err:
            return err

        stats = {
            "total_users": conn.execute("SELECT COUNT(*) FROM Users").fetchone()[0],
            "total_games": conn.execute("SELECT COUNT(*) FROM Games").fetchone()[0],
            "total_categories": conn.execute("SELECT COUNT(*) FROM Categories").fetchone()[0],
            "total_orders": conn.execute("SELECT COUNT(*) FROM Orders").fetchone()[0],
            "total_reviews": conn.execute("SELECT COUNT(*) FROM Reviews").fetchone()[0],
            "total_revenue": conn.execute(
                "SELECT COALESCE(SUM(total_amount), 0) FROM Orders"
            ).fetchone()[0],
            "free_games": conn.execute(
                "SELECT COUNT(*) FROM Games WHERE price = 0"
            ).fetchone()[0],
            "average_order": conn.execute(
                "SELECT COALESCE(AVG(total_amount), 0) FROM Orders"
            ).fetchone()[0],
        }
        return jsonify(stats)
    finally:
        conn.close()


@app.route("/api/admin/revenue-monthly", methods=["GET"])
def admin_revenue_monthly():
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, request.args.get("user_id"))
        if err:
            return err

        rows = conn.execute("""
            SELECT strftime('%Y-%m', order_date) AS month,
                   SUM(total_amount) AS revenue,
                   COUNT(*) AS orders
            FROM Orders
            GROUP BY month
            ORDER BY month ASC
            LIMIT 12
        """).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route("/api/admin/top-games", methods=["GET"])
def admin_top_games():
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, request.args.get("user_id"))
        if err:
            return err

        rows = conn.execute("""
            SELECT g.id, g.title, g.price, g.rating, g.sales,
                   c.name AS category_name,
                   COALESCE(SUM(od.price), 0) AS revenue,
                   COUNT(od.id) AS sold
            FROM Games g
            LEFT JOIN Categories c ON g.category_id = c.id
            LEFT JOIN Order_Details od ON od.game_id = g.id
            GROUP BY g.id
            ORDER BY revenue DESC, g.sales DESC
            LIMIT 10
        """).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


@app.route("/api/admin/orders", methods=["GET"])
def admin_orders():
    conn = get_db_connection()
    try:
        _, err = require_admin(conn, request.args.get("user_id"))
        if err:
            return err

        rows = conn.execute("""
            SELECT o.*, u.username,
                   (SELECT COUNT(*) FROM Order_Details WHERE order_id = o.id) AS item_count
            FROM Orders o
            JOIN Users u ON o.user_id = u.id
            ORDER BY o.id DESC
            LIMIT 30
        """).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()


# ==========================================
# ERROR HANDLERS (JSON cho mọi lỗi)
# ==========================================

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "API endpoint không tồn tại!"}), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"error": "Phương thức request không được hỗ trợ!"}), 405


@app.errorhandler(Exception)
def unhandled_exception(exc):
    app.logger.exception("Lỗi server không mong muốn")
    return jsonify({"error": f"Lỗi server: {exc}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
