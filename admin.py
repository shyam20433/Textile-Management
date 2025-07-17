from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='admin_template', static_folder='static')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "adminsecret")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

try:
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
    client.admin.command('ping')
    db = client['textiles']
    dresses_collection = db['dress']
    reviews_collection = db['reviews']
    login_collection = db['login']
    confirmed_orders = db['confirmed_order']
    print("Admin MongoDB connection successful!")
except Exception as e:
    print(f"Admin MongoDB connection failed: {e}")
    db = None
    dresses_collection = None
    reviews_collection = None
    login_collection = None
    confirmed_orders = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def admin_dashboard():
    if (login_collection is None or dresses_collection is None or 
        confirmed_orders is None or reviews_collection is None):
        flash("Database connection error. Please try again later.")
        return render_template('admin_dashboard.html', users=0, dresses=0,
                               orders=0, reviews=0, recent_orders=[], 
                               recent_reviews=[], revenue=0)
    total_users = login_collection.count_documents({})
    total_dresses = dresses_collection.count_documents({})
    total_orders = confirmed_orders.count_documents({})
    total_reviews = reviews_collection.count_documents({})
    orders_cursor = confirmed_orders.find().sort("order_date", -1).limit(3)
    recent_orders = []
    for order in orders_cursor:
        price = order.get('dress_details', {}).get('price', 0)
        quantity = order.get('dress_details', {}).get('quantity', 1)
        try:
            price = float(price)
        except Exception:
            price = 0
        try:
            quantity = int(quantity)
        except Exception:
            quantity = 1
        total = price * quantity
        price_str = f"₹{int(total)}" if total else "₹0"
        status_str = str(order.get('status', 'N/A'))
        recent_orders.append({
            "order_id": str(order.get('_id'))[:7],
            "customer": order.get('user_details', {}).get('username', 'N/A'),
            "dress": order.get('dress_details', {}).get('dress_type', 'N/A'),
            "amount": price_str,
            "status": status_str
        })
    reviews_cursor = reviews_collection.find().sort("_id", -1).limit(3)
    recent_reviews = []
    for review in reviews_cursor:
        recent_reviews.append({
            "rating": review.get('rating', 0),
            "title": review.get('review_text', '')[:20] + ("..." if len(review.get('review_text', '')) > 20 else ""),
            "text": review.get('review_text', ''),
            "author": review.get('username', 'Anonymous')
        })
    revenue = 0
    for order in confirmed_orders.find({"status": "Delivered"}):
        try:
            price = float(order.get('dress_details', {}).get('price', 0))
            quantity = int(order.get('dress_details', {}).get('quantity', 1))
            revenue += price * quantity
        except Exception:
            continue
    revenue = int(revenue)
    return render_template('admin_dashboard.html', users=total_users, dresses=total_dresses,
                           orders=total_orders, reviews=total_reviews,
                           recent_orders=recent_orders, recent_reviews=recent_reviews,
                           revenue=revenue)

@app.route('/admin/dresses')
def admin_dresses():
    if dresses_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('admin_dresses.html', dresses=[])
    dresses = list(dresses_collection.find())
    return render_template('admin_dresses.html', dresses=dresses)

@app.route('/admin/dress/add', methods=['GET', 'POST'])
def add_dress():
    if dresses_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('add_dress.html')
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        color = request.form.get('color', '').strip()
        price = request.form.get('price', '').strip()
        description = request.form.get('description', '').strip()
        dress_type = request.form.get('type', '').strip()
        if not all([name, color, price, description, dress_type]):
            flash("All fields are required.", "error")
            return redirect(request.url)
        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            flash("Price must be a positive number.", "error")
            return redirect(request.url)
        image = request.files.get('image')
        if not image or not image.filename or not allowed_file(image.filename):
            flash("A valid image file (.jpg, .jpeg, .png) is required.", "error")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_url = f"/static/uploads/{filename}"
        dresses_collection.insert_one({
            "name": name,
            "color": color,
            "price": price,
            "description": description,
            "type": dress_type,
            "image_url": image_url
        })
        flash("New dress added successfully.", "success")
        return redirect(url_for('admin_dresses'))
    return render_template('add_dress.html')

