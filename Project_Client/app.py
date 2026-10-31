import os
import sqlite3

from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, session, abort
)

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "vapor_secret_key_change_before_deploy"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "game_store.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT DEFAULT 'user'
        )
    """)

    columns = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(Users)").fetchall()
    }

    if "email" not in columns:
        conn.execute("ALTER TABLE Users ADD COLUMN email TEXT")

    if "role" not in columns:
        conn.execute(
            "ALTER TABLE Users ADD COLUMN role TEXT DEFAULT 'user'"
        )

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    conn.commit()
    conn.close()



categories = [
    {"id": 1, "name": "Action"},
    {"id": 2, "name": "RPG"},
    {"id": 3, "name": "Strategy"}
]

games = [
    {
        "id": 1,
        "title": "Grand Theft Auto V",
        "category_id": 1,
        "category_name": "Action",
        "price": 500000,
        "description": "Game thế giới mở đỉnh cao.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png"
    },
    {
        "id": 2,
        "title": "The Witcher 3: Wild Hunt",
        "category_id": 2,
        "category_name": "RPG",
        "price": 400000,
        "description": "Siêu phẩm nhập vai.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Witcher_3_cover_art.jpg"
    },
    {
        "id": 3,
        "title": "Age of Empires IV",
        "category_id": 3,
        "category_name": "Strategy",
        "price": 800000,
        "description": "Game chiến thuật thời gian thực.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/e/e2/Age_of_Empires_IV_cover_art.jpg"
    },
    {
        "id": 4,
        "title": "Elden Ring",
        "category_id": 2,
        "category_name": "RPG",
        "price": 1200000,
        "description": "Game Souls-like đình đám.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Elden_Ring_Box_art.jpg"
    }
]


@app.route("/")
def index():
    keyword = request.args.get("q", "").strip().lower()
    category_id = request.args.get("category", "").strip()

    result = games.copy()

    if keyword:
        result = [
            game for game in result
            if keyword in game["title"].lower()
            or keyword in game["description"].lower()
        ]

    if category_id.isdigit():
        result = [
            game for game in result
            if game["category_id"] == int(category_id)
        ]

    logged_in_user = None

    if session.get("user_id"):
        logged_in_user = {
            "username": session.get("username")
        }

    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template(
        "index.html",
        games=result,
        categories=categories,
        keyword=request.args.get("q", ""),
        selected_category=category_id,
        logged_in_user=logged_in_user,
        cart_count=cart_count
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Vui lòng nhập tên đăng nhập và mật khẩu!", "error")
            return render_template("login.html")

        conn = get_db_connection()

        try:
            user = conn.execute("""
                SELECT id, username, password
                FROM Users
                WHERE username = ?
            """, (username,)).fetchone()

            if user is None:
                flash(
                    "Tài khoản không tồn tại. Vui lòng đăng ký tài khoản!",
                    "error"
                )
                return render_template("login.html")

            stored_password = user["password"]

            try:
                password_valid = check_password_hash(
                    stored_password, password
                )
            except (ValueError, TypeError):
                password_valid = False

            if not password_valid and stored_password == password:
                password_valid = True

                new_password = generate_password_hash(password)

                conn.execute("""
                    UPDATE Users
                    SET password = ?
                    WHERE id = ?
                """, (new_password, user["id"]))

                conn.commit()

            if not password_valid:
                flash("Mật khẩu không chính xác. Vui lòng thử lại!", "error")
                return render_template("login.html")

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("Đăng nhập thành công! Chào mừng bạn đến với Vapor.", "success")

            return redirect(url_for("index"))

        except sqlite3.Error:
            app.logger.exception("Lỗi đăng nhập")
            flash("Không thể kết nối dữ liệu tài khoản. Vui lòng thử lại!", "error")
            return render_template("login.html")

        finally:
            conn.close()

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password or not confirm_password:
            flash("Vui lòng nhập đầy đủ thông tin!", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp!", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Mật khẩu phải có ít nhất 6 ký tự!", "error")
            return render_template("register.html")

        conn = get_db_connection()

        try:
            # Kiểm tra tài khoản và email
            user = conn.execute("""
                SELECT id FROM Users
                WHERE username = ? OR email = ?
            """, (username, email)).fetchone()

            if user:
                flash(
                    "Tên đăng nhập hoặc email đã tồn tại. Vui lòng sử dụng thông tin khác!",
                    "error"
                )
                return render_template("register.html")


            hashed_password = generate_password_hash(password)


            conn.execute("""
                INSERT INTO Users (username, email, password, role)
                VALUES (?, ?, ?, 'user')
            """, (username, email, hashed_password))

            conn.commit()

            flash(
                "Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.",
                "success"
            )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            conn.rollback()
            flash("Tài khoản hoặc email đã được sử dụng!", "error")

        except sqlite3.Error as e:
            conn.rollback()
            app.logger.exception("Lỗi đăng ký tài khoản")
            flash("Không thể lưu tài khoản vào hệ thống. Vui lòng thử lại!", "error")

        finally:
            conn.close()

        return render_template("register.html")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất thành công.", "success")
    return redirect(url_for("index"))


@app.route("/cart")
def cart():
    return redirect(url_for("index"))

@app.route("/game/<int:game_id>")
def game_detail(game_id):

    game = next(
        (item for item in games if item["id"] == game_id),
        None
    )

    if game is None:
        abort(404)

    related_games = [
        item for item in games
        if item["id"] != game_id
        and item["category_id"] == game["category_id"]
    ]

    if not related_games:
        related_games = [
            item for item in games
            if item["id"] != game_id
        ]

    related_games = related_games[:3]

    logged_in_user = None

    if session.get("user_id"):
        logged_in_user = {
            "username": session.get("username")
        }

    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template(
        "game_detail.html",
        game=game,
        related_games=related_games,
        logged_in_user=logged_in_user,
        cart_count=cart_count
    )


@app.route("/cart/add/<int:game_id>", methods=["POST"])
def add_to_cart(game_id):
    return redirect(url_for("index"))



if __name__ == "__main__":
    init_auth_db()
    app.run(debug=True)
