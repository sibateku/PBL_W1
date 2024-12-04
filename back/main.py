# coding: utf-8

from flask import Flask
import json

import account, template, schedule, category
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Test!'


# テンプレートのリクエストを処理
@app.route('/account', methods=['GET'])
def account_request():
    """
    'req'パラメータに基づいてアカウント関連のリクエストを処理します
    クエリパラメータ:
        req (str): リクエストの種類。'create', 'delete', 'auth'のいずれか
        id (str): ユーザーID
        password (str): ユーザーのパスワード（'create'および'auth'リクエストに必要）
    戻り値:
        str: アカウント操作の結果、またはリクエストタイプが認識されない場合は'Invalid request'
    """

    req = request.args.get('req')
    user_id = request.args.get('id')
    password = request.args.get('password')

    print(req)
    print(user_id)
    print(password)

    if req == 'create':
        return account.account_create(user_id, password)
    elif req == 'delete':
        return account.account_delete(user_id)
    elif req == 'auth':
        return str(account.account_auth(user_id, password))
    else:
        return 'Invalid request'


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
    戻り値:
        dict: スケジュール情報または設定結果。
    """

    req = request.args.get('req')
    user_id = request.args.get('id')

    if account.account_isExists(user_id) == False:
        return 'Account not found'

    if req == 'get':
        year = request.args.get('year')
        month = request.args.get('month')
        
        return schedule.get_schedule_between(user_id, year, month)
    
    elif req == 'set':
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')
        title = request.args.get('title')
        budget = request.args.get('budget')
        spent = request.args.get('spent')
        category = request.args.get('category')
        
        return schedule.add_data(user_id, year, month, day, title, budget, spent, category)

    else:
        return 'Invalid request'


# テンプレートのリクエストを処理
@app.route('/template', methods=['GET'])
def template_request():
    """
    テンプレートリクエストを処理する関数。
    リクエストの種類に応じて、テンプレートの取得または設定を行います。
    リクエストパラメータ:
        req (str): リクエストの種類 ('get' または 'set')。
        id (str): ユーザーID。
        title (str): タイトル (オプション、'set' リクエストの場合必須)。
        budget (str): 予算 (オプション)。
    戻り値:
        dict: テンプレート情報または設定結果。
    """

    req = request.args.get('req')
    user_id = request.args.get('id')

    if account.account_isExists(user_id) == False:
        return 'Account not found'

    if req == 'get':
        return template.get_templates(user_id)
    
    elif req == 'set':
        title = request.args.get('title')
        budget = request.args.get('budget')
        
        return template.set_template(user_id, title, budget)

    else:
        return 'Invalid request'



# カテゴリのリクエストを処理
@app.route('/category', methods=['GET'])
def category_request():
    """
    カテゴリリクエストを処理する関数。
    リクエストの種類に応じて、カテゴリの取得または設定を行います。
    リクエストパラメータ:
        req (str): リクエストの種類 ('get' または 'set')。
        id (str): ユーザーID。
        title (str): タイトル (オプション、'set' リクエストの場合必須)。
    戻り値:
        dict: カテゴリ情報または設定結果。
    """

    req = request.args.get('req')
    user_id = request.args.get('id')

    if account.account_isExists(user_id) == False:
        return 'Account not found'

    if req == 'get':
        category_id = request.args.get('category_id')
        return category.get_category_fromId(user_id, category_id)
    
    elif req == 'getall':
        return category.get_categories(user_id)
    
    elif req == 'set':
        title = request.args.get('title')
        return category.set_category(user_id, title)

    else:
        return 'Invalid request'



if __name__ == '__main__':
    app.run(debug=True)