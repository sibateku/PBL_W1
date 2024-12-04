import sqlite3

# ユーザーデータの位置
userdata_db = "sql/userdata/"

def set_category(account_id: str, category_name: str) -> bool:
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories(name) VALUES(?)", (category_name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_category(account_id: str) -> list:
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        category = cursor.fetchall()
        return category
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def get_category_fromId(account_id: str, category_id: int) -> str:
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        category = cursor.fetchone()
        if category:
            return category[0]
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

def get_category_fromName(account_id: str, category_name: str) -> int:
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categories WHERE title = ?", (category_name,))
        category = cursor.fetchone()
        if category:
            return category[0]
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    # テスト
    """
    account_id = "taro"
    template_name = "test_template"
    print(set_template(account_id, template_name))
    print(get_templates(account_id))
    print(get_template_fromId(account_id, 1))
    """
