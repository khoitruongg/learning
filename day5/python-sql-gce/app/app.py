from flask import Flask, request, redirect, render_template_string
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# DB helper
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )

# HTML Template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>User Management</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7fc;
            color: #333;
            margin: 0;
            padding: 20px;
        }

        h1, h2 {
            color: #4CAF50;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        ul li {
            background-color: #f9f9f9;
            padding: 10px;
            margin: 5px 0;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        form {
            margin-top: 20px;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        input[type="text"], input[type="email"], button {
            padding: 10px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 100%;
            box-sizing: border-box;
        }

        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        a {
            color: #ff5722;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Management</h1>

        <h2>User List</h2>
        <ul>
            {% for user in users %}
                <li>
                    <span>{{ user.name }} ({{ user.email }})</span>
                    <div>
                        <a href="/edit/{{ user.id }}">Edit</a> |
                        <a href="/delete/{{ user.id }}" onclick="return confirm('Delete this user?');">Delete</a>
                    </div>
                </li>
            {% endfor %}
        </ul>

        <h2>Add New User</h2>
        <form method="POST" action="/add">
            Name: <input type="text" name="name" required><br>
            Email: <input type="email" name="email" required><br>
            <button type="submit">Add User</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return render_template_string(TEMPLATE, users=users)

@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Error: {e}"
    return redirect("/")

@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Error: {e}"
    return redirect("/")

@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        try:
            cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
            conn.commit()
        except Exception as e:
            return f"Error: {e}"
        finally:
            cur.close()
            conn.close()
        return redirect("/")
    else:
        cur.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            name, email = user
            return f"""
            <h1>Edit User</h1>
            <form method="POST">
                Name: <input type="text" name="name" value="{name}" required><br><br>
                Email: <input type="email" name="email" value="{email}" required><br><br>
                <button type="submit">Update</button>
            </form>
            """
        else:
            return "User not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
