<<<<<<< HEAD
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mail import Mail, Message
from firebase import auth, db
import os
import razorpay


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Mail configuration


# Razorpay keys (you should store these in environment variables for production)
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")



razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.route('/create_order', methods=['POST'])
def create_order():
    try:
        amount = int(request.form.get('amount')) * 100  # in paise
        payment = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })
        return jsonify(payment)
    except Exception as e:
        print("Error creating Razorpay order:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/payment_success', methods=['POST'])
def payment_success():
    try:
        data = request.form
        print("Payment Successful:", data)
        # You can save payment info here if needed
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/')
def index():
    email = session.get('user')
    uid = session.get('uid')
    role = session.get('role')
    token = session.get('token')

    if not email:
        return render_template('index.html', user=None)

    # ✅ Safely refresh token if refresh_token is present
    try:
        if 'refresh_token' in session:
            refreshed = auth.refresh(session['refresh_token'])
            session['token'] = refreshed['idToken']
            session['refresh_token'] = refreshed['refreshToken']
            token = session['token']
    except Exception as e:
        print("Token refresh error:", e)

    # ✅ Derive user display name
    name = 'Mohan' if role == 'admin' else email.split('@')[0].split('.')[0].capitalize()

    if role == 'admin':
        try:
            all_services = db.child("user_services").get(token).val() or {}
        except Exception as e:
            print("Admin service fetch error:", e)
            all_services = {}
        return render_template("index.html", user=email, name=name, role=role, all_services=all_services)

    return render_template("index.html", user=email, name=name, role=role)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            # Get both ID token and refresh token
            token = user['idToken']
            refresh_token = user['refreshToken']
            uid = user['localId']

            # Fetch role using current token
            role = db.child("users").child(uid).child("role").get(token).val()

            # Save everything to session
            session['user'] = email
            session['uid'] = uid
            session['role'] = role
            session['token'] = token
            session['refresh_token'] = refresh_token  # ✅ add this

            return redirect(url_for('index'))
        except Exception as e:
            print("Login error:", e)
            return render_template('login.html', error="Invalid email or password.")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = 'admin' if email.lower() == 'maavsolutions@gmail.com' else 'user'

        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            token = user['idToken']
            refresh_token = user['refreshToken']  # ✅ store refresh token

            # Save user info to Firebase DB
            db.child("users").child(uid).set({"email": email, "role": role}, token)

            # Store session details
            session['user'] = email
            session['uid'] = uid
            session['role'] = role
            session['token'] = token
            session['refresh_token'] = refresh_token  # ✅ added

            return redirect(url_for('index'))
        except Exception as e:
            print("Signup error:", e)
            return render_template('signup.html', error="Signup failed.")
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            return render_template('reset_password.html', success="Reset link sent to your email.")
        except:
            return render_template('reset_password.html', error="Failed to send reset link.")
    return render_template('reset_password.html')
=======
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail Configuration (replace with your email settings)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'maavsolutions@gmail.com'
app.config['MAIL_PASSWORD'] = 'hfeyjhxjkgyozjmo'
app.config['MAIL_DEFAULT_SENDER'] = 'maavsolutions@gmail.com'
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        number= request.form.get('number')
        message = request.form.get('message')

        if not all([name, email, message]):
            # Return a JSON response indicating that all fields are required
            return jsonify({'error': 'All fields are required'})
        else:
            # Send email
            subject = 'New Form Submission'
            body = f'''
            Name: {name}
            Email: {email}
            Number: {number}
            Message: {message}
            '''
            try:
                msg = Message(subject, recipients=['maavsolutions@gmail.com'])  # Replace with your personal email
                msg.body = body
                mail.send(msg)
                # Return a JSON response indicating successful submission
                return jsonify({'success': 'Message sent successfully!'})
            except Exception as e:
                # Return a JSON response with an error message
                return jsonify({'error': f'Error sending message: {str(e)}'})

    return render_template('index.html')
    
>>>>>>> 86b260f6abc041dbb2a062364de855e345938ce2


@app.route('/GST.html')
def gst_page():
<<<<<<< HEAD
    email = session.get('user')
    role = session.get('role')
    name = 'Admin' if role == 'admin' else (email.split('@')[0].capitalize() if email else None)

    return render_template('GST.html', user=email, role=role, name=name)


@app.route('/ITR.html')
def itr_page():
    email = session.get('user')
    role = session.get('role')
    name = 'Admin' if role == 'admin' else (email.split('@')[0].capitalize() if email else None)

    return render_template('ITR.html', user=email, role=role, name=name)


@app.route('/BOOKKeeping.html')
def bookkeeping_page():
    email = session.get('user')
    role = session.get('role')
    name = 'Admin' if role == 'admin' else (email.split('@')[0].capitalize() if email else None)

    return render_template('BOOKKeeping.html', user=email, role=role, name=name)
@app.route('/submit_service/<service>', methods=['POST'])
def submit_service(service):
    if 'uid' not in session:
        return redirect(url_for('login_page'))

    uid = session['uid']
    account_email = session['user']
    token = session['token']

    name = email = phone = plan = plan_name = pan = None
    price = 0

    # 📘 Bookkeeping
    if service == 'bookkeeping':
        name = request.form.get('name_bookkeeping')
        email = request.form.get('email_bookkeeping')
        phone = request.form.get('phone_bookkeeping')
        pan = request.form.get('pan_bookkeeping')
        plan = request.form.get('plan_bookkeeping')

        plan_name = plan.split(' - ')[0].strip() if plan else None  # e.g. "Starter"

        price_map = {
            'Starter': 1499,
            'Standard': 2499,
            'Professional': 4999,
            'Enterprise': 7999,
            'Custom Plan': 0
        }

        price = price_map.get(plan_name, -1)
        if price == -1:
            print("❌ Unknown bookkeeping plan:", plan)
            return redirect(url_for('index'))

        full_service = f"Bookkeeping - {plan_name}"

    # 📘 GST
    elif service == 'gst':
        gst_type = request.form.get('gst_type')
        name = request.form.get(f'name_{gst_type}')
        email = request.form.get(f'email_{gst_type}')
        phone = request.form.get(f'phone_{gst_type}')
        pan = request.form.get(f'pan_{gst_type}')
        plan = request.form.get(f'plan_{gst_type}') or "Basic"
        plan_name = plan  # GST plans already short like "Starter", "Standard", etc.

        price = 499 if '499' in plan else \
                999 if '999' in plan else \
                1999 if '1,999' in plan else \
                2999 if '2,999' in plan else 3000

        full_service = f"GST - {gst_type.upper()}"

    # 📘 ITR
    elif service == 'itr':
        itr_type = request.form.get('itr_type')
        name = request.form.get(f'name_{itr_type}')
        email = request.form.get(f'email_{itr_type}')
        phone = request.form.get(f'phone_{itr_type}')
        pan = request.form.get(f'pan_{itr_type}')
        plan_name = f"{itr_type.upper()} Plan"
        plan = plan_name

        itr_prices = {
            'pan': 499,
            'itr1': 999,
            'itr2': 1999,
            'itr3': 2999,
            'itr4': 2999
        }

        price = itr_prices.get(itr_type, -1)
        if price == -1:
            print("❌ Unknown ITR type:", itr_type)
            return redirect(url_for('index'))

        full_service = f"ITR - {itr_type.upper()}"

    else:
        print("❌ Invalid service submitted")
        return redirect(url_for('index'))

    # ✅ Save to user_services
    try:
        db.child("user_services").child(uid).push({
            "account_email": account_email,
            "user_name": name,
            "user_email": email,
            "user_phone": phone,
            "user_pan": pan,
            "service": full_service,
            "plan": plan_name,
            "price": price,
            "status": "in progress",
            "admin_status": "pending"
        }, token)
        print(f"✅ Submitted: {full_service}, Plan: {plan_name}, ₹{price}")
    except Exception as e:
        print("❌ Error saving service:", e)

    # ✅ Save to user_cart
    try:
        db.child("user_cart").child(uid).push({
            "service": full_service,
            "plan": plan_name,
            "price": price,
            "quantity": 1
        }, token)
        print(f"🛒 Added to cart: {full_service} at ₹{price}")
    except Exception as e:
        print("❌ Error saving to cart:", e)

    return redirect(url_for('index'))


@app.route('/update_status/<uid>/<key>/<action>')
def update_status(uid, key, action):
    print(f"[ADMIN ACTION] {action} → UID: {uid}, KEY: {key}")

    if session.get('role') != 'admin':
        return redirect(url_for('index'))

    try:
        # Safely refresh token only if refresh_token exists
        if 'refresh_token' in session:
            refreshed = auth.refresh(session['refresh_token'])
            session['token'] = refreshed['idToken']
            session['refresh_token'] = refreshed['refreshToken']

        token = session['token']

        # Fetch current service data
        service_data = db.child("user_services").child(uid).child(key).get(token).val()
        if not service_data:
            print("❌ No service data found.")
            return redirect(url_for('index'))

        print("🔍 Before update:", service_data)

        updates = {}
        if action == 'accepted':
            updates = {'admin_status': 'accepted', 'status': 'in progress'}
        elif action == 'rejected':
            updates = {'admin_status': 'rejected', 'status': 'in progress'}
        elif action == 'completed':
            current_status = service_data.get('admin_status', 'pending')
            updates = {'status': 'completed', 'admin_status': current_status}
        else:
            print("❌ Invalid action")
            return redirect(url_for('index'))

        # Update the service entry
        db.child("user_services").child(uid).child(key).update(updates, token)
        updated = db.child("user_services").child(uid).child(key).get(token).val()
        print("✅ After update:", updated)

    except Exception as e:
        import traceback
        print("❌ Update status error:", e)
        traceback.print_exc()

    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if 'uid' not in session:
        return redirect(url_for('login_page'))

    uid = session['uid']
    name = session['user'].split('@')[0].capitalize()
    token = session.get('token')
    cart_data = {}
    total = 0

    try:
        # ✅ Refresh token
        if 'refresh_token' in session:
            refreshed = auth.refresh(session['refresh_token'])
            token = refreshed['idToken']
            session['token'] = token
            session['refresh_token'] = refreshed['refreshToken']

        # ✅ Fetch cart data
        cart_data = db.child("user_cart").child(uid).get(token).val() or {}

        for item in cart_data.values():
            qty = int(item.get('quantity', 1))
            price = int(item.get('price', 0))
            total += qty * price

        # ✅ Apply combo offer
        has_itr = has_gst = has_bookkeeping = False
        for item in cart_data.values():
            service = item.get('service', '').lower()
            if 'itr' in service:
                has_itr = True
            if 'gst' in service:
                has_gst = True
            if 'bookkeeping' in service:
                has_bookkeeping = True

        if has_itr and has_gst and has_bookkeeping:
            total = 2999

    except Exception as e:
        print("❌ Cart fetch error:", e)

    return render_template(
        'cart.html',
        user=session['user'],
        name=name,
        cart_data=cart_data,
        total=total,
        razorpay_key_id=RAZORPAY_KEY_ID  # 🔑 Passed to HTML for Razorpay checkout
    )

from flask import request, jsonify

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    number = request.form.get('number')
    message = request.form.get('message')

    print(f"📬 New Contact Submission:\nName: {name}\nEmail: {email}\nNumber: {number}\nMessage: {message}")

    # Validate fields
    if not name or not email or not number or not message:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    try:
        db.child("contact_messages").push({
            "name": name,
            "email": email,
            "number": number,
            "message": message
        })
        return jsonify({"success": True})
    except Exception as e:
        print("❌ Error saving contact message:", e)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    if 'uid' not in session:
        return redirect(url_for('login_page'))

    uid = session['uid']
    user = session['user']
    role = session['role']
    name = 'Mohan' if role == 'admin' else user.split('@')[0].split('.')[0].capitalize()

    try:
        if role == 'admin':
            contact_messages = db.child("contact_messages").get().val() or {}
            return render_template('dashboard.html', name=name, user=user, role=role, messages=contact_messages)
        else:
            user_services = db.child("user_services").child(uid).get(session['token']).val()
            return render_template('dashboard.html', name=name, user=user, role=role, user_services=user_services)
    except Exception as e:
        print("Dashboard fetch error:", e)
        return render_template('dashboard.html', name=name, user=user, role=role)

if __name__ == '__main__':
    app.run(debug=True)
=======
    return render_template('GST.html')

@app.route('/ITR.html')
def itr_page():
    return render_template('ITR.html')

@app.route('/TDS.html')
def tds_page():
    return render_template('TDS.html')
>>>>>>> 86b260f6abc041dbb2a062364de855e345938ce2
