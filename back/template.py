import sqlite3

# ユーザーデータの位置
userdata_db = "sql/userdata/"

def set_template(account_id: str, template_name: str) -> bool:
    """
    指定されたSQLiteデータベースにテンプレートを追加します。
    Args:
        account_id (str): アカウントID。
        template_name (str): テンプレート名。
    Returns:
        bool: テンプレートの追加に成功した場合はTrue、失敗した場合はFalseを返します。
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO templates(title) VALUES(?)", (template_name,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()



def delete_template(account_id: str, template_id: int) -> bool:
    """
    指定されたSQLiteデータベースからテンプレートを削除します。
    Args:
        account_id (str): アカウントID。
        template_id (int): テンプレートID。
    Returns:
        bool: テンプレートの削除に成功した場合はTrue、失敗した場合はFalseを返します。
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM templates WHERE id = ?", (template_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()



def get_templates(account_id: str) -> list:
    """
    指定されたSQLiteデータベースからユーザーのテンプレートを取得します。
    Args:
        account_id (str): アカウントID。
    Returns:
        list: テンプレートのリスト
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templates")
        templates = cursor.fetchall()
        return templates
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()



def get_template_fromId(account_id: str, template_id: int) -> str:
    """
    指定されたSQLiteデータベースからテンプレートを取得します。
    Args:
        account_id (str): アカウントID。
        template_id (int): テンプレートID。
    Returns:
        str: テンプレートの名前
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM templates WHERE id = ?", (template_id,))
        template = cursor.fetchone()
        if template:
            return template[0]
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()



def get_template_fromName(account_id: str, template_name: str) -> int:
    """
    名前からテンプレートのIDを取得
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM templates WHERE title = ?", (template_name,))
        template = cursor.fetchone()
        if template:
            return template[0]
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()



if __name__ == "__main__":
    # テスト
    account_id = "taro"
    template_name = "test_template"
    print(set_template(account_id, template_name))
    print(get_templates(account_id))
    print(get_template_fromId(account_id, 1))