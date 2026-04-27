## 💻 Running the Project in Visual Studio Code

Follow these steps to run the project using **Visual Studio Code**:

### 🔹 Step 1: Open Project

* Open **VS Code**
* Click **File → Open Folder**
* Select your project folder:

  ```
  client query management
  ```

---

### 🔹 Step 2: Open Terminal

* Go to **Terminal → New Terminal**
* Or press:

  ```
  Ctrl + `
  ```

---

### 🔹 Step 3: Activate Virtual Environment

```bash
.venv\Scripts\activate
```

---

### 🔹 Step 4: Install Dependencies

```bash
pip install streamlit pandas mysql-connector-python
```

---

### 🔹 Step 5: Setup MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE client_db;
```

---

### 🔹 Step 6: Run the Application

```bash
streamlit run app.py
```

---

### 🌐 Output

After running, open your browser:

```
http://localhost:8501
```

---

### ⚠️ Common Issues

| Issue                    | Solution                    |
| ------------------------ | --------------------------- |
| streamlit not recognized | Run `pip install streamlit` |
| MySQL connection error   | Check server is running     |
| Module not found         | Install required packages   |

---

### ✅ Requirements

* Python 3.x
* MySQL Server
* Visual Studio Code
* Internet connection (for package installation)
