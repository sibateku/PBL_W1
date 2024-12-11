import sqlite3
import os

### アカウントデータベースを扱うpythonコード
### これをimportしてサーバープログラムに使用する

# account.db の位置
account_db = "sql/account.db"

# アカウントに紐づいたデータベースの位置
userdata_db = "sql/userdata/"



def account_create(id: str, pw: str) -> bool:
    """
    指定されたIDとパスワードで新しいアカウントを作成します。
    この関数は以下の手順を実行します:
    1. アカウントデータベース(sql/account.db)に接続します。
    2. 提供されたIDがデータベースに既に存在するか確認します。
    3. IDが存在しない場合、新しいアカウントをデータベースに挿入します。
    4. ユーザー専用データベース(sql/userdata/[アカウント名].db)を作成します。
    5. ユーザー専用データベースに必要なテーブル（categories, schedules, templates）を作成します。
    Args:
        id (str): 新しいアカウントのID。
        pw (str): 新しいアカウントのパスワード。
    Returns:
        bool: アカウントが正常に作成された場合はTrue、そうでない場合はFalse。
    """

    try:
        conn = sqlite3.connect(account_db)
        cursor = conn.cursor()
        # IDがすでに存在するか確認
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (id,))
        if cursor.fetchone():
            print(f"ID {id} already exists.")
            return False  # IDが既に存在する場合
        # 新しいアカウントを登録
        cursor.execute("INSERT INTO accounts (id, pw) VALUES (?, ?)", (id, pw))
        conn.commit()

        # アカウントに紐づいたデータベース(id.db)を作成
        with sqlite3.connect(f"{userdata_db}{id}.db") as user_conn:
            user_cursor = user_conn.cursor()

            # カテゴリーテーブルを作る
            # categories
            #   - id (AUTO INCREMENT)
            #   - name (NOT NULL)
            user_cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )
            """)

            # スケジュールテーブルを作る
            # schedules
            #   - id (AUTO INCREMENT)
            #   - title (NOT NULL): 予定のタイトル
            #   - year (NOT NULL): 年
            #   - month (NOT NULL): 月
            #   - day (NOT NULL): 日
            #   - budget: 予算
            #   - spent: 実際に使った金額
            #   - category: カテゴリーid
            #   - details: 詳細
            user_cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedules (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            title    TEXT NOT NULL,
            year     INTEGER NOT NULL,
            month    INTEGER NOT NULL,
            day      INTEGER NOT NULL,
            budget   INTEGER,
            spent    INTEGER,
            category INTEGER,
            details  TEXT
            )
            """)

            # テンプレートテーブルを作る
            # templates
            #   - id (AUTO INCREMENT)
            #   - title (NOT NULL): テンプレートのタイトル
            #   - budget (NOT NULL): 予算
            user_cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            title  TEXT NOT NULL,
            budget INTEGER NOT NULL
            )
            """)
            user_conn.commit()

        print(f"Account for ID {id} created successfully.")
        return True  # 登録成功
    except Exception as e:
        print(f"Error: {e}")
        return False  # エラーが発生した場合
    finally:
        conn.close()



def account_auth(id: str, pw: str) -> bool:
    """
    指定されたIDとパスワードを使用してアカウント認証を行います。
    Args:
        id (str): 認証するアカウントのID。
        pw (str): 認証するアカウントのパスワード。
    Returns:
        bool: 認証が成功した場合はTrue、失敗した場合はFalseを返します。
    """

    try:
        conn = sqlite3.connect(account_db)
        cursor = conn.cursor()
        # IDとパスワードが一致するレコードを検索
        cursor.execute("SELECT * FROM accounts WHERE id = ? AND pw = ?", (id, pw))
        if cursor.fetchone():
            print(f"ID {id} authenticated successfully.")
            return True  # 認証成功
        return False  # 認証失敗
    except Exception as e:
        print(f"Error: {e}")
        return False  # エラーが発生した場合
    finally:
        conn.close()



def account_isExists(id: str) -> bool:
    """
    指定されたIDがアカウントデータベースに存在するかを確認します。
    Args:
        id (str): 確認するアカウントのID。
    Returns:
        bool: IDが存在する場合はTrue、存在しない場合はFalseを返します。
                エラーが発生した場合もFalseを返します。
    Raises:
        Exception: データベース接続やクエリ実行中に発生したエラー。
    """

    try:
        conn = sqlite3.connect(account_db)
        cursor = conn.cursor()
        # IDが存在するか確認
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (id,))
        if cursor.fetchone():
            print(f"ID {id} exists.")
            return True  # IDが存在する場合
        print(f"ID {id} does not exist.")
        return False  # IDが存在しない場合
    except Exception as e:
        print(f"Error: {e}")
        return False  # エラーが発生した場合
    finally:
        conn.close()



def account_delete(id: str) -> bool:
    """
    指定されたIDのアカウントを削除します。
    この関数は、指定されたIDのアカウントをデータベースから削除し、
    そのアカウントに関連付けられたユーザーデータベースも削除します。
    Args:
        id (str): 削除するアカウントのID。
    Returns:
        bool: アカウントの削除に成功した場合はTrue、失敗した場合はFalseを返します。
    """
    
    try:
        conn = sqlite3.connect(account_db)
        cursor = conn.cursor()
        # IDが存在するか確認
        cursor.execute("SELECT * FROM accounts WHERE id = ?", (id,))
        if not cursor.fetchone():
            print(f"ID {id} does not exist.")
            return False  # IDが存在しない場合
        # アカウントを削除
        cursor.execute("DELETE FROM accounts WHERE id = ?", (id,))
        conn.commit()

        # アカウントに紐づいたデータベースを削除
        user_db_path = f"{userdata_db}{id}.db"
        if os.path.exists(user_db_path):
            os.remove(user_db_path)
            print(f"Database for ID {id} has been deleted.")

        print(f"ID {id} has been deleted.")
        return True  # 削除成功
    except Exception as e:
        print(f"Error: {e}")
        return False  # エラーが発生した場合
    finally:
        conn.close()



if __name__ == "__main__":
    # なければデータベースを作る
    def init_db():
        try:
            conn = sqlite3.connect(account_db)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    pw TEXT NOT NULL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    # ユーザーとパスワード一覧を表示する関数
    def list_accounts():
        try:
            conn = sqlite3.connect(account_db)
            cursor = conn.cursor()
            cursor.execute("SELECT id, pw FROM accounts")
            accounts = cursor.fetchall()
            for account in accounts:
                print(f"ID: {account[0]}, PW: {account[1]}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

    init_db()
    account_delete("sample")
    account_delete("taro")
    list_accounts()

    account_create("sample", "sample00")
    account_create("taro", "tar0pas!")
    list_accounts()