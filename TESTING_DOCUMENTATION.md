# 🧪 AURA Hotel - Testing Documentation

## 1. Testing Strategy

### Scope & Goals
The primary goal of testing the AURA Hotel application is to ensure the reliability of the booking flow and the accuracy of the room management system. Given the application's nature (stateless, session-based), the strategy emphasizes **End-to-End (E2E) and Integration Testing** over granular unit testing.

### Test Pyramid Justification
For this project, the "Test Pyramid" is slightly inverted (hourglass shape):
- **E2E/Integration Tests (High Volume)**: Since most logic relies on user interactions (forms, sessions, redirects) and UI rendering, Selenium tests provide the highest value.
- **Unit Tests (Low Volume)**: Used only for utility functions (e.g., date parsing), as there is little complex internal business logic isolated from the request context.

---

## 2. Tools & Frameworks

- **Runner**: `pytest` (Standard Python testing framework)
- **Browser Automation**: `Selenium WebDriver` (Chrome)
- **Driver Management**: `webdriver-manager` (Automatic binary handling)
- **Reporting**: `pytest-html` (Visual HTML reports)
- **Notification**: custom SMTP script (Email alerts)

---

## 3. How to Run Tests

### Local Execution

```bash
# 1. Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate

# 2. Run all tests with verbose output
pytest -v

# 3. Run with HTML report generation
pytest -v --html=report.html --self-contained-html

# 4. Run normally (Headless) or visible (Headful)
# Default is Headless. To see the browser:
# Windows (PowerShell)
$env:HEADLESS="0"; pytest
# Linux/Mac
HEADLESS=0 pytest
```

### Coverage
While strictly not measured by a tool in the current setup, the suite covers:
- 100% of defined Routes
- 100% of Form Actions (Login, Booking, Cancel, Delete)

---

## 4. Test Structure

```
tests/
├── conftest.py                   # Setup/Teardown, Browser Fixture, Email Hooks
├── test_auth.py                  # Login/Logout scenarios
├── test_booking_reservations.py  # Core business logic (Create/Cancel/Delete)
├── test_rooms_search.py          # Search and Filter verification
└── test_dashboard.py             # Admin metrics verification
```

**Naming Convention**: `test_<feature>.py` containing functions `test_<scenario>`.

---

## 5. Critical Test Scenarios (Manual & Automated)

### Test Data
- **Valid User**: `admin` / `1234`
- **Valid Room IDs**: 1-6
- **Valid Dates**: Future dates, `check_out > check_in`

### Test Cases Table

| ID | Feature | Preconditions | Steps | Expected Result | Priority | Type |
|----|---------|---------------|-------|-----------------|----------|------|
| **Auth** |
| TC01 | Login | Logged out | 1. Go to /login<br>2. Enter `admin`/`1234`<br>3. Click Login | Redirect to Home; "Login successful" flash msg | P0 | E2E |
| TC02 | Invalid Login | Logged out | 1. Go to /login<br>2. Enter `admin`/`wrong`<br>3. Click Login | Stay on /login; "Wrong username" flash msg | P1 | E2E |
| TC03 | Logout | Logged in | 1. Click Logout in nav | Redirect to Home; Session cleared | P1 | E2E |
| **Search** |
| TC04 | Search by Name | None | 1. Go to /rooms<br>2. Enter "Cairo" in search<br>3. Submit | List shows only "Cairo" room | P1 | E2E |
| TC05 | Filter by Type | None | 1. Go to /rooms<br>2. Select "Suite"<br>3. Submit | List shows only Suite types | P2 | E2E |
| TC06 | Max Price | None | 1. Go to /rooms<br>2. Enter "100" in max price<br>3. Submit | List shows rooms <= $100 | P2 | E2E |
| TC07 | Empty Search | None | 1. Go to /rooms<br>2. Search "InvalidRoom"<br>3. Submit | Show "No rooms found" message | P2 | E2E |
| **Booking** |
| TC08 | Create Booking | Logged in | 1. Go to Room 1 details<br>2. Click Book<br>3. Fill dates<br>4. Submit | Redirect to /reservations; "Reservation created" msg | P0 | E2E |
| TC09 | Guest Validation | Logged in | 1. Booking Form<br>2. Enter guests > Capacity (e.g., 5) | Error "Guests must be between..." | P2 | E2E |
| TC10 | Date Validation | Logged in | 1. Booking Form<br>2. Set Check-out < Check-in | Error "Check-out must be after check-in" | P2 | E2E |
| TC11 | Booking Auth Guard | Logged out | 1. Try to access /booking | Redirect to /login | P1 | Integration |
| **Reservations** |
| TC12 | View Reservations | Has booking | 1. Go to /reservations | Verify newly created booking is listed | P0 | E2E |
| TC13 | Cancel Reservation | Has booking | 1. Go to /reservations<br>2. Click "Cancel" on a booking | Status changes to "Cancelled"; Button changes to "Delete" | P1 | E2E |
| TC14 | Delete Reservation | Has cancelled | 1. Click "Delete" on cancelled booking | Booking removed from list completely | P1 | E2E |
| TC15 | Delete Active | Has active | 1. Try to force delete active booking (API/URL) | Error "Only cancelled reservations can be deleted" | P2 | Integration |
| **Dashboard** |
| TC16 | Stats Accuracy | Has 1 booking | 1. Go to /dashboard | "Total Reservations" count = 1 | P2 | E2E |
| TC17 | Test History | Tests ran | 1. Go to /dashboard | "Latest Test Run" shows Pass/Fail status | P2 | E2E |
| **UI/UX** |
| TC18 | Room Modal | None | 1. Click "Details" on room card | Modal opens; Size/Rating visible | P2 | UI |
| TC19 | Responsive Nav | Mobile View | 1. Resize < 768px<br>2. Click hamburger menu | Menu expands/collapses | P3 | UI |
| TC20 | 404 Page | None | 1. Visit /non-existent-page | Show 404 error page | P3 | Integration |

---

## 6. CI Recommendations

For Continuous Integration (e.g., GitHub Actions), the following pipeline is recommended:

1. **Install Dependencies**:
   ```yaml
   - run: pip install -r requirements.txt && pip install pytest selenium webdriver-manager
   ```
2. **Setup Chrome**:
   Use a standard action like `browser-actions/setup-chrome` or rely on `webdriver-manager` in headless mode.
3. **Run Tests with Headless Mode**:
   ```yaml
   - run: pytest -v
     env:
       HEADLESS: "1"
   ```
4. **Archive Artifacts**:
   Store the `test_results/` and `report.html` as build artifacts.

---

## 7. Bug Reporting Template

When reporting bugs found during testing, use this format:

**Title**: [Component] Short description of issue
**Environment**: Windows 10 / Chrome 120 / Localhost
**Steps to Reproduce**:
1. Go to X
2. Click Y
3. Enter Z
**Expected Result**: System should...
**Actual Result**: System instead did...
**Screenshots**: (Attach if available)
**Logs**:
```
Paste server logs or browser console errors here
```

---

## 8. Open Questions & Assumptions

### Open Questions
- **Production Persistence**: The current system uses in-memory session. Is there a plan to migrate to SQLite/PostgreSQL? Testing strategy would need to change (DB fixtures/transactions).
- **Concurrency**: How should the system behave if two users book the same room for the same dates? Currently, there is no availability check logic implemented.

### Assumptions
- Test environment is always `localhost:5000`.
- Application is single-instance (no session synchronization needed for Redis/Memcached).
- Email notifications rely on a valid Gmail App Password provided in `.env`.
