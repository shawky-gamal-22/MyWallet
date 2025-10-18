# 🧾 MyWallet

**MyWallet** is a personal expense tracking system that allows users to store, manage, and analyze their invoices.  
The system extracts data from invoice images, stores them in a structured database, and provides summaries and insights about spending habits.

---

## 🚀 Features

✅ 📸 **Incomes & Expenses Management**
- Add, update, and delete income and expense records.
- Categorize transactions by type or frequency.

✅ **Recurring Transactions**
- Automatically process recurring **incomes** and **invoices** using Celery Beat tasks.
- Define recurrence rules (daily, weekly, monthly, etc.).

✅ **Data Storage**: Store invoices in PostgreSQL with metadata (user, category, price, description, date, and file path).
✅ **File Management**: Save invoice images in organized folders (per user).

✅ **Filtering**: Retrieve invoices for a specific user within a date range.

✅ **Summaries**: Generate spending summaries (total invoices, total amount spent, categorized breakdown, and habits).

 🔒 **Multi-user Ready**: Authentication with email & password, each user has isolated data.

 📈 **Future Extensions** (planned):
  - Reports export (Excel/PDF).
  - Visualizations (charts for categories & trends).
  - Multi-language OCR support.

---


## 🗂 Database Schema

### Users
- `id`
- `email`
- `password_hash`
- `name`

### InvoiceCategories
- `id`
- `name`
- `description`

### Invoices
- `id`
- `user_id`
- `category_id`
- `total_price`
- `description`
- `created_at`
- `img_path`
- `is_recurring`
- `recurrence_interval`
- `next_due_date`
- `last_run_date`

### Incomies
- `id`
- `user_id`
- `category_id`
- `amount`
- `source_name`
- `created_at`
- `is_recurring`
- `recurrence_interval`
- `next_due_date`
- `last_run_date`

### IncomiesCategories
- `id`
- `name`
- `description`

### UsertBalance
- `user_id`
- `current_balance`


---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy Async + Alembic |
| **Task Queue** | Celery |
| **Message Broker** | Redis |
| **Containerization** | Docker & Docker Compose |

---


## ✨ Current Progress

- ✅ **Invoice Upload & OCR Extraction**  
  Successfully implemented the invoice upload feature using **Mistral OCR**, which extracts text from images and passes it to an **LLM** that structures the data (amount, date, category, etc.).  
  Extracted data is stored directly in a **PostgreSQL** database using **SQLAlchemy (async)**.

- ✅ **Summarization by Date Range**  
  Added a route to generate summaries for a given period (`start_date`, `end_date`), displaying:  
  - Total amount spent  
  - Spending categories  
  - Purchase locations  
  This enables users to easily track their expenses across any time range.
 
- ✅ **Income & Balance Tracking**  
  - Add support for multiple **income sources** (salary, freelance, etc.).  
  - Implement **current balance calculation** = total income − total expenses.  
  - Keep a **historical balance record** for financial trend tracking. 


## 🚀 Roadmap(Future Work)


### 🧾 Advanced Invoice Management
- Support multiple **invoice types** (shopping, utilities, groceries, etc.).  
- Enable **batch invoice uploads** for faster processing.  
- Improve **OCR accuracy** using advanced or fine-tuned models.  
- Add **auto-categorization** of invoices using LLM-based content understanding.  

---

### 📊 Analytics & Insights
- Build an **analytics dashboard** with:  
  - Total spending by category.  
  - Month-over-month expense comparisons.  
  - Most frequent spending locations.  
- Implement **spending pattern detection** and **budget alerts**.  
- Provide **smart saving recommendations** based on user behavior.  

---

### 🧠 Multi-Agent Financial Assistant
- Introduce a **multi-agent system** to plan and manage financial goals.  
  - Example: A “Travel Planner” agent that calculates required savings for a trip.  
  - Another agent monitors weekly spending and suggests optimizations.  
- Allow agents to **collaborate** to keep users on track financially.  

---

### 🪙 Financial Goals Management
- Add a feature for users to **set and track financial goals** (e.g., “Save EGP 5000 in 3 months”).  
- Visualize progress and integrate with spending analysis.  

---

### 🧑‍💻 User Interface / Dashboard
- Develop a **modern web or mobile dashboard** (React / Flutter).  
- Include **interactive charts, filters, and invoice upload tools**.  
- Provide a **clean and intuitive UX** for managing finances.  

---

### ☁️ Cloud & Scalability
- Store images on **cloud storage** (AWS S3 / Google Cloud).  
- Add **JWT authentication** for secure user access.  
- Support **multi-user environments** with isolated data.  
- Deploy using **Docker** and cloud platforms (Render, Railway, AWS).  

---

### 📤 Reports & Exports
- Allow users to **export summaries** as **PDF or Excel reports**.  
- Enable **automated weekly or monthly email reports**.  

---



## Installation & Setup
1. Clone repository:

```bash
git clone https://github.com/your-username/mywallet.git
cd mywallet
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Handle alembic for Database Migration

5. Run the app:

```bash
uvicorn main:app --reload 
```



## Contributing 🤝
Pull requests are welcome! For major changes, please open an issue first to discuss.

