from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime
import json
from pathlib import Path


app = Flask(__name__)
app.secret_key = "change-this-secret"

# Static credentials (no register)
STATIC_USER = {"username": "admin", "password": "1234"}

# Static rooms (no DB)
ROOMS = [
    {
        "id": 1,
        "name": "Cairo Comfort Single",
        "type": "Single",
        "price": 55,
        "capacity": 1,
        "size": 220,
        "bedType": "Twin",
        "floor": 2,
        "rating": 4.5,
        "amenities": ["Wi-Fi", "AC", "Breakfast", "Desk"],
        "image": "https://images.unsplash.com/photo-1568495248636-6432b97bd949?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "desc": "A quiet minimalist single room, perfect for solo travelers. Features modern Egyptian decor with warm earth tones and a comfortable workspace."
    },
    {
        "id": 2,
        "name": "Nile View Double",
        "type": "Double",
        "price": 85,
        "capacity": 2,
        "size": 320,
        "bedType": "Queen",
        "floor": 4,
        "rating": 4.7,
        "amenities": ["Wi-Fi", "AC", "Balcony", "Breakfast"],
        "image": "https://images.unsplash.com/photo-1505692952047-1a78307da8f2?auto=format&fit=crop&w=1200&q=60",
        "desc": "A bright double room with a relaxing city view. Wake up to stunning views and enjoy the spacious balcony overlooking the bustling streets."
    },
    {
        "id": 3,
        "name": "Lux Suite",
        "type": "Suite",
        "price": 160,
        "capacity": 4,
        "size": 520,
        "bedType": "King",
        "floor": 6,
        "rating": 4.9,
        "amenities": ["Wi-Fi", "AC", "Jacuzzi", "Living Area", "Breakfast"],
        "image": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1200&q=60",
        "desc": "Premium suite with extra space and comfort for families. Features a separate living area, luxurious jacuzzi, and elegant furnishings."
    },
    {
        "id": 4,
        "name": "Alexandria Sea Breeze",
        "type": "Double",
        "price": 95,
        "capacity": 2,
        "size": 350,
        "bedType": "Queen",
        "floor": 5,
        "rating": 4.6,
        "amenities": ["Wi-Fi", "AC", "Sea View", "Mini Bar", "Breakfast"],
        "image": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=60",
        "desc": "Mediterranean-inspired coastal room with refreshing sea breeze ambiance. Perfect for couples seeking a romantic getaway with ocean views."
    },
    {
        "id": 5,
        "name": "Pharaoh's Royal Chamber",
        "type": "Suite",
        "price": 220,
        "capacity": 4,
        "size": 680,
        "bedType": "King",
        "floor": 8,
        "rating": 5.0,
        "amenities": ["Wi-Fi", "AC", "Jacuzzi", "Living Area", "Butler Service", "Breakfast", "Private Terrace"],
        "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=60",
        "desc": "Our most luxurious Egyptian-themed suite inspired by ancient royalty. Features gold accents, premium amenities, butler service, and a private terrace."
    },
    {
        "id": 6,
        "name": "Aswan Desert Oasis",
        "type": "Single",
        "price": 65,
        "capacity": 1,
        "size": 250,
        "bedType": "Twin",
        "floor": 3,
        "rating": 4.4,
        "amenities": ["Wi-Fi", "AC", "Breakfast", "Spa Access"],
        "image": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=1200&q=60",
        "desc": "A tranquil desert-themed retreat with warm sandy tones and calming atmosphere. Includes complimentary spa access for ultimate relaxation."
    },
]

# Static "reservations" stored in session (still no DB)
# session["reservations"] = list of dicts

