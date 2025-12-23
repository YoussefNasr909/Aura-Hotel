# 🎓 AURA Hotel - Complete Technical Mentor Guide

## Purpose
This guide is designed to prepare you for **project discussions and technical interviews**. It covers architecture, Flask fundamentals, pytest + Selenium integration, line-by-line code explanations, and a comprehensive Q&A section.

---

## Table of Contents
1. [Big Picture: Architecture & Integration](#1-big-picture-architecture--integration)
2. [Tools: What, How, Why](#2-tools-what-how-why)
3. [Flask Functionality Deep Dive](#3-flask-functionality-deep-dive)
4. [Test Suite: Line-by-Line Walkthrough](#4-test-suite-line-by-line-walkthrough)
5. [Project Discussion Q&A Bank](#5-project-discussion-qa-bank)
6. [Mental Model Summary](#6-mental-model-summary)
7. [Troubleshooting Tips](#7-troubleshooting-tips)

---

## 1. Big Picture: Architecture & Integration

### 1.1 What the Flask App Does

**AURA Hotel** is a hotel room booking demonstration application. It allows users to:
- Browse and search hotel rooms
- View detailed room information
- Create bookings (requires login)
- Manage reservations (cancel/delete)
- View dashboard statistics and test results

### 1.2 Request Flow Diagram

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │ 1. HTTP Request (GET /rooms)
       ▼
┌──────────────────────────────────────┐
│         Flask App (app.py)           │
│  ┌────────────────────────────────┐  │
│  │  Route Handler (@app.route)    │  │
│  │  def rooms():                  │  │
│  │    - Parse query params        │  │
│  │    - Filter ROOMS data         │  │
│  │    - Prepare context           │  │
│  └────────┬───────────────────────┘  │
│           │ 2. Calls render_template │
│           ▼                           │
│  ┌────────────────────────────────┐  │
│  │  Jinja2 Template Engine        │  │
│  │  - Loads templates/rooms.html  │  │
│  │  - Injects context variables   │  │
│  │  - Loops/conditionals          │  │
│  └────────┬───────────────────────┘  │
└───────────┼───────────────────────────┘
            │ 3. Rendered HTML
            │ (with Bootstrap CSS)
            ▼
    ┌───────────────┐
    │  Static Files │
    │  /static/css/ │
    └───────┬───────┘
            │ 4. CSS/JS loaded by browser
            ▼
    ┌──────────────┐
    │   Response   │
    │ (Full HTML)  │
    └──────────────┘
```

**Step-by-Step Explanation:**

1. **Client sends HTTP request**: User clicks a link or submits a form → Browser sends `GET /rooms?q=suite` to Flask server
2. **Flask routing**: Flask matches the URL to `@app.route("/rooms")` decorator → calls the `rooms()` function
3. **Business logic**: The function:
   - Reads query parameters (`request.args.get("q")`)
   - Filters the `ROOMS` list based on search criteria
   - Prepares data to pass to the template
4. **Template rendering**: `render_template("rooms.html", rooms=data, ...)` loads the Jinja2 template and injects variables
5. **Template processing**: Jinja2 executes loops (`{% for r in rooms %}`), conditionals, and variable substitutions (`{{ r.name }}`)
6. **HTML generation**: A complete HTML document is created
7. **Static files**: Browser requests CSS/JS files using `<link>` and `<script>` tags (served via `/static/` route)
8. **Response**: Flask sends the final HTML to the browser which renders it

### 1.3 Flask App Structure

```
app.py (Single-file app)
├── Imports (Flask, datetime, json, functools)
├── App initialization: app = Flask(__name__)
├── Configuration: app.secret_key
├── Static data: ROOMS, STATIC_USER
├── Helper functions: load_test_results(), login_required()
├── Route handlers (9 routes):
│   ├── / (home)
│   ├── /rooms (room listing)
│   ├── /login (authentication)
│   ├── /logout
│   ├── /booking (create reservation)
│   ├── /reservations (view all)
│   ├── /reservations/<id>/cancel
│   ├── /reservations/<id>/delete
│   ├── /dashboard
│   └── /test/reset (test helper)
└── Main entry: if __name__ == "__main__": app.run()
```

**Why single-file?**
- Simple demonstration project
- No database models to separate
- Easier for students to understand the flow
- Production apps would use **Blueprints** to modularize

### 1.4 Test Structure

```
tests/
├── conftest.py          # Shared fixtures and hooks
│   ├── @pytest.fixture: driver()
│   ├── @pytest.fixture: base_url()
│   ├── Hook: pytest_terminal_summary()
│   └── Helper: send_test_notification()
│
├── test_auth.py         # Login/logout tests
│   ├── test_login_success()
│   ├── test_login_failure()
│   └── test_protected_page_redirects_to_login()
│
├── test_rooms_search.py # Search/filter tests
│   ├── test_rooms_search_suite_found()
│   ├── test_rooms_search_no_results()
│   ├── test_rooms_filter_by_type()
│   ├── test_rooms_filter_by_max_price()
│   └── test_rooms_filter_combined()
│
├── test_booking_reservations.py  # Booking flow tests
│   ├── test_create_booking_then_cancel()
│   ├── test_booking_validation_checkout_before_checkin()
│   ├── test_booking_validation_guests_exceed_capacity()
│   └── test_delete_cancelled_reservation()
│
└── test_dashboard.py    # Dashboard tests
    ├── test_dashboard_requires_login()
    ├── test_dashboard_shows_room_stats()
    └── test_dashboard_shows_test_automation_section()
```

**Naming Convention:**
- Test files: `test_*.py` (pytest auto-discovery)
- Test functions: `test_*()` (pytest requirement)
- Fixtures: descriptive names (`driver`, `base_url`)

**Discovery:** When you run `pytest`, it:
1. Scans the `tests/` directory
2. Finds all files matching `test_*.py`
3. Collects all functions matching `test_*()`
4. Executes them in isolation

### 1.5 How Selenium Talks to Flask

```
Terminal 1:              Terminal 2:
┌─────────────────┐      ┌──────────────────┐
│  Flask Server   │      │  Pytest + Selenium│
│  python app.py  │      │  pytest -v        │
│                 │      │                   │
│  Listening on:  │      │  1. Launches Chrome│
│  127.0.0.1:5000 │◄─────┤  2. driver.get()  │
│                 │ HTTP │  3. Sends requests│
│  Responds with  ├─────►│  4. Asserts HTML  │
│  HTML/JSON      │      │  5. Quits driver  │
└─────────────────┘      └──────────────────┘
```

**Critical Integration Points:**

1. **BASE_URL configuration** (`conftest.py` line 18):
   ```python
   BASE_URL = "http://127.0.0.1:5000"
   ```
   Tests assume Flask is running on this address.

2. **Test isolation via `/test/reset`** (`app.py` lines 348-352):
   ```python
   @app.route("/test/reset")
   def test_reset():
       session.clear()
       return "OK", 200
   ```
   Each test calls this to start with a clean state.

3. **WebDriver lifecycle**:
   - `@pytest.fixture` creates a new browser instance per test
   - Test executes (navigates, clicks, asserts)
   - `yield` hands control to test
   - Fixture cleanup (`driver.quit()`) runs after test

### 1.6 Test Data Setup and Cleanup

**Setup (before each test):**
```python
def test_example(driver, base_url):
    reset_session(driver, base_url)  # Clears session
    login(driver, base_url)          # Logs in with static credentials
    # Test logic here...
```

**Why this approach?**
- No database = no SQL truncate needed
- Session-based state = just clear cookies
- Idempotent tests = each can run independently
- Predictable state = room 1 always has capacity 1

**Cleanup:**
- Selenium driver quits automatically (`yield drv` in fixture)
- Sessions clear between tests via `/test/reset`
- No database rollback needed

---

## 2. Tools: What, How, Why

### 2.1 What is Selenium?

**Selenium** is a browser automation framework. It lets you programmatically control a web browser (Chrome, Firefox, Safari, Edge) to:
- Navigate to URLs
- Find elements (by ID, CSS selector, XPath)
- Interact with elements (click, type, select)
- Read page content (text, attributes, HTML)
- Take screenshots
- Execute JavaScript

**Core Components:**
1. **WebDriver**: API for browser control
2. **Browser Driver**: Executable that controls the actual browser (ChromeDriver for Chrome)
3. **Language Bindings**: Python, Java, C#, JavaScript libraries

### 2.2 What Problem Does Selenium Solve?

**Problem:** How do you verify a web application works correctly **from the user's perspective**?

Traditional unit/integration tests:
```python
# Tests the function directly
response = app.test_client().get('/rooms')
assert response.status_code == 200
```

**What's missing?**
- Does the rendered HTML actually display correctly?
- Can users **see** the room cards?
- Does clicking "Book" navigate to the booking page?
- Are form validations working in the browser?
- Does JavaScript execute correctly?

**Selenium's solution:**
```python
# Tests through the actual browser
driver.get("http://localhost:5000/rooms")
room_card = driver.find_element(By.CSS_SELECTOR, "[data-test='room-book-1']")
assert room_card.is_displayed()
room_card.click()
assert "/booking" in driver.current_url
```

**What kind of tests does Selenium enable?**
- **End-to-End (E2E) tests**: Full user journeys (login → search → book → verify)
- **UI tests**: Visual elements display correctly
- **Integration tests**: Frontend + Backend + Browser working together
- **Regression tests**: Ensure UI doesn't break after code changes

### 2.3 What is pytest?

**pytest** is a Python testing framework that makes writing tests simple and scalable.

**Core Features:**

1. **Simple test syntax:**
   ```python
   def test_addition():
       assert 1 + 1 == 2  # No special assertEqual() needed
   ```

2. **Fixtures:** Reusable setup/teardown code
   ```python
   @pytest.fixture
   def database():
       db = create_db()
       yield db  # Test runs here
       db.cleanup()
   ```

3. **Parametrization:** Run same test with different inputs
   ```python
   @pytest.mark.parametrize("x,y,expected", [
       (1, 1, 2),
       (5, 3, 8),
   ])
   def test_add(x, y, expected):
       assert x + y == expected
   ```

4. **Markers:** Tag tests for selective execution
   ```python
   @pytest.mark.slow
   def test_heavy_query():
       ...
   ```

5. **Rich assertion messages:**
   ```python
   assert {"a": 1} == {"a": 2}
   # Output: AssertionError: assert {'a': 1} == {'a': 2}
   #         Differing items: {'a': 1 != 2}
   ```

6. **Hooks:** Customize test behavior (e.g., `pytest_terminal_summary` to export JSON reports)

7. **Plugins:** pytest-html, pytest-xdist (parallel), pytest-cov (coverage)

**How pytest runs tests:**
```
1. Test Collection Phase:
   - Scans for test_*.py files
   - Finds test_*() functions
   - Builds test queue

2. Setup Phase (for each test):
   - Execute fixtures (@pytest.fixture)
   - Run setup code

3. Execution Phase:
   - Run test function
   - Collect results

4. Teardown Phase:
   - Run fixture cleanup (code after yield)
   - Close resources

5. Reporting Phase:
   - terminal_summary hook (we export JSON here)
   - Generate HTML report (pytest-html)
```

### 2.4 Why pytest + Selenium for This Project?

**Why not just Flask test client?**
| Flask Test Client | Selenium |
|-------------------|----------|
| ❌ No JavaScript execution | ✅ Full browser environment |
| ❌ No CSS rendering | ✅ Can verify visual elements |
| ❌ No user interactions | ✅ Clicks, scrolls, hovers |
| ✅ Fast | ⚠️ Slower |
| ✅ No browser needed | ❌ Requires browser installation |
| ✅ Good for API/backend | ✅ Tests the **actual user experience** |

**Why pytest over unittest?**
| unittest | pytest |
|----------|--------|
| More verbose (`self.assertEqual()`) | Clean assertions (`assert x == y`) |
| setUp/tearDown methods | Fixtures (more flexible) |
| No parametrization built-in | `@pytest.mark.parametrize` |
| Standard library (no install) | More features, better errors |

**Decision for this project:**
- **Goal:** Practice **E2E testing** for QA roles
- **Use case:** Verify complete user workflows
- **Learning objective:** Understand browser automation
- **Trade-off:** Sacrifice speed for realism

### 2.5 What We Used Specifically

**Selenium Components Used:**

1. **WebDriver** (`webdriver.Chrome`):
   - The main browser controller
   - Created in conftest.py fixture

2. **By locators** (`By.CSS_SELECTOR`, `By.TAG_NAME`):
   - `CSS_SELECTOR`: Most common, uses CSS syntax
   - `TAG_NAME`, `ID`, `XPATH`: Alternative locators

3. **WebDriverWait** (explicit waits):
   ```python
   WebDriverWait(driver, 5).until(
       EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="flash"]'))
   )
   ```
   **Why:** Page elements load asynchronously, must wait for them

4. **Expected Conditions** (`EC.url_contains`, `EC.presence_of_element_located`):
   - Reusable wait conditions
   - Avoid flaky tests from race conditions

5. **Select** (dropdown handling):
   ```python
   Select(element).select_by_value("1")
   ```

6. **JavaScript execution**:
   ```python
   driver.execute_script("document.querySelector('input').value = '2025-01-01';")
   ```
   **Why:** Date inputs are hard to interact with via send_keys()

7. **Alert handling**:
   ```python
   driver.switch_to.alert.accept()
   ```
   **Why:** JavaScript confirm() dialogs block Selenium until handled

**pytest Features Used:**

1. **Fixtures** (`driver`, `base_url`):
   - Provide clean browser instance per test
   - Centralize configuration

2. **Hooks** (`pytest_terminal_summary`):
   - Export test results to JSON
   - Send email notifications

3. **Plugins**:
   - `pytest-html`: Generate HTML reports
   - `webdriver-manager`: Auto-download ChromeDriver

**Why these specific tools?**
- **data-test attributes**: Makes locators resilient to UI changes
- **Explicit waits**: More reliable than implicit waits or sleep()
- **Headless mode**: Run tests in CI without GUI
- **WebDriver Manager**: Eliminates manual driver version management

---

## 3. Flask Functionality Deep Dive

### 3.1 Core Flask Concepts

**What is Flask?**
A **micro web framework** for Python. "Micro" means:
- Small core (routing, templates, requests)
- Extensions for databases, auth, etc.
- You assemble what you need

**Minimal Flask app:**
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

app.run()
```

### 3.2 Routing

**How it works:**
```python
@app.route("/rooms")
def rooms():
    return render_template("rooms.html")
```

- `@app.route(path)` is a **decorator**
- Maps URL patterns to Python functions
- Supports HTTP methods: GET (default), POST, PUT, DELETE

**Dynamic routes:**
```python
@app.route("/reservations/<int:res_id>/cancel", methods=["POST"])
def cancel_reservation(res_id):
    # res_id is automatically converted to int
    ...
```

### 3.3 Request/Response Lifecycle

**1. Request Object** (`from flask import request`):
```python
request.method          # "GET" or "POST"
request.args            # Query params (?q=suite)
request.form            # POST form data
request.json            # JSON payload
request.cookies         # Cookies
request.headers         # HTTP headers
request.path            # "/rooms"
request.url             # Full URL
```

**Example from app.py:**
```python
q = request.args.get("q", "").strip().lower()  # Get "q" param, default to ""
```

**2. Response:**
- **String return:** `return "OK"` → Flask converts to HTTP response
- **Tuple return:** `return "OK", 200` → (body, status code)
- **Redirect:** `return redirect(url_for("home"))` → 302 redirect
- **Template:** `return render_template("rooms.html", rooms=data)` → HTML response

### 3.4 Sessions and Cookies

**What is a session?**
A way to store user-specific data **across requests**. HTTP is stateless (each request is independent), sessions provide continuity.

**Flask sessions:**
```python
from flask import session

# Store data
session["logged_in"] = True
session["username"] = "admin"

# Read data
if session.get("logged_in"):
    print(f"User: {session.get('username')}")

# Clear session
session.clear()
```

**How it works:**
1. Flask serializes session dict to JSON
2. Signs it with `app.secret_key`
3. Stores in browser cookie named `session`
4. Browser sends cookie with every request
5. Flask deserializes and verifies signature

**Security:**
- Cookie is signed but **not encrypted**
- Don't store passwords or secrets in session
- Use a strong random `secret_key`

**In our app:**
```python
session["reservations"] = [
    {"id": 1, "room_name": "Suite", ...}
]
session.modified = True  # Force Flask to save changes
```

**Why `modified = True`?**
Flask only saves session if you reassign it. Modifying a list inside session doesn't trigger save unless you mark it.

### 3.5 Forms and Validation

**HTML Form:**
```html
<form method="post">
    <input name="username" required>
    <input name="password" type="password" required>
    <button type="submit">Login</button>
</form>
```

**Flask handler:**
```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if username == "admin" and password == "1234":
            session["logged_in"] = True
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        
        flash("Wrong username or password.", "danger")
    
    return render_template("login.html")
```

**Validation levels:**
1. **Client-side (HTML5):** `required`, `type="email"`, `min`, `max`
   - Good UX, but not secure (can be bypassed)
2. **Server-side (Flask):** Check in route handler
   - Required for security
   - In our app: date validation, guest capacity checks

**Example (booking validation):**
```python
ci = datetime.strptime(check_in, "%Y-%m-%d").date()
co = datetime.strptime(check_out, "%Y-%m-%d").date()
if co <= ci:
    flash("Check-out must be after check-in.", "danger")
    return render_template("booking.html", ...)
```

### 3.6 Templates (Jinja2)

**Syntax:**

**Variables:** `{{ variable }}`
```html
<h1>{{ room.name }}</h1>
<p>Price: ${{ room.price }}/night</p>
```

**Conditionals:**
```html
{% if session.get("logged_in") %}
    <a href="/logout">Logout</a>
{% else %}
    <a href="/login">Login</a>
{% endif %}
```

**Loops:**
```html
{% for room in rooms %}
    <div class="card">{{ room.name }}</div>
{% endfor %}
```

**Template inheritance:**
```html
<!-- base.html -->
<html>
<body>
    <nav>...</nav>
    {% block content %}{% endblock %}
</body>
</html>

<!-- rooms.html -->
{% extends "base.html" %}
{% block content %}
    <h1>Rooms</h1>
{% endblock %}
```

**Passing context:**
```python
render_template("rooms.html", rooms=data, q=query, types=room_types)
```
Then in template: `{{ rooms }}`, `{{ q }}`, `{{ types }}`

**Filters:**
```html
{{ room.price | int }}           <!-- Convert to int -->
{{ "hello" | upper }}            <!-- HELLO -->
{{ items | length }}             <!-- Count -->
{{ data | tojson }}              <!-- Convert to JSON -->
```

### 3.7 Flash Messages

**Purpose:** Show temporary feedback to users (success, errors, warnings)

**Setting a flash:**
```python
flash("Booking confirmed!", "success")
flash("Invalid date.", "danger")
```

**Displaying in template:**
```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, msg in messages %}
            <div class="alert alert-{{ category }}">{{ msg }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

**Categories map to Bootstrap classes:**
- `success` → green alert
- `danger` → red alert
- `warning` → yellow alert
- `info` → blue alert

### 3.8 Configuration Patterns

**Our app (simple):**
```python
app.secret_key = "change-this-secret"
```

**Production pattern:**
```python
import os
app.secret_key = os.environ.get("SECRET_KEY") or "dev-key-only"
app.config["DEBUG"] = os.environ.get("DEBUG") == "1"
```

**Config classes (larger apps):**
```python
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

app.config.from_object(ProductionConfig)
```

### 3.9 Common Pitfalls & How We Avoid Them

**1. Session not persisting:**
```python
# WRONG
session["reservations"].append(new_item)

# RIGHT
items = session.get("reservations", [])
items.append(new_item)
session["reservations"] = items
session.modified = True
```

**2. Forgetting to return:**
```python
# WRONG
@app.route("/")
def home():
    render_template("home.html")  # Returns None

# RIGHT
@app.route("/")
def home():
    return render_template("home.html")
```

**3. No CSRF protection (our app doesn't have):**
- Production: Use Flask-WTF for form tokens
- Our app: Demonstration only, accepts any POST

**4. No authentication on protected routes:**
```python
@app.route("/booking")
@login_required  # Our decorator
def booking():
    ...
```

**5. Mixing GET/POST logic:**
```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle form submission
        ...
    # Always return GET response at the end
    return render_template("login.html")
```

---

**[Continue to Part 2: Test Suite Walkthrough → See next response due to length]**
