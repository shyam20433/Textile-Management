
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import random
import smtplib
import os
from datetime import datetime

app = Flask(__name__, template_folder='template')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")
try:
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
    client.admin.command('ping')
    db = client['textiles']
    login_collection = db['login']
    dresses_collection = db['dress']
    dress_types_collection = db['confirmed_order']
    reviews_collection = db['reviews']
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    db = None
    login_collection = None
    dresses_collection = None
    dress_types_collection = None
    reviews_collection = None
image_url_map_baby = {
    "Half Hand": {
        'black': '/static/dress/black ft.jpg',
        'red': '/static/dress/red ft.jpg',
        'blue': '/static/dress/blue ft.jpg',
        'milk': '/static/dress/milk ft.jpg',
        'yellow': '/static/dress/yellow ft.jpg',
        'brown': '/static/dress/brown hft.jpg',
    },
    "Full Hand": {
        'black': '/static/dress/black fft.jpg',
        'red': '/static/dress/red fft.jpg',
        'blue': '/static/dress/blue fft.jpg',
        'milk': '/static/dress/milk fft.jpg',
        'yellow': '/static/dress/yellow fft.jpg',
        'brown': '/static/dress/brown ft.jpg',
    },
    "Shorts": {
        'black': '/static/dress/black sft.jpg',
        'red': '/static/dress/red sft.jpg',
        'blue': '/static/dress/blue sft.jpg',
        'milk': '/static/dress/milk sft.jpg',
        'yellow': '/static/dress/yellow sft.jpg',
        'brown': '/static/dress/brown sft.jpg',
    },
    "Sleeveless": {
        'black': '/static/dress/black bsl.jpg',
        'red': '/static/dress/red bsl.jpg',
        'blue': '/static/dress/blue bsl.jpg',
        'milk': '/static/dress/milk bsl.jpg',
        'yellow': '/static/dress/yellow bsl.jpg',
        'brown': '/static/dress/brown bsl.jpg',
    },
    "Hooded onesie": {
        'black': '/static/dress/black bh.jpg',
        'red': '/static/dress/red bh.jpg',
        'blue': '/static/dress/blue bh.jpg',
        'milk': '/static/dress/milk bh.jpg',
        'yellow': '/static/dress/yellow bh.jpg',
        'brown': '/static/dress/brown bh.jpg',
    },
    "Baby sweat suit": {
        'black': '/static/dress/black bss.jpg',
        'red': '/static/dress/red bss.jpg',
        'blue': '/static/dress/blue bss.jpg',
        'milk': '/static/dress/milk bss.jpg',
        'yellow': '/static/dress/yellow bss.jpg',
        'brown': '/static/dress/brown bss.jpg',
    },
    "Cotton jumpsuit":{
        'black': '/static/dress/black bj.jpg',
        'red': '/static/dress/red bj.jpg',
        'blue': '/static/dress/blue bj.jpg',
        'milk': '/static/dress/milk bj.jpg',
        'yellow': '/static/dress/yellow bj.jpg',
        'brown': '/static/dress/brown bj.jpg',
    }
}
image_url_map_men = {
    "Full Hand": {
        'black': '/static/dress/black ffb.jpg',
        'red': '/static/dress/red ffb.jpg',
        'blue': '/static/dress/blue ffb.jpg',
        'milk': '/static/dress/milk ffb.jpg',
        'yellow': '/static/dress/yellow ffb.jpg',
        'brown': '/static/dress/brown ffb.jpg',
    },
    "Half Hand": {
        'black': '/static/dress/black hfb.jpg',
        'red': '/static/dress/red hfb.jpg',
        'blue': '/static/dress/blue hfb.jpg',
        'milk': '/static/dress/milk hfb.jpg',
        'yellow': '/static/dress/yellow hfb.jpg',
        'brown': '/static/dress/brown hfb.jpg',
    },
    "Casual": {
        'black': '/static/dress/black cfb.jpg',
        'red': '/static/dress/red cfb.jpg',
        'blue': '/static/dress/blue cfb.jpg',
        'milk': '/static/dress/milk cfb.jpg',
        'yellow': '/static/dress/yellow cfb.jpg',
        'brown': '/static/dress/brown cfb.jpg',
    },
    "T-Shirt": {
        'black': '/static/dress/black p.jpg',
        'red': '/static/dress/red p.jpg',
        'blue': '/static/dress/blue p.jpg',
        'milk': '/static/dress/milk p.jpg',
        'yellow': '/static/dress/yellow p.jpg',
        'brown': '/static/dress/brown p.jpg',
    },
    "Long sleeve": {
        'black': '/static/dress/black jfw.jpg',
        'red': '/static/dress/red jfw.jpg',
        'blue': '/static/dress/blue jfw.jpg',
        'milk': '/static/dress/milk jfw.jpg',
        'yellow': '/static/dress/yellow jfw.jpg',
        'brown': '/static/dress/brown jfw.jpg',
    }
}
image_url_map_women = {
    'Open Front':{
        'black': '/static/dress/black of.jpg',
        'red': '/static/dress/red of.jpg',
        'blue': '/static/dress/blue of.jpg',
        'milk': '/static/dress/milk of.jpg',
        'yellow': '/static/dress/yellow of.jpg',
        'brown': '/static/dress/brown of.jpg',
    },
    "Straight":{
        'black': '/static/dress/black wps.jpg',
        'red': '/static/dress/red ws.jpg',
        'blue': '/static/dress/blue ws.jpg',
        'milk': '/static/dress/milk ws.jpg',
        'yellow': '/static/dress/yellow ws.jpg',
        'brown': '/static/dress/brown ws.jpg',
    },
    "Skinny": {
        'black': '/static/dress/black wps.jpg',
        'red': '/static/dress/red wps.jpg',
        'blue': '/static/dress/blue wps.jpg',
        'milk': '/static/dress/milk wps.jpg',
        'yellow': '/static/dress/yellow wps.jpg',
        'brown': '/static/dress/brown wps.jpg',
    },
    "Wide Leg": {
        'black': '/static/dress/black ww.jpg',
        'red': '/static/dress/red ww.jpg',
        'blue': '/static/dress/blue ww.jpg',
        'milk': '/static/dress/milk ww.jpg',
        'yellow': '/static/dress/yellow ww.jpg',
        'brown': '/static/dress/brown ww.jpg',
    },
    "Long sleeve": {
        'black': '/static/dress/black jfw.jpg',
        'red': '/static/dress/red jfw.jpg',
        'blue': '/static/dress/blue jfw.jpg',
        'milk': '/static/dress/milk jfw.jpg',
        'yellow': '/static/dress/yellow jfw.jpg',
        'brown': '/static/dress/brown jfw.jpg',
    }
}
def send_reset_email(email, token):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: http://localhost:5000/reset_password/{token}"
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(str(sender_email or ''), str(sender_password or ''))
            server.sendmail(str(sender_email or ''), str(email or ''), message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
@app.route('/')
def home():
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if login_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email') or ''
        password = request.form.get('password') or ''
        user = login_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password or ''):
            session['username'] = user['username']
            session['user_email'] = user['email']
            flash("Login successful!")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password. Please try again.")
    return render_template('login.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if login_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form.get('email', type=str)
        contact = request.form.get('contact', type=str)
        phone = request.form.get('phone', type=str)
        street = request.form.get('street', type=str)
        city = request.form.get('city', type=str)
        state = request.form.get('state', type=str)
        zip_code = request.form.get('zip', type=str)
        username = request.form.get('username', type=str)
        password = request.form.get('password', type=str)
        existing_user = login_collection.find_one({"email": email})
        if existing_user:
            flash("Email already exists. Please log in.")
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(password or '')
        login_collection.insert_one({
            "username": username or '',
            "email": email or '',
            "password": hashed_password,
            "contact": contact or '',
            "street": street or '',
            "city": city or '',
            "state": state or '',
            "zip": zip_code or ''
        })
        flash("Signup successful! Please log in.")
        return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/index')
def index():
    if dresses_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('index.html', dresses=[])
    dresses = dresses_collection.find()
    dress_list = list(dresses)
    return render_template('index.html', dresses=dress_list)
@app.route('/dress/<dress_id>')
def dress_detail(dress_id):
    if dresses_collection is None or reviews_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('index'))
    try:
        dress = dresses_collection.find_one({"_id": ObjectId(dress_id)})
        if dress:
            related_dresses = dresses_collection.find({"color": dress['color']})
            reviews = list(reviews_collection.find({"dress_id": ObjectId(dress_id)}))
            total_rating = sum(review['rating'] for review in reviews)
            average_rating = total_rating / len(reviews) if reviews else None
            return render_template('dress_detail.html', dress=dress, related_dresses=related_dresses, reviews=reviews,
                                   average_rating=average_rating)
        else:
            flash("Dress not found.")
            return redirect(url_for('index'))
    except Exception as e:
        flash("Invalid dress ID.")
        return redirect(url_for('index'))
