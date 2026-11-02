"""VAPOR GAME STORE — Web Client (Flask, cổng 5001).

Toàn bộ dữ liệu (game, người dùng, đơn hàng, ví, đánh giá, thống kê)
đều lấy từ Project_API (http://127.0.0.1:5000) qua HTTP — client KHÔNG
chạm trực tiếp vào SQLite.

Chạy:  python app.py            (đảm bảo API đang chạy ở cổng 5000)
"""

import hashlib
import os
import sys
from urllib.parse import urlencode

import requests
from flask import (
    Flask, abort, flash, redirect, render_template, request, session, url_for,
)

# Console Windows cp1252 không in được tiếng Việt — chuyển stream sang UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

app = Flask(__name__)

app.secret_key = os.environ.get(
    "VAPOR_SECRET_KEY", "vapor_secret_key_change_before_deploy"
)

API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
API_TIMEOUT = float(os.environ.get("API_TIMEOUT", "15"))

PAGE_SIZE = 24


# ==========================================
# API HELPERS
# ==========================================

class ApiDown(Exception):
    pass


def api_call(method, path, **kwargs):
    """Gọi API và trả về dict/list. Ném ApiDown nếu API chưa chạy."""
    url = f"{API_BASE_URL}{path}"
    kwargs.setdefault("timeout", API_TIMEOUT)
    try:
        resp = requests.request(method, url, **kwargs)
    except requests.RequestException:
        raise ApiDown()

    try:
        payload = resp.json()
    except ValueError:
        raise ApiDown()

    if resp.status_code >= 400:
        return {"__error__": payload.get("error", "API trả về lỗi không rõ."),
                "__status__": resp.status_code}
    return payload


def api_get(path, params=None):
    return api_call("GET", path, params=params)


def api_post(path, data=None, params=None):
    return api_call("POST", path, json=data, params=params)


def api_put(path, data=None):
    return api_call("PUT", path, json=data)


def api_delete(path, params=None):
    return api_call("DELETE", path, params=params)


def relay_api_error(result, fallback):
    """Nếu API trả lỗi, flash lỗi và trả True để route dừng lại."""
    if isinstance(result, dict) and "__error__" in result:
        flash(result["__error__"], "error")
        return True
    return False


# ==========================================
# SESSION: ĐĂNG NHẬP + GIỎ HÀNG
# ==========================================

def current_user():
    return session.get("user")


def require_login():
    if not current_user():
        flash("Vui lòng đăng nhập để tiếp tục!", "warning")
        return redirect(url_for("login", next=request.path))
    return None


def cart_ids():
    return session.get("cart", [])


def cart_count():
    return len(cart_ids())


@app.context_processor
def inject_globals():
    user = current_user()
    return {
        "logged_in_user": user,
        "is_admin": bool(user and user.get("role") == "admin"),
        "cart_count": cart_count(),
        "vnd": vnd_format,
        "api_base": API_BASE_URL,
    }


def vnd_format(value):
    try:
        return "{:,.0f}".format(float(value)).replace(",", ".") + "đ"
    except (TypeError, ValueError):
        return "0đ"


# ==========================================
# TRANG CHỦ: DANH MỤC GAME (SEARCH/FILTER/SORT/PAGING)
# ==========================================

@app.route("/")
def index():
    keyword = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "newest")
    max_price = request.args.get("max_price", "").strip()
    free = "1" if request.args.get("free") == "1" else ""

    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1

    params = {"q": keyword, "category": category, "sort": sort,
              "page": page, "limit": PAGE_SIZE}
    if max_price:
        params["max_price"] = max_price
    if free:
        params["free"] = 1

    games_data = api_get("/api/games", params)
    if relay_api_error(games_data, None):
        games_data = {"items": [], "total": 0, "page": 1, "pages": 1}

    categories = api_get("/api/categories")
    if relay_api_error(categories, None):
        categories = []

    return render_template(
        "index.html",
        games=games_data["items"],
        total_games=games_data.get("total", 0),
        page=games_data.get("page", 1),
        pages=games_data.get("pages", 1),
        categories=categories,
        keyword=keyword,
        selected_category=category,
        selected_sort=sort,
        max_price=max_price,
        free_only=free,
    )


# ==========================================
# TRANG CHI TIẾT GAME + ĐÁNH GIÁ
# ==========================================

