import os
import time
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "apppass")


def get_connection():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to the database after several retries.")


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM messages ORDER BY id DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", messages=rows)


@app.route("/add", methods=["POST"])
def add_message():
    content = request.form.get("content", "").strip()
    if content:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (content) VALUES (%s);", (content,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
