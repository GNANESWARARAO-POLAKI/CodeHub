# 🚀 CodeHub – Multi-Coding Contest Platform

CodeHub is a scalable and robust web-based coding contest platform designed for managing and participating in programming competitions. Built using Django and FastAPI, it supports real-time code submissions, dynamic leaderboards, and admin-controllable contest management.

---

## 📌 Features

### 👥 User Management
- User signup/login system
- Role-based access: Admins & Participants
- Dashboard to view contest status and participation

### 🏆 Contest Management
- Admin can:
  - Create contests
  - Add/edit/remove problems
  - Schedule contest timings
- Participants can:
  - View ongoing/upcoming contests
  - Attempt problems during contest duration

### ⌨️ Real-Time Code Submission
- Code editor with language selector
- Compile and run code on the server
- Instant verdict after submission:
  - ✅ Correct
  - ❌ Wrong Answer
  - ⏳ Time Limit Exceeded

### 📊 Leaderboard & Scoring
- Real-time leaderboard
- Tracks attempts, accuracy, and submission times



---

## 🛠 Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Django, FastAPI                   |
| Frontend    | HTML, CSS, JavaScript             |
| Database    | SQLite/PostgreSQL                 |
| Load Testing| Locust                            |
| Version Control | Git, GitHub                   |

---

## 🧾 Setup Instructions

### 🔁 Step 1: Clone the Repository

```bash
git clone https://github.com/gnaneswararao-polaki/codehub.git
cd codehub

```
---

### 🧱 Step 2: Create a Virtual Environment

```bash
python -m venv env

```
---

### 📦 Step 3: Install Required Packages

Install all required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```
---
### 🗃️ Step 4: Apply Migrations

First, create migration files:

```bash
python manage.py makemigrations
```

Then, apply the migrations to your database:
```bash 
python manage.py migrate
```
---
### ▶️ Step 6: Start the Server

Run the Django development server:

```bash
python manage.py runserver
```