@app.route("/game/<int:game_id>")
def game_detail(game_id):
    game = api_get(f"/api/games/{game_id}")
    if isinstance(game, dict) and game.get("__status__") == 404:
        abort(404)
    if relay_api_error(game, None):
        abort(503)

    user = current_user()
    in_cart = game_id in cart_ids()
    already_reviewed = False
    if user:
        already_reviewed = any(
            r["user_id"] == user["id"] for r in game.get("reviews", [])
        )

    return render_template(
        "game_detail.html",
        game=game,
        in_cart=in_cart,
        already_reviewed=already_reviewed,
    )


@app.route("/game/<int:game_id>/review", methods=["POST"])
def post_review(game_id):
    redirect_url = url_for("game_detail", game_id=game_id)
    guard = require_login()
    if guard:
        return guard

    result = api_post(f"/api/games/{game_id}/reviews", {
        "user_id": current_user()["id"],
        "rating": request.form.get("rating", 0),
        "comment": request.form.get("comment", ""),
    })
    if relay_api_error(result, None):
        return redirect(redirect_url + "#reviews")

    flash("Gửi đánh giá thành công! Cảm ơn bạn đã đồng hành cùng Vapor.", "success")
    return redirect(redirect_url + "#reviews")


# ==========================================
# GIỎ HÀNG (lưu trong session, chỉ lưu game_id)
# ==========================================

@app.route("/cart")
def cart():
    items = []
    total = 0
    for game_id in cart_ids():
        game = api_get(f"/api/games/{game_id}")
        if isinstance(game, dict) and "id" in game:
            items.append(game)
            total += game.get("price", 0)
        else:
            # Game đã bị admin xóa khỏi DB — dọn giỏ hàng tương ứng
            session["cart"] = [g for g in cart_ids() if g != game_id]

    user = current_user()
    balance = user.get("balance", 0) if user else 0

    return render_template("cart.html", items=items, total=total, balance=balance)


@app.route("/cart/add/<int:game_id>", methods=["POST"])
def add_to_cart(game_id):
    game = api_get(f"/api/games/{game_id}")
    if "id" not in game:
        flash("Game không tồn tại trong cửa hàng!", "error")
        return redirect(url_for("index"))

    cart = cart_ids()
    if game_id in cart:
        flash("Game đã nằm trong giỏ hàng rồi!", "warning")
    else:
        cart.append(game_id)
        session["cart"] = cart
        flash(f"Đã thêm '{game['title']}' vào giỏ hàng!", "success")

    return redirect(request.form.get("next") or url_for("index"))


@app.route("/cart/remove/<int:game_id>", methods=["POST"])
def remove_from_cart(game_id):
    session["cart"] = [g for g in cart_ids() if g != game_id]
    return redirect(url_for("cart"))


@app.route("/cart/clear", methods=["POST"])
def clear_cart():
    session["cart"] = []
    flash("Đã xóa toàn bộ giỏ hàng.", "success")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    guard = require_login()
    if guard:
        return guard

    cart = cart_ids()
    if not cart:
        flash("Giỏ hàng đang trống!", "warning")
        return redirect(url_for("cart"))

    result = api_post("/api/checkout", {
        "user_id": current_user()["id"],
        "cart": cart,
    })
    if relay_api_error(result, None):
        return redirect(url_for("cart"))

    session["cart"] = []
    # Cập nhật lại số dư ví trong session
    user = current_user()
    user["balance"] = result.get("new_balance", user.get("balance", 0))
    session["user"] = user

    flash(
        f"Thanh toán thành công! Đơn hàng #{result['order_id']} "
        f"tổng {vnd_format(result['total'])} — chúc bạn chơi vui!",
        "success",
    )
    return redirect(url_for("orders"))


# ==========================================
# ĐƠN HÀNG + THƯ VIỆN GAME ĐÃ SỞ HỮU
# ==========================================

@app.route("/orders")
def orders():
    guard = require_login()
    if guard:
        return guard

    data = api_get(f"/api/users/{current_user()['id']}/orders")
    if relay_api_error(data, None):
        data = []
    return render_template("orders.html", orders=data)


@app.route("/library")
def library():
    guard = require_login()
    if guard:
        return guard

    data = api_get(f"/api/users/{current_user()['id']}/library")
    if relay_api_error(data, None):
        data = []
    return render_template("library.html", games=data)


# ==========================================
# VÍ TIỀN (WALLET)
# ==========================================

