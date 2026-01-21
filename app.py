from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    if request.method == "POST":
        description = request.form["description"]
        amount = request.form["amount"]

        cur.execute(
            "INSERT INTO expenses (description, amount) VALUES (?, ?)",
            (description, amount)
        )
        conn.commit()
        return redirect(url_for("index"))

    # Fetch all expenses
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    conn.close()

    return render_template("index.html", expenses=expenses)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)