@app.route('/dress/<dress_id>/review', methods=['POST'])
def submit_review(dress_id):
    if reviews_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('dress_detail', dress_id=dress_id))
    review_text = request.form.get('review_text')
    rating = request.form.get('rating')
    if 'username' not in session:
        flash("You must be logged in to submit a review.")
        return redirect(url_for('dress_detail', dress_id=dress_id))
    username = session['username']
    if not rating:
        flash("Please select a rating.")
        return redirect(url_for('dress_detail', dress_id=dress_id))
    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 5:
            flash("Rating must be between 1 and 5.")
            return redirect(url_for('dress_detail', dress_id=dress_id))
    except ValueError:
        flash("Invalid rating value.")
        return redirect(url_for('dress_detail', dress_id=dress_id))
    reviews_collection.insert_one({
        "dress_id": ObjectId(dress_id),
        "review_text": review_text,
        "rating": rating_value,
        "username": username
    })
    flash("Review submitted successfully!")
    return redirect(url_for('dress_detail', dress_id=dress_id))
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if login_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('forgot_password.html')
    if request.method == 'POST':
        email = request.form.get('email')
        user = login_collection.find_one({"email": email})
        if user:
            token = str(random.randint(100000, 999999))
            send_reset_email(email, token)
            flash("A password reset link has been sent to your email.")
            return redirect(url_for('verify_otp', email=email, token=token))
        else:
            flash("Email not found. Please check and try again.")
    return render_template('forgot_password.html')
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        email = request.form.get('email')
        session['otp'] = otp
        flash("OTP verified successfully! Please reset your password.")
        return redirect(url_for('reset_password', email=email))
    email = request.args.get('email')
    return render_template('verify_otp.html', email=email)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if login_collection is None:
        flash("Database connection error. Please try again later.")
        return render_template('reset_password.html', email=None)
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        email = request.form.get('email')
        if email and new_password:
            hashed_password = generate_password_hash(new_password)
            login_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
            flash("Your password has been reset successfully. Please log in.")
            return redirect(url_for('login'))
    email = request.args.get('email')
    return render_template('reset_password.html', email=email)
