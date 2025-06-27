from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)
db.init_db()

@app.route("/")
def index():
    items = db.get_items()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    db.add_item(request.form["item"])
    return redirect("/")

@app.route("/done/<int:item_id>")
def done(item_id):
    db.mark_done(item_id)
    return redirect("/")

@app.route("/delete/<int:item_id>")
def delete(item_id):
    db.delete_item(item_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
