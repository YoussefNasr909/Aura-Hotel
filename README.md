# 🏨 AURA Hotel

A modern Flask-based hotel booking demo application with a premium dark UI design featuring Egyptian-themed rooms. Built for testing and QA automation practice.

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952b3?style=flat-square&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-ffc300?style=flat-square)

---

## ✨ Features

- **Room Browsing** — Search and filter rooms by name, type, and price
- **Enhanced Room Details** — View comprehensive room information including size, bed type, floor, and ratings
- **Room Details Modal** — Interactive modal with full room specifications and amenities
- **Booking System** — Create reservations stored in session
- **User Authentication** — Static demo login (no database)
- **Reservations Management** — View, search, and cancel bookings
- **Dashboard** — Statistics overview with test automation results
- **Modern UI** — Premium dark glassmorphism design with smooth animations

---

## 🏠 Room Collection

The hotel features **6 premium Egyptian-themed rooms**:

| Room | Type | Price | Size | Bed | Rating |
|------|------|-------|------|-----|--------|
| Cairo Comfort Single | Single | $55/night | 220 sq.ft | Twin | ⭐ 4.5 |
| Nile View Double | Double | $85/night | 320 sq.ft | Queen | ⭐ 4.7 |
| Lux Suite | Suite | $160/night | 520 sq.ft | King | ⭐ 4.9 |
| Alexandria Sea Breeze | Double | $95/night | 350 sq.ft | Queen | ⭐ 4.6 |
| Pharaoh's Royal Chamber | Suite | $220/night | 680 sq.ft | King | ⭐ 5.0 |
| Aswan Desert Oasis | Single | $65/night | 250 sq.ft | Twin | ⭐ 4.4 |

### Room Amenities

Each room includes various amenities such as:
- Wi-Fi, AC, Breakfast (standard)
- Balcony, Sea View, Mini Bar
- Jacuzzi, Living Area, Private Terrace
- Butler Service, Spa Access

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/hotel_test.git
cd hotel_test

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will be available at **http://127.0.0.1:5000**

---

## 🔐 Demo Credentials

| Username | Password |
|----------|----------|
| `admin`  | `1234`   |

---

## 📁 Project Structure

```
hotel_test/
├── app.py              # Flask application & routes
├── requirements.txt    # Python dependencies
├── static/
│   └── css/
│       └── styles.css  # Premium glassmorphism design system
├── templates/
│   ├── base.html       # Base layout template
│   ├── home.html       # Homepage with featured rooms
│   ├── rooms.html      # Room listing with search/filter & modals
│   ├── booking.html    # Booking form
│   ├── login.html      # Authentication
│   ├── reservations.html # Reservation management
│   └── dashboard.html  # Admin dashboard
├── tests/              # Pytest test suites
└── test_results/       # Test automation reports
```

---

## 🧪 Test Suite

This project includes a comprehensive test suite with **15 automated tests** using **pytest**.

### Test Categories

| Test File | Tests | Description |
|-----------|-------|-------------|
| `test_auth.py` | 3 | User authentication (login, logout, protected routes) |
| `test_booking_reservations.py` | 6 | Booking creation, validation, cancellation, deletion |
| `test_rooms_search.py` | 3 | Room search, filtering, and display |
| `test_dashboard.py` | 3 | Dashboard stats, test results display |

### Running Tests

```bash
# Run all tests
pytest -v

# Run with HTML report
pytest -v --html=report.html --self-contained-html

# Run specific test file
pytest tests/test_booking_reservations.py -v
```

### Test Features

- **Automatic Test Results Tracking** — Results saved to `test_results/` directory
- **Dashboard Integration** — Test results displayed on the Dashboard page
- **Pass/Fail Trends Chart** — Historical test run visualization
- **Email Notifications** — Automatic email alerts on test failures

---

## ✅ Course Requirements

This project meets **100% of the Software Quality Assurance course requirements**:

| Requirement | Status |
|-------------|--------|
| User Authentication | ✅ Complete |
| CRUD Operations (Create, Read, Update, Delete) | ✅ Complete |
| Search Functionality | ✅ Complete |
| 15 Automated Tests | ✅ All Passing |
| Test Automation Dashboard | ✅ Complete |
| Pass/Fail Trends Chart | ✅ Complete |
| Email Notifications on Failures | ✅ Working |

---

## 🎨 Design System

The UI features a **premium dark glassmorphism theme** with:

### Color Palette

| Token | Color | Usage |
|-------|-------|-------|
| Ink Black | `#000814` | Background |
| Prussian Blue | `#001d3d` | Secondary surfaces |
| Regal Navy | `#003566` | Primary actions |
| School Bus Yellow | `#ffc300` | Accents & highlights |
| Gold | `#ffd60a` | Secondary accents |

### Visual Effects

- **Glassmorphism** — Frosted glass effect on cards and modals
- **Premium Typography** — Modern font stack with optimal readability
- **Dynamic Shadows** — Multi-layered shadows for depth
- **Smooth Gradients** — Elegant color transitions

### Animations

- Smooth 120-250ms transitions on all interactive elements
- Card hover lift effects with enhanced shadows
- Page entrance fade animations
- Modal slide-in effects
- Button press feedback
- Respects `prefers-reduced-motion` for accessibility

### UI Components

- **Room Cards** — Display room info with ratings, amenities preview
- **Room Details Modal** — Full specifications including size, floor, bed type
- **Amenity Badges** — Styled tags for room features
- **Star Ratings** — Visual rating display with half-star support
- **Price Tags** — Highlighted pricing with accent colors

---

## 📝 Pages Overview

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero section + featured rooms |
| Rooms | `/rooms` | Full room listing with search/filter & detail modals |
| Booking | `/booking` | Create new reservation |
| Login | `/login` | User authentication |
| Reservations | `/reservations` | View & manage bookings |
| Dashboard | `/dashboard` | Statistics & test results |

---

## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5.3, Custom CSS with Glassmorphism
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js (Dashboard)
- **Testing**: pytest, pytest-html

---

## 📜 License

This project is for educational and testing purposes.

---

<div align="center">

**Built with ☕ for QA & Testing Practice**

</div>