import sqlite3

### アカウントデータベースを扱うpythonコード
### これをimportしてサーバープログラムに使用する

# account.db の位置
account_db = "sql/account.db"

# アカウントを作成する関数
def account_create(id: str, pw: str) -> bool:
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
        print(f"Account for ID {id} created successfully.")
        return True  # 登録成功
    except Exception as e:
        print(f"Error: {e}")
        return False  # エラーが発生した場合
    finally:
        conn.close()

# アカウント認証を行う関数
def account_auth(id: str, pw: str) -> bool:
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

# アカウントを削除する関数
def account_delete(id: str) -> bool:
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
        print(f"ID {id} has been deleted.")
        return True  # 削除成功
    except Exception as e:
        print(f"Error: {e}")
        return False  # エラーが発生した場合
    finally:
        conn.close()



if __name__ == "__main__":
    # データベースを作る
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

    account_delete("taro")
    list_accounts()