def load_test_results():
    results_dir = Path("test_results")
    latest_file = results_dir / "latest.json"
    history_file = results_dir / "history.json"

    latest = None
    history = []

    if latest_file.exists():
        try:
            latest = json.loads(latest_file.read_text(encoding="utf-8"))
        except Exception:
            latest = None

    if history_file.exists():
        try:
            history = json.loads(history_file.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                history = []
        except Exception:
            history = []

    return latest, history



def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please login first.", "warning")
            return redirect(url_for("login", next=request.path))
        return view_func(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    q = request.args.get("q", "").strip().lower()
    featured = ROOMS[:3]

    if q:
        filtered = [
            r for r in ROOMS
            if q in r["name"].lower() or q in r["type"].lower() or q in r["desc"].lower()
        ]
        featured = filtered[:3]

    return render_template("home.html", featured=featured, q=q)


@app.route("/rooms")
def rooms():
    q = request.args.get("q", "").strip().lower()
    room_type = request.args.get("type", "").strip()
    max_price = request.args.get("max_price", "").strip()

    data = ROOMS

    # search
    if q:
        data = [
            r for r in data
            if q in r["name"].lower() or q in r["type"].lower() or q in r["desc"].lower()
        ]

    # filter by type
    if room_type:
        data = [r for r in data if r["type"] == room_type]

    # filter by max price
    if max_price:
        try:
            mp = float(max_price)
            data = [r for r in data if r["price"] <= mp]
        except ValueError:
            flash("Max price must be a number.", "warning")

    types = sorted(list({r["type"] for r in ROOMS}))
    return render_template("rooms.html", rooms=data, q=q, types=types, selected_type=room_type, max_price=max_price)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == STATIC_USER["username"] and password == STATIC_USER["password"]:
            session["logged_in"] = True
            session["username"] = username
            session.setdefault("reservations", [])
            flash("Login successful!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("home"))

        flash("Wrong username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))


@app.route("/booking", methods=["GET", "POST"])
@login_required
def booking():
    # optional preselect room from querystring
    room_id = request.args.get("room_id", "").strip()
    selected_room = None
    if room_id.isdigit():
        selected_room = next((r for r in ROOMS if r["id"] == int(room_id)), None)

    if request.method == "POST":
        chosen_room_id = request.form.get("room_id", "").strip()
        check_in = request.form.get("check_in", "").strip()
        check_out = request.form.get("check_out", "").strip()
        guests = request.form.get("guests", "1").strip()

        if not chosen_room_id or not check_in or not check_out:
            flash("Please select a room and dates.", "danger")
            return render_template("booking.html", rooms=ROOMS, selected_room=selected_room)

        room = next((r for r in ROOMS if r["id"] == int(chosen_room_id)), None)
        if not room:
            flash("Room not found.", "danger")
            return render_template("booking.html", rooms=ROOMS, selected_room=selected_room)

        # basic date validation
        try:
            ci = datetime.strptime(check_in, "%Y-%m-%d").date()
            co = datetime.strptime(check_out, "%Y-%m-%d").date()
            if co <= ci:
                flash("Check-out must be after check-in.", "danger")
                return render_template("booking.html", rooms=ROOMS, selected_room=room)
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("booking.html", rooms=ROOMS, selected_room=room)

        try:
            guests_int = int(guests)
        except ValueError:
            guests_int = 1

        if guests_int < 1 or guests_int > room["capacity"]:
            flash(f"Guests must be between 1 and {room['capacity']}.", "danger")
            return render_template("booking.html", rooms=ROOMS, selected_room=room)

        reservation = {
            "id": len(session["reservations"]) + 1,
            "room_id": room["id"],
            "room_name": room["name"],
            "room_type": room["type"],
            "check_in": str(ci),
            "check_out": str(co),
            "guests": guests_int,
            "status": "Booked"
        }

        session["reservations"].append(reservation)
        session.modified = True

        flash("Reservation created successfully!", "success")
        return redirect(url_for("reservations"))

    return render_template("booking.html", rooms=ROOMS, selected_room=selected_room)


@app.route("/reservations")
@login_required
def reservations():
    q = request.args.get("q", "").strip().lower()
    status = request.args.get("status", "").strip()

    items = session.get("reservations", [])

    if q:
        items = [r for r in items if q in r["room_name"].lower() or q in r["room_type"].lower()]

    if status:
        items = [r for r in items if r["status"] == status]

    return render_template("reservations.html", reservations=items, q=q, status=status)


@app.route("/reservations/<int:res_id>/cancel", methods=["POST"])
@login_required
def cancel_reservation(res_id):
    items = session.get("reservations", [])
    for r in items:
        if r["id"] == res_id:
            r["status"] = "Cancelled"
            session.modified = True
            flash("Reservation cancelled.", "info")
            break
    return redirect(url_for("reservations"))


@app.route("/dashboard")
@login_required
def dashboard():
    items = session.get("reservations", [])
    total_res = len(items)
    booked = len([r for r in items if r["status"] == "Booked"])
    cancelled = len([r for r in items if r["status"] == "Cancelled"])
    total_rooms = len(ROOMS)
    latest_test, test_history = load_test_results()
    
    recent = list(reversed(items))[:6]
    return render_template(
        "dashboard.html",
        total_rooms=total_rooms,
        total_res=total_res,
        booked=booked,
        cancelled=cancelled,
        recent=recent,
        latest_test=latest_test,
        test_history=test_history
    )


# test route 
@app.route("/test/reset")
def test_reset():
    # Clear session so each test starts clean (logged out + no reservations)
    session.clear()
    return "OK", 200



if __name__ == "__main__":
    app.run(debug=True)
