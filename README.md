# Python Code Analyzer - FastAPI Project

## 📌 Overview

This project analyzes uploaded Python code files (in `.zip` format) and returns insights about code quality.  
The analysis includes:
- גילוי פונקציות ארוכות
- משתנים לא בשימוש
- פונקציות ללא Docstring
- קבצים ארוכים
- גרפים סטטיסטיים של הבעיות שנמצאו

המערכת נבנתה באמצעות FastAPI ומאפשרת להעלות קבצים, לבצע אנליזה ולחזות תוצאות גם בטקסט וגם בגרף.

---

## 🚀 Installation and Execution

1. **התקנת תלויות:**

```bash
pip install fastapi uvicorn matplotlib
```

2. **הרץ את השרת:**

```bash
uvicorn main:app --reload
```

3. **גישה ל־API:**

לאחר הרצה, עבור לדפדפן:  
```
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```
.
├── main.py                  # נקודת הכניסה הראשית לאפליקציה
├── routers/
│   ├── alerts.py           # ניתוח בעיות בקוד (alerts)
│   └── analyze.py          # יצירת גרפים מהנתונים
├── services/
│   ├── alerts_handler.py   # עיבוד מידע ל־alerts
│   ├── analyzer.py         # בניית נתונים ל־analyze
│   ├── common_analysis.py  # פונקציות ניתוח כלליות
│   └── UnusedVariableTracker.py  # מחלקה לזיהוי משתנים לא בשימוש
└── README.md               # קובץ תיעוד
```

---

## 📮 API Endpoints

### `POST /alerts`

🔍 **תיאור:**  
מקבל קובץ ZIP שמכיל קבצי Python ומחזיר ניתוח של בעיות נפוצות בקוד.

📥 **קלט:**  
- קובץ `zip` שמכיל קבצי `.py`.

📤 **פלט (JSON):**
```json
{
  "filename.py": {
    "Function Length": {"func_name": 25},
    "File Length": {"line": 250},
    "Unused Variables": {"func_name": [{"in": "func_name"}]},
    "Missing Docstrings": {"func_name": true}
  },
  ...
}
```

---

### `POST /analyze`

📊 **תיאור:**  
מקבל קובץ ZIP שמכיל קבצי Python ומחזיר תמונת גרף הכוללת:
- אורך פונקציות
- כמות בעיות מכל סוג
- סך בעיות בכל קובץ

📤 **פלט:**  
- קובץ תמונה (PNG)

📌 **שימוש:**  
ניתן לראות את התוצאה ישירות בדפדפן או לשמור את התמונה.
