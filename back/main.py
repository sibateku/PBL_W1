# coding: utf-8

# flask HTTP requests (example)

# アカウント作成 (アカウントid, password指定)
# http://127.0.0.1:5000/account?req=create&id=jiro&password=jir0pas!
# アカウント削除 (アカウントid指定)
# http://127.0.0.1:5000/account?req=delete&id=jiro
# アカウント認証 (アカウントid, password指定)
# http://127.0.0.1:5000/account?req=auth&id=jiro&password=jir0pas!

# スケジュール取得 (アカウントid, year, month指定)
# http://127.0.0.1:5000/schedule?req=get&id=jiro&year=2024&month=11
# スケジュール追加 (アカウントid, year, month, day, title, *budget, *spent, *category指定)
#   budget, spent, category の指定がなければそれぞれ 0, 0, 0 が入る
#   (なお，category の 0 はその他を表す)
# http://127.0.0.1:5000/schedule?req=set&id=jiro&year=2024&month=11&day=26&title=ご飯
# スケジュール削除 (アカウントid, スケジュールid指定)
# http://127.0.0.1:5000/schedule?req=delete&id=jiro&data_id=1

# テンプレートすべて取得 (アカウントid指定)
# http://127.0.0.1:5000/template?req=get&id=jiro
# テンプレート追加 (アカウントid, title, budget指定)
# http://127.0.0.1:5000/template?req=set&id=jiro&title=ご飯&budget=1000

# カテゴリ取得 (アカウントid, カテゴリid指定)
# http://127.0.0.1:5000/category?req=get&id=jiro&category_id=1
# カテゴリすべて取得 (アカウントid指定)
# http://127.0.0.1:5000/category?req=getall&id=jiro
# カテゴリ追加 (アカウントid, title指定)
# http://127.0.0.1:5000/category?req=set&id=jiro&title=食費

from flask import Flask
import json

import account, template, schedule, category
from flask import request

app = Flask(__name__)

# ローカルファイルで実行するためのアクセス制限撤廃用
LOCALTEST = False
if LOCALTEST:
    from flask_cors import CORS
    CORS(app)

@app.route('/')
def hello_world():
    print("hello_world")
    return 'Test!'

def makeJson(data) -> str:
    """
    様々な型のデータをjsonに変換して返す
    引数:
        data: 変換するデータ
            [dict]: json形式に変換
            [list]: json形式に変換
            [str]: {"res": data} の形式に変換
            [bool]: {"res": true/false} の形式に変換
    戻り値:
        str: json形式の文字列
    """
    if type(data) == dict:
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif type(data) == list:
        if len(list) == 0:
            return makeJson('makeJson: Empty list')
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif type(data) == str:
        data = {"res": data}
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif type(data) == bool:
        data = {"res": data}
        return json.dumps(data, indent=2, ensure_ascii=False)
    return makeJson('makeJson: Invalid data type')



# テンプレートのリクエストを処理
@app.route('/account', methods=['GET'])
def account_request():
    """
    'req'パラメータに基づいてアカウント関連のリクエストを処理
    クエリパラメータ:
        req (str): リクエストの種類。'create', 'delete', 'auth'のいずれか
        id (str): ユーザーID
        password (str): ユーザーのパスワード（'create'および'auth'リクエストに必要）
    戻り値:
        str: アカウント操作の結果、またはリクエストタイプが認識されない場合は'Invalid request'
    """
    print("account_request")

    req = request.args.get('req')
    user_id = request.args.get('id')
    password = request.args.get('password')

    print(f"req: {req}")
    print(f"user_id: {user_id}")
    print(f"password: {password}")

    if user_id is None or user_id == '':
        return makeJson('id: Invalid user_id: empty')

    if req is None or req == '':
        return makeJson('req: Invalid request: empty')
    elif req == 'create':
        if password is None or password == '':
            return makeJson('password: Invalid password: empty')
        return makeJson(account.account_create(user_id, password))
    elif req == 'delete':
        if not account.account_isExists(user_id):
            return makeJson('id: Account not found')
        return makeJson(account.account_delete(user_id))
    elif req == 'auth':
        if not account.account_isExists(user_id):
            return makeJson('id: Account not found')
        if password is None or password == '':
            return makeJson('password: Invalid password: empty')
        return makeJson(account.account_auth(user_id, password))
    else:
        return makeJson('req: Invalid request')