@app.route('/order_customization/<dress_id>', methods=['GET', 'POST'])
def order_customization(dress_id):
    if dresses_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('index'))
    try:
        dress = dresses_collection.find_one({"_id": ObjectId(dress_id)})
    except Exception as e:
        flash("Invalid dress ID.")
        return redirect(url_for('index'))
    if not dress:
        flash("Dress not found.")
        return redirect(url_for('index'))
    if request.method == 'POST':
        gender = request.form.get('gender')
        dress_design = request.form.get('dress_design')
        dress_type = request.form.get('dress_type')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        if not all([gender, dress_design, dress_type, size, quantity]):
            flash("Please fill in all required fields.")
            return render_template('order_customization.html', dress=dress)
        if not color:
            color = dress.get('color', 'N/A')
        image_url = dress.get('image_url')
        if gender and dress_design and color:
            if gender == 'baby' and dress_design in image_url_map_baby and color in image_url_map_baby[dress_design]:
                image_url = image_url_map_baby[dress_design][color]
            elif gender == 'men' and dress_design in image_url_map_men and color in image_url_map_men[dress_design]:
                image_url = image_url_map_men[dress_design][color]
            elif gender == 'women' and dress_design in image_url_map_women and color in image_url_map_women[dress_design]:
                image_url = image_url_map_women[dress_design][color]
        session['order_customization'] = {
            "dress_id": dress_id,
            "gender": gender,
            "dress_type": dress_type,
            "dress_design": dress_design,
            "color": color,
            "size": size,
            "quantity": quantity,
            "username": session.get('username'),
            "email": session.get('user_email'),
            "image_url": image_url,
            "base_price": dress.get('price', 0)
        }
        return redirect(url_for('review_order', dress_id=dress_id))
    return render_template('order_customization.html', dress=dress)
