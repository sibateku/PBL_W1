### 個人のデータベースを扱うpythonコード
import sqlite3

account_db = "sql/account.db"

def list_personal_data(account_id):
    personal_data = f"sql/userdata/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM schedules")
        titles = cursor.fetchall()
        for title in titles:
            print(f"ID: {title[0]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def get_schedule_between(account_id, year, month):
    personal_data = f"sql/userdata/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedules WHERE year = ? AND month = ?", (year, month))
        schedules = cursor.fetchall()
        for schedule in schedules:
            print(schedule)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def add_data(account_id, year, month, day, title, budget, category):
    personal_data = f"sql/userdata/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO schedules(year, month, day, title, budget, spent, category)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """, (year, month, day, title, budget, 0, category))
        conn.commit()
        print(f"Data added successfully.")
    except Exception as e:
        print(f"Error adding data: {e}")
    finally:
        conn.close()

def delete_data(account_id, data_id):
    personal_data = f"sql/userdata/{account_id}.db"
    try:
        conn = sqlite3.connect(personal_data)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedules WHERE id = ?", (data_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Record with ID {data_id} deleted successfully.")
        else:
            print(f"No record found with ID {data_id}.")
    except Exception as e:
        print(f"Error deleting data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    input_account_id = "taro"
    input_account_pw = "tar0pas!"

    from account import account_auth
    if account_auth(input_account_id, input_account_pw):
        add_data(input_account_id, 2024, 11, 26, "作成", 100, 1)
        add_data(input_account_id, 2024, 11, 27, "確認", 200, 1)
        list_personal_data(input_account_id)
