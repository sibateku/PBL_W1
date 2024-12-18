import sqlite3

# ユーザーデータの位置
userdata_db = "sql/userdata/"

def set_template(account_id: str, template_name: str, template_budget: int) -> bool:
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
        cursor.execute("INSERT INTO templates(title, budget) VALUES(?, ?)", (template_name, template_budget))
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
        for i in range(len(templates)):
            templates[i] = {
                "id": templates[i][0],
                "title": templates[i][1],
                "budget": templates[i][2]
            }
        return templates
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()



def get_template_fromId(account_id: str, template_id: int) -> dict:
    """
    指定されたSQLiteデータベースからテンプレートを取得します。
    Args:
        account_id (str): アカウントID。
        template_id (int): テンプレートID。
    Returns:
        dict: テンプレートの情報
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
        template = cursor.fetchone()
        if template:
            template = {
                "id": template[0],
                "title": template[1],
                "budget": template[2]
            }
            return template
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()



def get_template_fromName(account_id: str, template_name: str) -> dict:
    """
    名前からテンプレートのIDを取得
    """
    try:
        conn = sqlite3.connect(f"{userdata_db}{account_id}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM templates WHERE title = ?", (template_name,))
        template = cursor.fetchone()
        if template:
            template = {
                "id": template[0],
                "title": template[1],
                "budget": template[2]
            }
            return template
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()



if __name__ == "__main__":
    # テスト
    account_id = "taro"
    template_name = "test_template"
    template_budget = 10000
    print(set_template(account_id, template_name, template_budget))
    print(get_templates(account_id))
    print(get_template_fromId(account_id, 1))