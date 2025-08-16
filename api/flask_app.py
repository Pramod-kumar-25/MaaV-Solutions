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

@app.route('/ITR.html')
def itr_page():
    return render_template('ITR.html')

@app.route('/GST.html')
def gst_page():
    return render_template('GST.html')

@app.route('/TDS.html')
def tds_page():
    return render_template('TDS.html')

# Define the serverless function handler
def handler(request, response):
    # Set Flask's context to the request
    with app.request_context(request):
        # Dispatch the request to Flask
        app.preprocess_request()
        try:
            # Handle the request
            response = app.full_dispatch_request()
        except Exception as e:
            # Handle exceptions
            response = app.handle_exception(e)
        # Set Flask's context to the response
        app.process_response(response)
        return response
