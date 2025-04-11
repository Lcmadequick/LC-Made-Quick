import stripe
from flask import Flask, render_template, request, redirect
from config import Payment_buttons

app = Flask(__name__, static_folder='static', template_folder='templates')

stripe.api_key = 'Payment_buttons'  # Replace with your actual Stripe secret key

YOUR_DOMAIN = 'lcmadequick.com'  # Change this to your domain when live

@app.route('/')
def index():
    return render_template('index.html', title="Business Notes", description="Buy quality Leaving Cert notes")

@app.route('/create-checkout-session/<product_id>', methods=['POST'])
def create_checkout_session(product_id):
    product_map = {
        "management": {
            "name": "Business Management Notes",
            "price": 499,
            "file_url": "https://yourdomain.com/static/downloads/management_notes.pdf"
        },
        "marketing": {
            "name": "Marketing & Sales Notes",
            "price": 499,
            "file_url": "https://yourdomain.com/static/downloads/marketing_notes.pdf"
        },
        "accounting": {
            "name": "Accounting & Finance Notes",
            "price": 499,
            "file_url": "https://yourdomain.com/static/downloads/accounting_notes.pdf"
        }
    }

    product = product_map.get(product_id)

    if not product:
        return "Product not found", 404

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card', 'apple_pay'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'unit_amount': product["price"],
                'product_data': {
                    'name': product["name"],
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success',
        cancel_url=YOUR_DOMAIN + '/cancel',
    )

    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    return "<h1>Thank you for your purchase!</h1><p>Your download link will be emailed to you.</p>"

@app.route('/cancel')
def cancel():
    return "<h1>Payment cancelled</h1><p>No worries, come back anytime!</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5239, debug=True)