# スケジュールのリクエストを処理
@app.route('/schedule', methods=['GET'])
def schedule_request():
    """
    スケジュールリクエストを処理する関数。
    リクエストの種類に応じて、スケジュールの取得または設定を行います。
    リクエストパラメータ:
        req (str): リクエストの種類 ('get' または 'set')。
        id (str): ユーザーID。

        year (str): 年 (オプション、'get' リクエストの場合必須)。
        month (str): 月 (オプション、'get' リクエストの場合必須)。

        day (str): 日 (オプション、'set' リクエストの場合必須)。
        title (str): タイトル (オプション、'set' リクエストの場合必須)。
        budget (str): 予算 (オプション)。
        spent (str): 支出 (オプション)。
        category (str): カテゴリ (オプション)。
        details (str): 詳細 (オプション)。
    戻り値:
        dict: スケジュール情報または設定結果。
    """
    print("schedule_request")

    req = request.args.get('req')
    user_id = request.args.get('id')

    print(f"req: {req}")
    print(f"user_id: {user_id}")

    if user_id is None or user_id == '':
        return makeJson('id: Invalid user_id: empty')

    if not account.account_isExists(user_id):
        return makeJson('id: Account not found')

    if req is None or req == '':
        return makeJson('req: Invalid request: empty')

    elif req == 'getall':
        return makeJson("getall is not implemented yet")

    elif req == 'getday':
        year = str(request.args.get('year'))
        month = str(request.args.get('month'))
        day = str(request.args.get('day'))

        if year == "None" or year == '':
            return makeJson('year: Invalid year: empty')
        if not year.isdecimal():
            return makeJson('year: Invalid year: not decimal')
        if not (1970 <= int(year) <= 3000):
            return makeJson('year: Invalid year: out of range (1970-3000)')

        if month == "None" or month == '':
            return makeJson('month: Invalid month: empty')
        if not month.isdecimal():
            return makeJson('month: Invalid month: not decimal')
        if not (0 <= int(month) <= 12):
            return makeJson('month: Invalid month: out of range (0-12)')
        
        if day == "None" or day == '':
            return makeJson('day: Invalid day: empty')
        if not day.isdecimal():
            return makeJson('day: Invalid day: not decimal')
        if not (1 <= int(day) <= 31):
            return makeJson('day: Invalid day: out of range (1-31)')
        
        return makeJson(schedule.get_schedule_fromDay(user_id, year, month, day))

    elif req == 'get':
        year = str(request.args.get('year'))
        month = str(request.args.get('month'))

        if year == "None" or year == '':
            return makeJson('year: Invalid year: empty')
        if not year.isdecimal():
            return makeJson('year: Invalid year: not decimal')
        if not (1970 <= int(year) <= 3000):
            return makeJson('year: Invalid year: out of range (1970-3000)')

        if month == "None" or month == '':
            return makeJson('month: Invalid month: empty')
        if not month.isdecimal():
            return makeJson('month: Invalid month: not decimal')
        if not (0 <= int(month) <= 12):
            return makeJson('month: Invalid month: out of range (0-12)')

        return makeJson(schedule.get_schedule_between(user_id, year, month))

    elif req == 'delete':
        data_id = str(request.args.get('data_id'))
        if data_id == "None" or data_id == '':
            return makeJson('data_id: Invalid data_id: empty')
        if not data_id.isdecimal():
            return makeJson('data_id: Invalid data_id: not decimal')
        return makeJson(schedule.delete_data(user_id, data_id))

    elif req == 'set':
        year = str(request.args.get('year'))
        month = str(request.args.get('month'))
        day = str(request.args.get('day'))
        title = str(request.args.get('title'))
        budget = str(request.args.get('budget')) # Optional
        spent = str(request.args.get('spent')) # Optional
        category = str(request.args.get('category')) # Optional
        details = str(request.args.get('details')) # Optional

        print(f"year: {year}")
        print(f"month: {month}")
        print(f"day: {day}")
        print(f"title: {title}")
        print(f"budget: {budget}")
        print(f"spent: {spent}")
        print(f"category: {category}")
        print(f"details: {details}")

        if year == "None" or year == '':
            return makeJson('year: Invalid year: empty')
        if not year.isdecimal():
            return makeJson('year: Invalid year: not decimal')
        if not (1970 <= int(year) <= 3000):
            return makeJson('year: Invalid year: out of range (1970-3000)')

        if month == "None" or month == '':
            return makeJson('month: Invalid month: empty')
        if not month.isdecimal():
            return makeJson('month: Invalid month: not decimal')
        if not (0 <= int(month) <= 12):
            return makeJson('month: Invalid month: out of range (0-12)')

        if day == "None" or day == '':
            return makeJson('day: Invalid day: empty')
        if not day.isdecimal():
            return makeJson('day: Invalid day: not decimal')
        if not (1 <= int(day) <= 31):
            return makeJson('day: Invalid day: out of range (1-31)')

        if title == "None" or title == '':
            return makeJson('title: Invalid title: empty')

        if budget == "None" or budget == '':
            print("budget is empty -> set 0")
            budget = "0"
        if not budget.isdecimal():
            return makeJson('budget: Invalid budget: not decimal')
        if int(budget) < 0:
            return makeJson('budget: Invalid budget: negative value')
        
        if spent == "None" or spent == '':
            print("spent is empty -> set 0")
            spent = "0"
        if not spent.isdecimal():
            return makeJson('spent: Invalid spent: not decimal')
        if int(spent) < 0:
            return makeJson('spent: Invalid spent: negative value')

        if category == "None" or category == '':
            print("category is empty -> set 0")
            category = "0" # その他
        if not category.isdecimal():
            return makeJson('category: Invalid category: not decimal')
        if int(category) < 0:
            return makeJson('category: Invalid category: negative value')
        
        if details == "None" or details == '':
            details = ""

        return makeJson(schedule.add_data(user_id, year, month, day, title, budget, spent, category, details))

    else:
        return makeJson('Invalid request')