@app.route('/review_order/<dress_id>', methods=['GET', 'POST'])
def review_order(dress_id):
    if dresses_collection is None or login_collection is None or dress_types_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('index'))
    try:
        dress = dresses_collection.find_one({"_id": ObjectId(dress_id)})
    except Exception as e:
        flash("Invalid dress ID.")
        return redirect(url_for('index'))
    if not dress:
        flash("Dress not found.")
        return redirect(url_for('index'))
    order_customization = session.get('order_customization', None)
    if not order_customization:
        flash("No order details found. Please customize your order.")
        return redirect(url_for('order_customization', dress_id=dress_id))
    try:
        base_price = float(order_customization.get('base_price', 0))
        quantity = int(order_customization.get('quantity', 1))
    except (ValueError, TypeError):
        base_price = 0.0
        quantity = 1
    total_price = base_price * quantity
    if request.method == 'POST':
        final_quantity = request.form.get('quantity', quantity)
        final_color = request.form.get('color', order_customization.get('color'))
        final_size = request.form.get('size', order_customization.get('size'))
        final_dress_type = request.form.get('dress_type', order_customization.get('dress_type'))
        final_dress_design = request.form.get('dress_design', order_customization.get('dress_design'))
        final_gender = request.form.get('gender', order_customization.get('gender'))
        try:
            final_quantity = int(final_quantity)
        except (ValueError, TypeError):
            final_quantity = 1
        final_total_price = base_price * final_quantity
        email = session.get('user_email')
        user = login_collection.find_one({"email": email}) if email else None
        user_id = str(user['_id']) if user and '_id' in user else ''
        image_url = order_customization.get('image_url', dress.get('image_url'))
        order_data = {
            "dress_id": ObjectId(dress_id),
            "user_id": user_id,
            "order_date": datetime.utcnow(),
            "status": "Pending",
            "dress_details": {
                "color": final_color,
                "gender": final_gender,
                "dress_type": final_dress_type,
                "dress_design": final_dress_design,
                "size": final_size,
                "quantity": final_quantity,
                "price": base_price,
                "total_price": final_total_price,
                "image_url": image_url
            },
            "user_details": {
                "username": user['username'] if user and 'username' in user else '',
                "email": user['email'] if user and 'email' in user else '',
                "contact": user['contact'] if user and 'contact' in user else '',
                "address": {
                    "street": user['street'] if user and 'street' in user else '',
                    "city": user['city'] if user and 'city' in user else '',
                    "state": user['state'] if user and 'state' in user else '',
                    "zip": user['zip'] if user and 'zip' in user else ''
                }
            }
        }
        result = dress_types_collection.insert_one(order_data)
        session['order_id'] = str(result.inserted_id)
        session.pop('order_customization', None)
        flash("Order placed successfully!")
        return redirect(url_for('order_success'))
    return render_template('review_order.html', 
                         dress=dress, 
                         gender=order_customization.get('gender'),
                         dress_type=order_customization.get('dress_type'), 
                         dress_design=order_customization.get('dress_design'),
                         size=order_customization.get('size'), 
                         quantity=quantity, 
                         color=order_customization.get('color'),
                         image_url=order_customization.get('image_url'), 
                         total_price=total_price)
@app.route('/order_success')
def order_success():
    if dress_types_collection is None:
        flash("Database connection error. Please try again later.")
        return redirect(url_for('index'))
    order_id = session.get('order_id')
    if not order_id:
        flash("No order details found. Please place an order first.")
        return redirect(url_for('index'))
    order = dress_types_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        flash("Order not found.")
        return redirect(url_for('index'))
    user = order.get('user_details', {})
    dress_details = order.get('dress_details', {})
    return render_template('order_success.html', order=order, user=user, dress_details=dress_details)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    app.run(host="0.0.0.0", port=8080, debug=True)