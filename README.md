# 🏨 AURA Hotel

A modern Flask-based hotel booking demo application with a premium dark UI design. Built for testing and QA automation practice.

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952b3?style=flat-square&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-ffc300?style=flat-square)

---

## ✨ Features

- **Room Browsing** — Search and filter rooms by name, type, and price
- **Booking System** — Create reservations stored in session
- **User Authentication** — Static demo login (no database)
- **Reservations Management** — View, search, and cancel bookings
- **Dashboard** — Statistics overview with test automation results
- **Modern UI** — Premium dark glassmorphism design with smooth animations

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
│       └── styles.css  # Custom design system
├── templates/
│   ├── base.html       # Base layout template
│   ├── home.html       # Homepage with featured rooms
│   ├── rooms.html      # Room listing & search
│   ├── booking.html    # Booking form
│   ├── login.html      # Authentication
│   ├── reservations.html # Reservation management
│   └── dashboard.html  # Admin dashboard
├── tests/              # Pytest test suites
└── test_results/       # Test automation reports
```

---

## 🧪 Running Tests

This project uses **pytest** for automated testing.

```bash
# Run all tests
pytest -v

# Run with HTML report
pytest -v --html=report.html --self-contained-html

# Run specific test file
pytest tests/test_booking_reservations.py -v
```

Test results are displayed on the Dashboard page after running.

---

## 🎨 Design System

The UI features a premium dark theme with:

| Token | Color | Usage |
|-------|-------|-------|
| Ink Black | `#000814` | Background |
| Prussian Blue | `#001d3d` | Secondary surfaces |
| Regal Navy | `#003566` | Primary actions |
| School Bus Yellow | `#ffc300` | Accents & highlights |
| Gold | `#ffd60a` | Secondary accents |

### Animations

- Smooth 120-250ms transitions on all interactive elements
- Card hover lift effects with shadows
- Page entrance fade animations
- Respects `prefers-reduced-motion` for accessibility

---

## 📝 Pages Overview

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero section + featured rooms |
| Rooms | `/rooms` | Full room listing with search/filter |
| Booking | `/booking` | Create new reservation |
| Login | `/login` | User authentication |
| Reservations | `/reservations` | View & manage bookings |
| Dashboard | `/dashboard` | Statistics & test results |

---

## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5.3, Custom CSS
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