@app.route('/admin/dress/edit/<dress_id>', methods=['GET', 'POST'])
def edit_dress(dress_id):
    if dresses_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('admin_dresses'))
    dress = dresses_collection.find_one({"_id": ObjectId(dress_id)})
    if not dress:
        flash("Dress not found.", "error")
        return redirect(url_for('admin_dresses'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        color = request.form.get('color', '').strip()
        price = request.form.get('price', '').strip()
        description = request.form.get('description', '').strip()
        dress_type = request.form.get('type', '').strip()
        if not all([name, color, price, description, dress_type]):
            flash("All fields are required.", "error")
            return redirect(request.url)
        try:
            price = float(price)
            if price < 0:
                raise ValueError
        except ValueError:
            flash("Price must be a positive number.", "error")
            return redirect(request.url)
        update_data = {
            "name": name,
            "color": color,
            "price": price,
            "description": description,
            "type": dress_type
        }
        image = request.files.get('image')
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            update_data['image_url'] = f"/static/uploads/{filename}"
        dresses_collection.update_one({"_id": ObjectId(dress_id)}, {"$set": update_data})
        flash("Dress updated successfully.", "success")
        return redirect(url_for('admin_dresses'))
    return render_template('edit_dress.html', dress=dress)

@app.route('/admin/dress/delete/<dress_id>')
def delete_dress(dress_id):
    if dresses_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('admin_dresses'))
    dresses_collection.delete_one({"_id": ObjectId(dress_id)})
    flash('Dress deleted successfully.')
    return redirect(url_for('admin_dresses'))

@app.route('/admin/reviews')
def admin_reviews():
    if reviews_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('admin_reviews.html', reviews=[])
    reviews = list(reviews_collection.find())
    return render_template('admin_reviews.html', reviews=reviews)

@app.route('/admin/review/delete/<review_id>')
def delete_review(review_id):
    if reviews_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('admin_reviews'))
    reviews_collection.delete_one({"_id": ObjectId(review_id)})
    flash('Review deleted successfully.')
    return redirect(url_for('admin_reviews'))

@app.route('/admin/users')
def admin_users():
        flash("Database connection error. Please try again later.")
        return render_template('admin_users.html', users=[])
    users = list(login_collection.find())
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/delete/<user_id>')
def delete_user(user_id):
    if login_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('admin_users'))
    login_collection.delete_one({"_id": ObjectId(user_id)})
    flash('User deleted successfully.')
    return redirect(url_for('admin_users'))

@app.route('/admin/orders')
def admin_orders():
    if confirmed_orders is None:
        flash("Database connection error. Please try again later.")
        return render_template("admin_orders.html", orders=[], stats={})
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    query = {}
    if search:
        query['$or'] = [
            {'user_details.username': {'$regex': search, '$options': 'i'}},
            {'user_details.email': {'$regex': search, '$options': 'i'}}
        ]
    if status_filter:
        query['status'] = status_filter
    orders = list(confirmed_orders.find(query).sort("order_date", -1))
    if dresses_collection is not None:
        for order in orders:
            if order.get('dress_id'):
                original_dress = dresses_collection.find_one({"_id": order['dress_id']})
                if original_dress:
                    order['original_dress'] = original_dress
    stats = {
        "total": confirmed_orders.count_documents({}),
        "pending": confirmed_orders.count_documents({"status": "Pending"}),
        "dispatched": confirmed_orders.count_documents({"status": "Dispatched"}),
        "delivered": confirmed_orders.count_documents({"status": "Delivered"})
    }
    return render_template("admin_orders.html", orders=orders, stats=stats)

@app.route('/admin/order/update/<order_id>', methods=['POST'])
def update_order(order_id):
    if confirmed_orders is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('admin_orders'))
    new_status = request.form.get('status')
    confirmed_orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": new_status}})
    flash('Order status updated.')
    return redirect(url_for('admin_orders'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