@app.route("/wallet")
def wallet():
    guard = require_login()
    if guard:
        return guard

    user_id = current_user()["id"]
    fresh = api_get(f"/api/users/{user_id}")
    if not relay_api_error(fresh, None):
        stored = current_user()
        stored["balance"] = fresh.get("balance", stored.get("balance", 0))
        session["user"] = stored

    transactions = api_get(f"/api/users/{user_id}/transactions")
    if relay_api_error(transactions, None):
        transactions = []

    return render_template("wallet.html", transactions=transactions)


@app.route("/wallet/deposit", methods=["POST"])
def wallet_deposit():
    guard = require_login()
    if guard:
        return guard

    result = api_post("/api/wallet/deposit", {
        "user_id": current_user()["id"],
        "amount": request.form.get("amount", 0),
        "note": request.form.get("note", ""),
    })
    if relay_api_error(result, None):
        return redirect(url_for("wallet"))

    session["user"] = result["user"]
    flash(f"Nạp ví thành công! Số dư hiện tại: {vnd_format(result['user']['balance'])}", "success")
    return redirect(url_for("wallet"))


# ==========================================
# ĐĂNG NHẬP / ĐĂNG KÝ / ĐĂNG XUẤT (qua API)
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = api_post("/api/login", {
            "username": request.form.get("username", "").strip(),
            "password": request.form.get("password", ""),
        })
        if relay_api_error(result, None):
            return render_template("login.html")

        session["user"] = result["user"]
        flash(f"Đăng nhập thành công! Chào mừng {result['user']['username']} "
              "đến với thế giới Vapor.", "success")
        return redirect(request.args.get("next") or url_for("index"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if password != confirm:
            flash("Mật khẩu xác nhận không khớp!", "error")
            return render_template("register.html")

        result = api_post("/api/register", {
            "username": request.form.get("username", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": password,
        })
        if relay_api_error(result, None):
            return render_template("register.html")

        flash("Đăng ký thành công! Vui lòng đăng nhập để tiếp tục.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất khỏi Vapor. Hẹn gặp lại!", "success")
    return redirect(url_for("index"))


# ==========================================
# TRANG ADMIN (CRUD GAME + THỐNG KÊ)
# ==========================================

def require_admin():
    user = current_user()
    if not user or user.get("role") != "admin":
        return None
    return user


def admin_guard():
    if require_admin() is None:
        flash("Trang này chỉ dành cho quản trị viên!", "error")
        return redirect(url_for("index"))
    return None


@app.route("/admin")
def admin():
    blocked = admin_guard()
    if blocked:
        return blocked

    admin_id = require_admin()["id"]
    stats = api_get("/api/admin/stats", params={"user_id": admin_id})
    if relay_api_error(stats, None):
        stats = {}
    monthly = api_get("/api/admin/revenue-monthly", params={"user_id": admin_id})
    if relay_api_error(monthly, None):
        monthly = []
    top_games = api_get("/api/admin/top-games", params={"user_id": admin_id})
    if relay_api_error(top_games, None):
        top_games = []
    recent_orders = api_get("/api/admin/orders", params={"user_id": admin_id})
    if relay_api_error(recent_orders, None):
        recent_orders = []

    game_q = request.args.get("q", "").strip()
    try:
        game_page = max(1, int(request.args.get("gpage", 1)))
    except ValueError:
        game_page = 1
    params = {"sort": "popular", "limit": 30, "page": game_page}
    if game_q:
        params["q"] = game_q
    games_page = api_get("/api/games", params=params)
    if relay_api_error(games_page, None):
        games_page = {"items": [], "pages": 1, "total": 0}
    categories = api_get("/api/categories")
    if relay_api_error(categories, None):
        categories = []

    return render_template(
        "admin.html",
        stats=stats,
        monthly=monthly,
        top_games=top_games,
        recent_orders=recent_orders,
        games=games_page.get("items", []),
        game_page=games_page.get("page", game_page),
        game_pages=games_page.get("pages", 1),
        game_total=games_page.get("total", 0),
        game_q=game_q,
        categories=categories,
    )


@app.route("/admin/game/create", methods=["POST"])
def admin_create_game():
    blocked = admin_guard()
    if blocked:
        return blocked
    user = require_admin()
    result = api_post("/api/games", {
        "user_id": user["id"],
        "title": request.form.get("title", ""),
        "category_id": request.form.get("category_id", ""),
        "price": request.form.get("price", 0),
        "description": request.form.get("description", ""),
        "developer": request.form.get("developer", ""),
        "release_date": request.form.get("release_date", ""),
        "rating": request.form.get("rating", 0),
        "platforms": request.form.get("platforms", "PC"),
        "tags": request.form.get("tags", ""),
    })
    if relay_api_error(result, None):
        return redirect(url_for("admin"))

    flash(f"Đã thêm game '{result['game']['title']}' vào cửa hàng!", "success")
    return redirect(url_for("admin"))


@app.route("/admin/game/<int:game_id>/update", methods=["POST"])
def admin_update_game(game_id):
    blocked = admin_guard()
    if blocked:
        return blocked
    user = require_admin()
    result = api_put(f"/api/games/{game_id}", {
        "user_id": user["id"],
        "title": request.form.get("title", ""),
        "category_id": request.form.get("category_id", ""),
        "price": request.form.get("price", 0),
        "description": request.form.get("description", ""),
        "developer": request.form.get("developer", ""),
        "release_date": request.form.get("release_date", ""),
        "rating": request.form.get("rating", 0),
        "platforms": request.form.get("platforms", ""),
        "tags": request.form.get("tags", ""),
    })
    if relay_api_error(result, None):
        return redirect(url_for("admin"))

    flash("Đã cập nhật thông tin game!", "success")
    return redirect(url_for("admin"))


@app.route("/admin/game/<int:game_id>/delete", methods=["POST"])
def admin_delete_game(game_id):
    blocked = admin_guard()
    if blocked:
        return blocked
    user = require_admin()
    result = api_delete(f"/api/games/{game_id}", params={"user_id": user["id"]})
    if relay_api_error(result, None):
        return redirect(url_for("admin"))

    flash(result.get("message", "Đã xóa game."), "success")
    return redirect(url_for("admin"))


@app.route("/admin/category/create", methods=["POST"])
def admin_create_category():
    blocked = admin_guard()
    if blocked:
        return blocked
    user = require_admin()
    result = api_post("/api/categories", {
        "user_id": user["id"],
        "name": request.form.get("name", ""),
        "slug": request.form.get("slug", ""),
        "icon": request.form.get("icon", ""),
    })
    if relay_api_error(result, None):
        return redirect(url_for("admin"))

    flash("Đã tạo thể loại mới!", "success")
    return redirect(url_for("admin"))


@app.route("/admin/category/<int:category_id>/delete", methods=["POST"])
def admin_delete_category(category_id):
    blocked = admin_guard()
    if blocked:
        return blocked
    user = require_admin()
    result = api_delete(f"/api/categories/{category_id}",
                        params={"user_id": user["id"]})
    if relay_api_error(result, None):
        return redirect(url_for("admin"))

    flash("Đã xóa thể loại!", "success")
    return redirect(url_for("admin"))


# ==========================================
# COVER NEON SVG (vẽ poster procedural cho từng game)
# ==========================================

SVG_PALETTES = [
    ("#ff2e88", "#7b2ff7", "#05d9e8"),
    ("#05d9e8", "#010920", "#ff2e88"),
    ("#f72585", "#7209b7", "#4cc9f0"),
    ("#ffd200", "#ff2e88", "#3a0ca3"),
    ("#2affdf", "#1f0640", "#ff6ec7"),
    ("#b026ff", "#ff2079", "#00f0ff"),
]

SVG_WORDS = {
    "action": "ACTION", "rpg": "RPG", "strategy": "STRATEGY",
    "shooter": "SHOOTER", "horror": "HORROR", "adventure": "ADVENTURE",
    "racing": "RACING", "sports": "SPORTS", "puzzle": "PUZZLE",
    "simulation": "SIM", "indie": "INDIE", "mmo": "MMO",
}


def svg_escape(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def wrap_title(title, per_line=14, max_lines=3):
    words, lines, current = title.split(), [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if len(candidate) <= per_line:
            current = candidate
        else:
            lines.append(current)
            current = word[:per_line]
    if current:
        lines.append(current)
    return lines[:max_lines]


@app.route("/cover/<int:game_id>.svg")
def game_cover(game_id):
    seed = hashlib.md5(str(game_id).encode()).hexdigest()
    palette = SVG_PALETTES[int(seed[:4], 16) % len(SVG_PALETTES)]
    neon, deep, accent = palette

    game = api_get(f"/api/games/{game_id}")
    title = game.get("title") if isinstance(game, dict) and "title" in game \
        else "VAPOR GAME"
    slug = (game.get("category_slug") or "").lower() if isinstance(game, dict) else ""
    tag = SVG_WORDS.get(slug, "VAPOR")

    lines = wrap_title(title)
    title_spans = "".join(
        f'<text x="160" y="{252 + i * 40 - (len(lines) - 1) * 18}" '
        f'text-anchor="middle" font-family="Arial Black, Arial, sans-serif" '
        f'font-size="30" font-weight="900" fill="#ffffff" '
        f'stroke="{accent}" stroke-width="0.6">{svg_escape(line.upper())}</text>'
        for i, line in enumerate(lines)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="320" height="420"
 viewBox="0 0 320 420" role="img" aria-label="{svg_escape(title)}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{deep}"/>
      <stop offset="0.55" stop-color="#12002f"/>
      <stop offset="1" stop-color="{neon}"/>
    </linearGradient>
    <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{accent}"/>
      <stop offset="1" stop-color="{neon}"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#00000000"/>
      <stop offset="1" stop-color="#05010fdd"/>
    </linearGradient>
  </defs>
  <rect width="320" height="420" fill="url(#sky)"/>
  <circle cx="160" cy="150" r="86" fill="url(#sun)" opacity="0.9"/>
  <rect x="60" y="150" width="200" height="8" fill="#05010f" opacity="0.75"/>
  <rect x="60" y="168" width="200" height="11" fill="#05010f" opacity="0.75"/>
  <rect x="60" y="190" width="200" height="15" fill="#05010f" opacity="0.75"/>
  <rect x="60" y="216" width="200" height="20" fill="#05010f" opacity="0.75"/>
  <g stroke="{accent}" stroke-width="1" opacity="0.65">
    <line x1="0" y1="300" x2="320" y2="300"/><line x1="0" y1="330" x2="320" y2="330"/>
    <line x1="0" y1="368" x2="320" y2="368"/><line x1="0" y1="412" x2="320" y2="412"/>
    <line x1="160" y1="270" x2="-90" y2="420"/><line x1="160" y1="270" x2="10" y2="420"/>
    <line x1="160" y1="270" x2="80" y2="420"/><line x1="160" y1="270" x2="160" y2="420"/>
    <line x1="160" y1="270" x2="240" y2="420"/><line x1="160" y1="270" x2="310" y2="420"/>
    <line x1="160" y1="270" x2="410" y2="420"/>
  </g>
  <rect y="230" width="320" height="120" fill="url(#fade)"/>
  {title_spans}
  <rect x="18" y="18" width="{26 + 11 * len(tag)}" height="26" rx="6"
        fill="#05010fcc" stroke="{accent}"/>
  <text x="{31 + 5.5 * len(tag)}" y="36" text-anchor="middle"
        font-family="monospace" font-size="14" font-weight="bold"
        fill="{accent}">{svg_escape(tag)}</text>
  <text x="160" y="398" text-anchor="middle" font-family="monospace"
        font-size="12" letter-spacing="4" fill="{accent}">V A P O R</text>
</svg>"""
    return svg, 200, {"Content-Type": "image/svg+xml"}


@app.route("/cover-fallback.svg")
def cover_fallback():
    return redirect(url_for("game_cover", game_id=0))


def game_image(game):
    """Ưu tiên image_url thật, nếu kosong dùng cover SVG neon của client."""
    url = (game.get("image_url") or "").strip() if isinstance(game, dict) else ""
    if url:
        return url
    return url_for("game_cover", game_id=game.get("id", 0))


app.jinja_env.globals["game_image"] = game_image


# ==========================================
# LINK PHÂN TRANG (giữ nguyên bộ lọc hiện tại)
# ==========================================

def page_url(p):
    args = {k: v for k, v in request.args.items() if k != "page"}
    args["page"] = str(p)
    return url_for("index") + "?" + urlencode(args)


app.jinja_env.globals["page_url"] = page_url


# ==========================================
# ERROR PAGES
# ==========================================

@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


@app.errorhandler(503)
def api_offline(_):
    return render_template("503.html", api_base=API_BASE_URL), 503


@app.errorhandler(ApiDown)
def handle_api_down(_):
    return render_template("503.html", api_base=API_BASE_URL), 503


if __name__ == "__main__":
    port = int(os.environ.get("CLIENT_PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
