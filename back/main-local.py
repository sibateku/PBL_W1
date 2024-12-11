# mainをローカルで実行
from main import *

# ローカルファイルで実行するためのアクセス制限撤廃用
from flask_cors import CORS
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)