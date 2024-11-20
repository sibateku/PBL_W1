import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# データベースの設定
conn = sqlite3.connect('budget_app.db')
cursor = conn.cursor()

# テーブルの作成
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    category TEXT,
                    amount REAL,
                    date TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS fixed_costs (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    amount REAL
                )''')
conn.commit()

# TkinterでのGUI設定
root = tk.Tk()
root.title("家計簿アプリ")
root.geometry("400x300")

# 消費を記録する関数
def add_expense():
    category = simpledialog.askstring("カテゴリ入力", "カテゴリを入力してください")
    amount = simpledialog.askfloat("金額入力", "金額を入力してください")
    date = datetime.now().strftime('%Y-%m-%d')

    if category and amount:
        cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
                       (category, amount, date))
        conn.commit()
        messagebox.showinfo("情報", "消費が記録されました")
    else:
        messagebox.showwarning("エラー", "カテゴリと金額の入力が必要です")

# 固定費を設定する関数
def set_fixed_cost():
    name = simpledialog.askstring("固定費の名称", "固定費の名称を入力してください")
    amount = simpledialog.askfloat("固定費の金額", "固定費の金額を入力してください")

    if name and amount:
        cursor.execute("INSERT INTO fixed_costs (name, amount) VALUES (?, ?)", (name, amount))
        conn.commit()
        messagebox.showinfo("情報", "固定費が設定されました")
    else:
        messagebox.showwarning("エラー", "名称と金額の入力が必要です")

# カテゴリ別消費の円グラフを表示する関数
def show_expense_chart():
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()

    if data:
        categories, amounts = zip(*data)
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title("カテゴリ別消費額")
        plt.show()
    else:
        messagebox.showinfo("情報", "記録された消費がありません")

# GUIのボタンとラベル
add_expense_button = tk.Button(root, text="消費を記録", command=add_expense)
add_expense_button.pack(pady=10)

set_fixed_cost_button = tk.Button(root, text="固定費を設定", command=set_fixed_cost)
set_fixed_cost_button.pack(pady=10)

show_chart_button = tk.Button(root, text="円グラフを表示", command=show_expense_chart)
show_chart_button.pack(pady=10)

# メインループ
root.mainloop()

# 終了時にデータベース接続を閉じる
conn.close()