# テンプレートのリクエストを処理
@app.route('/template', methods=['GET'])
def template_request():
    """
    テンプレートリクエストを処理する関数
    リクエストの種類に応じて、テンプレートを取得または設定
    リクエストパラメータ:
        req (str): リクエストの種類 ('get' または 'set')
        id (str): ユーザーID
        title (str): タイトル ('set' リクエストの場合必須)
        budget (str): 予算
    戻り値:
        str(json): テンプレート情報または設定結果
    """
    print("template_request")

    req = request.args.get('req')
    user_id = request.args.get('id')

    print(f"req: {req}")
    print(f"user_id: {user_id}")

    if user_id is None or user_id == '':
        return makeJson('id: Invalid user_id: empty')
    if not account.account_isExists(user_id):
        return makeJson('id: Account not found')
    
    if req == 'get': # テンプレートすべて取得
        return makeJson(template.get_templates(user_id))
    elif req == 'set':
        title = request.args.get('title')
        budget = str(request.args.get('budget'))
        print(f"title: {title}")
        print(f"budget: {budget}")
        if title is None or title == '':
            return makeJson('title: Invalid title: empty')
        if budget == "None" or budget == '':
            return makeJson('budget: Invalid budget: empty')
        if not budget.isdecimal():
            return makeJson('budget: Invalid budget: not decimal')
        return makeJson(template.set_template(user_id, title, budget))
    else:
        return makeJson('Invalid request')



# カテゴリのリクエストを処理
@app.route('/category', methods=['GET'])
def category_request():
    """
    カテゴリリクエストを処理する関数。
    リクエストの種類に応じて、カテゴリの取得または設定を行います。
    リクエストパラメータ:
        req (str): リクエストの種類 ('get' または 'set')。
        id (str): ユーザーID。
        title (str): タイトル ('set' リクエストの場合必須)。
    戻り値:
        dict: カテゴリ情報または設定結果。
    """
    print("category_request")

    req = request.args.get('req')
    user_id = request.args.get('id')

    print(f"req: {req}")
    print(f"user_id: {user_id}")

    if user_id is None or user_id == '':
        return makeJson('id: Invalid user_id: empty')
    if not account.account_isExists(user_id):
        return makeJson('id: Account not found')

    if req == 'get':
        category_id = str(request.args.get('category_id'))
        print(f"category_id: {category}")
        if category_id == "None" or category_id == '':
            return makeJson('category_id: Invalid category_id: empty')
        if not category_id.isdecimal():
            return makeJson('category_id: Invalid category_id: not decimal')
        return makeJson(category.get_category_fromId(user_id, category_id))
    elif req == 'getall':
        return makeJson(category.get_categories(user_id))
    elif req == 'set':
        title = request.args.get('title')
        if title is None or title == '':
            return makeJson('title: Invalid title: empty')
        return makeJson(category.set_category(user_id, title))
    else:
        return makeJson('Invalid request')



if __name__ == '__main__':
    app.run(debug=True)