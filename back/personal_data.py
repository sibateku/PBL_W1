### 個人のデータベースを扱うpythonコード
import sqlite3

account_db = "sql/account.db"

def auth_user(id, pw):
    try:
        conn = sqlite3.connect(account_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE id = ? AND pw = ?", (id, pw))
        if cursor.fetchone():
            print(f"ID {id} authenticated successfully.")
            return True # 認証成功
        else: return False # 認証失敗
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def create_personal_db(account_id):
    personal_data = f"sql/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personal_data (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                year     INTEGER,
                month    INTEGER,
                day      INTEGER,
                title    TEXT,
                budget   INTEGER,
                spent    INTEGER,
                category TEXT,
            )
        """)
        conn.commit()
        print(f"Database '{personal_data}' created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()

def list_personal_data(account_id):
    personal_data = f"sql/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM personal_data")
        id_all = cursor.fetchall()
        for id in id_all:
            print(f"ID: {id[0]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def add_data(account_id, year, month, day, title, budget, category):
    personal_data = f"sql/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO personal_data(year, month, day, title, budget, spent, category)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """, (year, month, day, title, budget, 0, category))
        conn.commit()
        print(f"Data added successfully.")
    except Exception as e:
        print(f"Error adding data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    input_account_id = "taro"
    input_account_pw = "tar0pas!"

    if auth_user(input_account_id, input_account_pw):
        create_personal_db(input_account_id)
        add_data(input_account_id, 2024, 11, 26, "作成", 100, "001")
        add_data(input_account_id, 2024, 11, 27, "確認", 200, "001")
        list_personal_data(input_account_id)
