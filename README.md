# 🧾 MyWallet

**MyWallet** is a personal expense tracking system that allows users to store, manage, and analyze their invoices.  
The system extracts data from invoice images, stores them in a structured database, and provides summaries and insights about spending habits.

---

## 🚀 Features

- 📸 **Invoice Capture**: Upload an invoice image, automatically processed with OCR + LLM to extract data.
- 🗄 **Data Storage**: Store invoices in PostgreSQL with metadata (user, category, price, description, date, and file path).
- 📂 **File Management**: Save invoice images in organized folders (per user).
- 🔍 **Filtering**: Retrieve invoices for a specific user within a date range.
- 📊 **Summaries**: Generate spending summaries (total invoices, total amount spent, categorized breakdown, and habits).
- 🔒 **Multi-user Ready**: Authentication with email & password, each user has isolated data.
- 📈 **Future Extensions** (planned):
  - Balance tracking (income vs expenses).
  - Reports export (Excel/PDF).
  - Visualizations (charts for categories & trends).
  - Multi-language OCR support.

---

## 🏗 System Architecture

1. **User uploads invoice image** via API.  
2. **OCR Model** extracts text from the image.  
3. **LLM (Large Language Model)** parses text into structured key-value pairs.  
4. Data stored in **PostgreSQL** (Invoices, Categories, Users).  
5. API provides endpoints to:
   - Add invoices
   - Retrieve invoices by date
   - Generate summaries  
6. Invoice image saved locally under `/assets/images/{user_id}/`.

---

## 🗂 Database Schema

### Users
- `id`
- `email`
- `password_hash`
- `name`

### Categories
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

---

## ⚙️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: SQLAlchemy (Async)
- **AI Models**:  
  - OCR (Tesseract / custom model)  
  - LLM (for parsing invoice data into structured format)
- **Tools**: Pydantic, Alembic (for migrations), Postman (for testing)

---

## 📌 Example Workflow

### 1. Upload Invoice
Input: An image of a bill (e.g. WE Internet Bill).  
The system extracts:
```json
{
  "user_id": 1,
  "category_id": 4,
  "invoice_name": "WE internet bill",
  "total_price": 260.5,
  "description": "Payment for home internet bill",
  "file_path": "/assets/images/user_1/invoice_123.jpeg"
}
```

### 2. Get summary
Input:
``` json
{
  "start_date": "2025-09-30",
  "end_date": "2025-10-01"
}

```

Response:
```json
{
  "summary": {
    "date_range": "2025-09-30 to 2025-10-01",
    "total_invoices": 4,
    "total_amount_spent": 1042.0,
    "categories": {
      "Utilities": 1042.0
    },
    "spending_habits": "The user spent a total of $1042.0 on utilities (4 transactions)."
  }
}
```

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

## 📅 Roadmap(Future Work)
* Add income sources & balance tracking
* Export reports (Excel, PDF)
* Charts for visualization
* User dashboard (Frontend with React)
* Cloud storage support for images (S3, GCS)


## Contributing 🤝
Pull requests are welcome! For major changes, please open an issue first to discuss.

