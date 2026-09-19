"""
Developed by MASA
All Rights Reserved.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("MASA - Bank Management System with SQLite")
        self.root.geometry("1100x660")
        self.root.configure(bg="#0f172a")

        self.init_db()
        self.setup_ui()
        self.fetch_accounts()

    def init_db(self):
        self.conn = sqlite3.connect("bank_vault.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                acc_no TEXT PRIMARY KEY,
                holder_name TEXT NOT NULL,
                acc_type TEXT NOT NULL,
                balance REAL NOT NULL,
                email TEXT,
                phone TEXT,
                status TEXT
            )
        """)
        self.cur.execute("SELECT COUNT(*) FROM accounts")
        if self.cur.fetchone()[0] == 0:
            sample_data = [
                ("ACC-90112", "Alexander Wright", "Savings", 14500.00, "alex@fintech.io", "+1 555-0192", "Active"),
                ("ACC-90113", "Eleanor Vance", "Current", 48200.50, "eleanor@corp.com", "+1 555-0144", "Active"),
                ("ACC-90114", "Dmitri Volkov", "Savings", 8300.00, "dmitri@nordic.net", "+1 555-0183", "Active"),
                ("ACC-90115", "Sophia Martinez", "Investment", 125000.00, "sophia@invest.co", "+1 555-0167", "Active"),
                ("ACC-90116", "Marcus Aurelius", "Current", 3240.00, "marcus@rome.it", "+1 555-0131", "Dormant"),
            ]
            self.cur.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)", sample_data)
            self.conn.commit()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e293b", foreground="#f8fafc", fieldbackground="#1e293b", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#334155", foreground="#38bdf8", font=("Segoe UI", 10, "bold"))

        hdr = tk.Frame(self.root, bg="#0284c7", height=65)
        hdr.pack(fill="x")
        tk.Label(hdr, text="MASA Core Banking & Account Operations", font=("Segoe UI", 19, "bold"), fg="#ffffff", bg="#0284c7").pack(side="left", padx=25, pady=15)
        tk.Label(hdr, text="Architecture: MASA | MIT License: XREFS0", font=("Segoe UI", 10), fg="#bae6fd", bg="#0284c7").pack(side="right", padx=25, pady=20)

        body = tk.Frame(self.root, bg="#0f172a")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        sidebar = tk.Frame(body, bg="#1e293b", width=220)
        sidebar.pack(side="left", fill="y", padx=(0, 15))

        for btn_t in ["Account Directory", "Open Account", "Deposit Funds", "Withdrawal Desk", "Account Transfer", "Statement Audit"]:
            tk.Button(sidebar, text=btn_t, font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#334155", relief="flat", pady=9, cursor="hand2").pack(fill="x", padx=10, pady=5)

        content = tk.Frame(body, bg="#1e293b")
        content.pack(side="right", fill="both", expand=True)

        stats = tk.Frame(content, bg="#1e293b")
        stats.pack(fill="x", padx=15, pady=15)

        for t, v, c in [("Vault Deposits", "$199,240.50", "#4ade80"), ("Active Accounts", "1,420", "#38bdf8"), ("Daily Transactions", "248", "#facc15"), ("Compliance Rate", "100%", "#a855f7")]:
            f = tk.Frame(stats, bg="#334155", padx=14, pady=9)
            f.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(f, text=t, font=("Segoe UI", 9), fg="#94a3b8", bg="#334155").pack(anchor="w")
            tk.Label(f, text=v, font=("Segoe UI", 15, "bold"), fg=c, bg="#334155").pack(anchor="w")

        cols = ("Account No", "Account Holder", "Type", "Balance", "Email Address", "Contact Phone", "Status")
        self.tree = ttk.Treeview(content, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.column("Account Holder", width=160, anchor="w")
        self.tree.column("Email Address", width=160, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def fetch_accounts(self):
        self.cur.execute("SELECT * FROM accounts")
        for row in self.cur.fetchall():
            formatted = list(row)
            formatted[3] = f"${formatted[3]:,.2f}"
            self.tree.insert("", "end", values=formatted)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()
