from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Home
@app.route("/")
def home():
    return render_template("home.html")



# Services Page
@app.route("/services")
def services():
    return render_template("services.html")

# Booking Page
@app.route("/book", methods=["GET", "POST"])
# def book():
#     # selected_service = request.args.get("service")
#     # return render_template("book.html", selected_service=selected_service)
#     if request.method == "POST":
#         name = request.form["name"]
#         phone = request.form["phone"]
#         service = request.form["service"]
#         address = request.form["address"]

#         conn = sqlite3.connect("database.db")
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO bookings (name, phone, service, address) VALUES (?, ?, ?, ?)",
#                        (name, phone, service, address))
#         conn.commit()
#         conn.close()

#         return redirect("/")

#     return render_template("book.html")
# Booking Page
@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        services = request.form.getlist("services[]")
        services_str = ", ".join(services)

        # calculate total price (same as frontend)
        prices = {
            "AC Repair": 499,
            "Electrician": 199,
            "Plumbing": 299,
            "Painting": 2000,
            "Garden": 499,
            "Pest Control": 999
        }

        total_price = sum(prices[s] for s in services)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (name, phone, services, address, total_price) VALUES (?, ?, ?, ?, ?)",
            (name, phone, services_str, address, total_price)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("book.html")

# Admin Panel
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["password"] != "victorji123":
            return "Wrong Password"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        data = cursor.fetchall()
        conn.close()
        return render_template("admin.html", data=data)

    return '''
    <form method="post">
    <input type="password" name="password" placeholder="Admin Password">
    <button type="submit">Login</button>
    </form>
    '''

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
