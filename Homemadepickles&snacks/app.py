from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Login-required decorator ---
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return wrapper

# --- Login page shown first ---
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Dummy login check
        if username and password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('products'))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

# --- Signup page ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Save user to database (not implemented)
        flash('Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html")

# --- Forgot password page ---
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Handle password reset logic (not implemented)
        email = request.form.get('email')
        if not email:
            return render_template("forgot_password.html", error="Please enter your email.")
        flash('Password reset instructions sent to your email.', 'info')
        return redirect(url_for('login'))
    return render_template("forgot_password.html")

# --- Products page ---
@app.route('/products')
@login_required
def products():
    username = session.get('username')
    return render_template("products.html", username=username)

# --- Other pages ---
@app.route('/about')
@login_required
def about():
    return render_template("about.html")

@app.route('/contact')
@login_required
def contact():
    return render_template("contact.html")

@app.route('/reviews')
@login_required
def reviews():
    return render_template("reviews.html")

@app.route('/cart')
@login_required
def cart():
    cart_items = session.get('cart', [])
    total = sum(int(item['price']) for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

# --- Add to Cart ---
@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product = request.form['product']
    price = request.form['price']
    
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append({
        'product': product,
        'price': int(price)
    })
    
    return redirect(url_for('cart'))

# --- Checkout ---
@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if 'cart' in session:
        session.pop('cart')
    return "Thank you for your order!"

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)