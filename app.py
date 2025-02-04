from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session , send_from_directory , Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_ , DateTime , ForeignKey , Integer , String , Float , Text , Column
from datetime import datetime
from flask_migrate import Migrate
import os
import json
import requests
from uuid import uuid4
from werkzeug.utils import secure_filename
from models.bosta import BostaService
from datetime import datetime
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orfe-shop.sqlite3'
app.config['SECRET_KEY'] = 'secret-key'
app.config['FAWATERAK_API_KEY'] = 'a9e5325766195d9e5cb7a340da036646609e8c83690fb3678a'
app.config['FAWATERAK_API_URL'] = 'https://app.fawaterk.com/api/v2/createInvoiceLink'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'orfe-shop'
app.secret_key = 'secret-key'

# save sessiom 365 day 
app.config['PERMANENT_SESSION_LIFETIME'] = 365 * 24 * 60 * 60
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bosta_service = BostaService()


# products and  Category and Card and Order and OrderItem and adintiol images and adintiol data to prodect amd promo code
class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class Gusts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True) 
    address = db.Column(db.String(100), nullable=True)
    orders = db.relationship('Order', backref='guest', lazy=True)
    carts = db.relationship('Cart', backref='gust', lazy=True)  # This should work now
    last_activity = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    additional_images = db.relationship('AdditionalImage', backref='product', lazy=True)
    additional_data = db.relationship('AdditionalData', backref='product', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class AdditionalImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class AdditionalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('gusts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # إضافة العلاقة مع Product
    product = db.relationship('Product', backref='carts', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('gusts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    zone_id = db.Column(db.String(100))
    district_id = db.Column(db.String(100))
    business_reference = db.Column(db.String(50), unique=True)
    tracking_number = db.Column(db.String(100))
    shipping_status = db.Column(db.String(50), default='pending')
    cod_amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50), nullable=False)
    package_size = db.Column(db.String(20), default='SMALL')
    package_type = db.Column(db.String(20), default='Parcel')
    invoice_key = db.Column(db.String(100), nullable=True)
    invoice_id = db.Column(db.String(50), nullable=True)
    invoice_url = db.Column(db.String(200), nullable=True)
    payment_status = db.Column(db.String(20), default='pending', nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class PromoCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    session = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    session = db.Column(db.String(100), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
# shiping and city and zone and district and prices
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    zones = db.relationship('Zone', backref='city', lazy=True, foreign_keys='Zone.city_id')
    price = db.relationship('ShippingCost', backref='city', lazy=True, foreign_keys='ShippingCost.city_id')
    districts = db.relationship('District', backref='city', lazy=True, foreign_keys='District.city_id')
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id,
            'zones': [zone.serialize() for zone in self.zones],
            'districts': [district.serialize() for district in self.districts]
        }

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    zone_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'zone_id': self.zone_id
        }

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    district_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'district_id': self.district_id
        }

class ShippingCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# changShippingCostFromcity_idIsIdToCityId()

shop = Blueprint('shop', __name__)
admin = Blueprint('admin', __name__)

# check if user have session or not and if not create new session for him time 365 day and save it in db
def check_session():
    if 'session' not in session:
        session['session'] = os.urandom(24).hex()  # أفضل استخدام hex بدلًا من bytes
        session['cart_count'] = 0
        new_gest = Gusts(session=session['session'])
        db.session.add(new_gest)
        db.session.commit()
    else:
        gest = Gusts.query.filter_by(session=session['session']).first()
        if gest:
            cart_count = Cart.query.filter_by(user_id=gest.id).count()
            session['cart_count'] = cart_count
            gest.last_activity = datetime.utcnow()
            db.session.commit()
        else:
            # Handle orphaned session
            session.clear()
            session['session'] = os.urandom(24).hex()
            session['cart_count'] = 0
            new_gest = Gusts(session=session['session'])
            db.session.add(new_gest)
            db.session.commit()
@app.before_request
def before_request():
    check_session()
    session.permanent = True
    session.modified = True
@app.template_filter('currency')
def currency_format(value):
    return f"{value:,.2f} ج.م"

@app.template_filter('date_format')
def date_format(value):
    return value.strftime('%Y-%m-%d %I:%M %p')
@shop.route('/')
def home():

    check_session()
    categories = Category.query.all()
    last_products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    trending_products = Product.query.order_by(Product.views.desc()).limit(8).all()
    return render_template("shop/index.html", 
                           last_products=last_products, 
                           most_viewed=trending_products,
                           section_id="featured-products",
                           section_title="Our Featured Products",
                           products=last_products)

from sqlalchemy import or_
@shop.route('/shop')
def list():
    page = request.args.get('page', 1, type=int)  # Current page
    per_page = request.args.get('per_page', 9, type=int)  # Items per page
    sort = request.args.get('sort', 'default')  # Sorting option
    search = request.args.get('search', '')  # Search query
    category = request.args.get('category', '')  # Category filter
    price = request.args.get('price', '')  # Price range filter

    # Base query
    query = Product.query

    # Apply filters
    if search:
      query = query.filter(or_(
        Product.name.ilike(f'%{search}%'),
        Product.description.ilike(f'%{search}%')
      ))
    if category:
      query = query.filter(Product.category_id == category)
    if price:
      min_price, max_price = map(float, price.split('-'))
      query = query.filter(Product.price.between(min_price, max_price))

    # Apply sorting
    if sort == 'name-asc':
      query = query.order_by(Product.name.asc())
    elif sort == 'name-desc':
      query = query.order_by(Product.name.desc())
    elif sort == 'price-asc':
      query = query.order_by(Product.price.asc())
    elif sort == 'price-desc':
      query = query.order_by(Product.price.desc())
    elif sort == 'rating-asc':
      query = query.order_by(Product.rating.asc())
    elif sort == 'rating-desc':
      query = query.order_by(Product.rating.desc())
    elif sort == 'model-asc':
      query = query.order_by(Product.model.asc())
    elif sort == 'model-desc':
      query = query.order_by(Product.model.desc())
    else:
      query = query.order_by(Product.created_at.desc())

    # Pagination
    paginated_products = query.paginate(page=page, per_page=per_page, error_out=False)
    products = paginated_products.items

    # Get all categories for the sidebar
    categories = Category.query.all()

    # Render the template with filtered products and pagination data
    return render_template('shop/shop.html', 
                  products=products, 
                  categories=categories, 
                  pagination=paginated_products,
                  current_filters={
                    'sort': sort,
                    'search': search,
                    'category': category,
                    'price': price
                  })
    
@shop.route('/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    additional_images = AdditionalImage.query.filter_by(product_id=product_id).all()
    additional_data = AdditionalData.query.filter_by(product_id=product_id).all()
    product.views += 1
    db.session.commit()
    random_products = Product.query.order_by(db.func.random()).limit(6).all()
    return render_template('shop/product.html', product=product, additional_images=additional_images, additional_data=additional_data, products=random_products)
@shop.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > product.stock:
        flash('الكمية المطلوبة غير متوفرة في المخزون', 'danger')
        return redirect(url_for('shop.product', product_id=product_id))
    
    user = Gusts.query.filter_by(session=session['session']).first()
    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
    
    if cart_item:
        if (cart_item.quantity + quantity) > product.stock:
            flash('لا يمكن إضافة هذه الكمية، المخزون غير كافي', 'danger')
            return redirect(url_for('shop.cart'))
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user.id, product_id=product_id, quantity=quantity)
    
    db.session.add(cart_item)
    db.session.commit()
    flash('تمت إضافة المنتج إلى السلة بنجاح!', 'success')
    
    # Redirect to cart if "Add to Cart & Checkout" is clicked
    if 'add-to-cart-checkout' in request.form:
        return redirect(url_for('shop.cart'))
    
    return redirect(url_for('shop.product', product_id=product_id))

@shop.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    user = Gusts.query.filter_by(session=session['session']).first()
    cart_item = Cart.query.get_or_404(item_id)
    product = Product.query.get_or_404(cart_item.product_id)
    
    new_quantity = request.json.get('quantity')
    
    if not (1 <= new_quantity <= product.stock):
        return jsonify({
            'success': False,
            'message': f'الكمية يجب أن تكون بين 1 و {product.stock}'
        }), 400
    
    cart_item.quantity = new_quantity
    db.session.commit()
    
    return jsonify({
        'success': True,
        'new_total': product.price * new_quantity,
        'new_subtotal': sum(item.product.price * item.quantity for item in user.carts)
    })

@shop.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    user = Gusts.query.filter_by(session=session['session']).first()
    cart_item = Cart.query.filter_by(id=item_id, user_id=user.id).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('تم حذف المنتج من السلة', 'success')
    return redirect(url_for('shop.cart'))

@shop.route('/checkout')
def checkout():
    user = Gusts.query.filter_by(session=session['session']).first()
    cart_items = Cart.query.filter_by(user_id=user.id).all()

    if not cart_items:
        return redirect(url_for('shop.cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)
    cities = City.query.all()

    return render_template('shop/checkout.html', 
                         cart_items=cart_items,
                         total=total,
                         cities=cities)
from uuid import uuid4
def handle_fawaterak_payment(order):
    customer_name = order.name.strip().split(maxsplit=1)
    first_name = customer_name[0]
    last_name = customer_name[1] if len(customer_name) > 1 else 'N/A'

    if not all([first_name, last_name, order.phone]):
        flash('البيانات الأساسية للعميل غير مكتملة', 'danger')
        return redirect(url_for('shop.checkout'))

    cart_items = []
    cart_total = 0.0

    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    for item in order_items:
        product = Product.query.get(item.product_id)
        if product:
            try:
                price = float(product.price)
                quantity = int(item.quantity)
            except (ValueError, TypeError):
                flash('خطأ في بيانات المنتج', 'danger')
                return redirect(url_for('shop.checkout'))

            cart_items.append({
                "name": product.name[:255],
                "price": str(round(price, 2)),
                "quantity": str(quantity)
            })
            cart_total += price * quantity

    if not cart_items:
        flash('سلة التسوق فارغة', 'danger')
        return redirect(url_for('shop.checkout'))

    payload = {
        "cartTotal": str(round(cart_total, 2)),
        "currency": "EGP",
        "customer": {
            "first_name": first_name[:50],
            "last_name": last_name[:50],
            "email": order.email or "no-email@example.com",
            "phone": ''.join(filter(str.isdigit, order.phone))[:15],
            "address": order.address[:100] if order.address else "N/A"
        },
        "redirectionUrls": {
            "successUrl": url_for('shop.payment_success', order_id=order.id, _external=True),
            "failUrl": url_for('shop.payment_fail', order_id=order.id, _external=True),
            "pendingUrl": url_for('shop.payment_pending', order_id=order.id, _external=True),
            "webhookUrl": url_for('shop.payment_webhook', _external=True)
        },
        "cartItems": cart_items,
        "sendEmail": False,
        "sendSMS": False
    }

    headers = {
        'Authorization': f'Bearer {app.config["FAWATERAK_API_KEY"]}',
        'Content-Type': 'application/json'
    }

    app.logger.debug("Fawaterak Payload:")
    app.logger.debug(json.dumps(payload, indent=2))

    response = requests.post(
        app.config['FAWATERAK_API_URL'],
        headers=headers,
        json=payload,
        timeout=10
    )

    print(response.text)
    if not response.ok:
        app.logger.error(f"Fawaterak API Error: {response.status_code} - {response.text}")
        response.raise_for_status()

    fawaterak_data = response.json()
    if fawaterak_data.get('status') != 'success':
        app.logger.error(f"Fawaterak API Error: {fawaterak_data}")
        flash('فشل في إنشاء فاتورة الدفع', 'danger')
        return redirect(url_for('shop.checkout'))

    order.invoice_key = fawaterak_data['data']['invoiceKey']
    order.invoice_id = fawaterak_data['data']['invoiceId']
    order.invoice_url = fawaterak_data['data']['url']
    db.session.commit()

    return redirect(fawaterak_data['data']['url'])

@shop.route('/checkout/place_order', methods=['POST'])
def place_order():
        required_fields = ['name', 'phone', 'address', 'city', 'zone_id', 'district_id', 'total', 'payment_method']
        for field in required_fields:
            if field not in request.form:
                flash(f'الحقل {field} مطلوب', 'danger')
                return redirect(url_for('shop.checkout'))

        user = Gusts.query.filter_by(session=session['session']).first()
        cart_items = Cart.query.filter_by(user_id=user.id).all()

        if not cart_items:
            flash('سلة التسوق فارغة', 'danger')
            return redirect(url_for('shop.cart'))

        payment_method = request.form['payment_method']
        if payment_method not in ['cash_on_delivery', 'vodafone_cash', 'visa']:
            flash('طريقة الدفع المختارة غير متاحة', 'danger')
            return redirect(url_for('shop.checkout'))

        shipping_cost = ShippingCost.query.filter_by(city_id=request.form['city']).first()
        if not shipping_cost:
            flash('تكلفة الشحن غير متوفرة لهذه المدينة', 'danger')
            return redirect(url_for('shop.checkout'))

        total_amount = float(request.form['total']) + shipping_cost.price

        order = Order(
            user_id=user.id,
            name=request.form['name'],
            email=request.form.get('email', 'test@gmail.com'),
            phone=request.form['phone'],
            address=request.form['address'],
            city=request.form['city'],
            zone_id=request.form['zone_id'],
            district_id=request.form['district_id'],
            cod_amount=total_amount,
            payment_method=payment_method,
            status='pending'
        )

        if payment_method == 'visa':
            db.session.add(order)
            db.session.commit()
            return handle_fawaterak_payment(order)

        db.session.add(order)
        db.session.commit()

        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)
            db.session.delete(cart_item)

        db.session.commit()

        flash('تم إنشاء الطلب بنجاح!', 'success')
        return redirect(url_for('shop.order_confirmation', order_id=order.id))

# order_confirmation
@shop.route('/order_confirmation')
def order_confirmation():
    # get gusts session
    user = Gusts.query.filter_by(session=session['session']).first()
    # get order by user id
    order = Order.query.filter_by(user_id=user.id).first()
    # get order items by order id
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    for item in order_items:
        product = Product.query.get(item.product_id)
        item.product = product
    return render_template('shop/order_confirmation.html', order=order, order_items=order_items)

# order_detail
@shop.route('/order_detail')
def order_detail():
    # get gusts session
    user = Gusts.query.filter_by(session=session['session']).first()
    # get order by user id
    order = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).first()
    # get order items by order id
    shipping_cost = ShippingCost.query.filter_by(city_id=order.city).first()
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    for item in order_items:
        product = Product.query.get(item.product_id)
        item.product = product
    productsPrice = 0 
    for item in order_items:
        productsPrice += item.product.price * item.quantity
    return render_template('shop/order_detail.html', order=order, order_items=order_items , shipping_cost=shipping_cost ,productsPrice=productsPrice)
@shop.route('/payment/success/<int:order_id>')
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    order.payment_status = 'paid'
    db.session.commit()

    user = Gusts.query.filter_by(session=session['session']).first()
    Cart.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    return render_template('shop/payment_success.html', order=order)


@shop.route('/payment/fail/<int:order_id>')
def payment_fail(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return render_template('shop/payment_fail.html', order=order)


@shop.route('/payment/pending/<int:order_id>')
def payment_pending(order_id):
    order = Order.query.get_or_404(order_id)
    order.payment_status = 'pending'
    db.session.commit()
    return render_template('shop/payment_pending.html', order=order)


@shop.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    try:
        data = request.get_json()
        invoice_key = data.get('invoiceKey')
        status = data.get('status')

        order = Order.query.filter_by(invoice_key=invoice_key).first()
        if order:
            order.payment_status = status
            if status == 'paid':
                user = Gusts.query.get(order.user_id)
                Cart.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            return jsonify({'status': 'success'}), 200

        return jsonify({'status': 'error', 'message': 'Order not found'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@shop.route('/api/cities')
def get_cities():
    cities = City.query.all()
    return jsonify(city=[city.serialize() for city in cities])

# /api/zones?city_id=
@shop.route('/api/zones')
def get_zones():
    city_id = request.args.get('city_id')
    zones = Zone.query.filter_by(city_id=city_id).all()
    return jsonify(zones=[zone.serialize() for zone in zones])

# /api/districts?city_id=
@shop.route('/api/districts')
def get_districts():
    city_id = request.args.get('city_id')
    districts = District.query.filter_by(city_id=city_id).all()
    return jsonify(districts=[district.serialize() for district in districts])

@shop.route('/api/shipping-cost')
def get_shipping_cost():    

    city_id = request.args.get('city_id')
    shipping_cost = ShippingCost.query.filter_by(city_id=city_id).first()

    if shipping_cost is None:
        return jsonify(error="Shipping cost not found"), 404  # Return error response

    return jsonify(cost=shipping_cost.price)

@shop.route('/cart')
def cart():
    user = Gusts.query.filter_by(session=session['session']).first()
    # Change the query to use correct relationship between Cart and Product
    cart_query_result = db.session.query(Cart, Product).join(Product).filter(Cart.user_id == user.id).all()
    total = sum(item.Product.price * item.Cart.quantity for item in cart_query_result)
    cart_items = [
        {
            'id': item.Cart.id,
            'product': item.Product, 
            'quantity': item.Cart.quantity
        } for item in cart_query_result
    ]
    return render_template('shop/cart.html', cart_items=cart_items, total=total)
# chang-quantity/plus/1
@shop.route('/cart/change-quantity/<action>/<int:item_id>')
def change_quantity(action, item_id):
    user = Gusts.query.filter_by(session=session['session']).first()
    cart_item = Cart.query.filter_by(id=item_id, user_id=user.id).first_or_404()
    
    if action == 'plus':
        cart_item.quantity += 1
    elif action == 'minus':
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.quantity = 1
    
    db.session.commit()
    return redirect(url_for('shop.cart'))
# admin log in
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        is_admin_created = Admins.query.first()
        if not is_admin_created:
            new_admin = Admins(
                name='Admin',
                email="orfecosmetics@gmail.com",
                password="Orfe196196",
            )
            db.session.add(new_admin)
            db.session.commit()
            flash('تم إنشاء حساب المشرف بنجاح!', 'success')
        email = request.form['username']
        password = request.form['password']
        admin = Admins.query.filter_by(email=email, password=password).first()
        if admin:
            session['admin'] = admin.id
            admin.last_login = datetime.utcnow()
            db.session.commit()
            return redirect("/admin")
        flash('البريد الإلكتروني أو كلمة المرور غير صحيحة', 'danger')
    return render_template('admin/login.html')
# ...existing code...
from functools import wraps
from datetime import timedelta
# ...existing code...
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/logout')
def logout():
    session.pop('admin')
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin_required
def home():
    products_count = Product.query.count()
    orders_count = Order.query.count()
    customers_count = Gusts.query.count()
    total_revenue = db.session.query(db.func.sum(Order.cod_amount)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.id.desc()).limit(20).all()
    
    # Generate chart data
    # Calculate orders chart data
    orders_chart = {
        'labels': [],
        'data': []
    }
    for i in range(10):
        date = datetime.utcnow() - timedelta(days=i)
        orders_count = Order.query.filter(Order.created_at >= date).count()
        orders_chart['labels'].append(date.strftime('%Y-%m-%d'))
        orders_chart['data'].append(orders_count)

    # Calculate revenue chart data
    revenue_chart = {
        'labels': [],
        'data': []
    }
    for i in range(6):
        date = datetime.utcnow() - timedelta(days=i*30)
        revenue = db.session.query(db.func.sum(Order.cod_amount)).filter(Order.created_at >= date).scalar() or 0
        revenue_chart['labels'].append(date.strftime('%B'))
        revenue_chart['data'].append(revenue)
    
    return render_template('admin/index.html',
                         products_count=products_count,
                         orders_count=orders_count,
                         customers_count=customers_count,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         orders_chart=orders_chart,
                         revenue_chart=revenue_chart)



@admin.route('/add_product', methods=['POST'])
@admin_required
def add_product():
    try:
        # التحقق من الحقول المطلوبة
        if 'name' not in request.form or not request.form['name'].strip():
            flash('اسم المنتج مطلوب', 'error')
            return redirect(request.referrer)
            
        # معالجة البيانات الأساسية
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        price = float(request.form.get('price', 0))
        discount = float(request.form.get('discount', 0))
        stock = int(request.form.get('quantity', 0))
        category_id = int(request.form.get('category', 0))
        
        # التحقق من صحة البيانات
        if price <= 0:
            flash('السعر يجب أن يكون أكبر من صفر', 'error')
            return redirect(request.referrer)
            
        if stock < 0:
            flash('الكمية غير صالحة', 'error')
            return redirect(request.referrer)
            
        if discount < 0 or discount > 100:
            flash('نسبة الخصم يجب أن تكون بين 0 و 100', 'error')
            return redirect(request.referrer)

        # معالجة الصورة الرئيسية
        if 'image' not in request.files:
            flash('الصورة الرئيسية مطلوبة', 'error')
            return redirect(request.referrer)
            
        image_file = request.files['image']
        if image_file.filename == '':
            flash('لم يتم اختيار صورة رئيسية', 'error')
            return redirect(request.referrer)
            
        if not allowed_file(image_file.filename):
            flash('نوع الملف غير مسموح به للصورة الرئيسية', 'error')
            return redirect(request.referrer)
            
        main_image_filename = save_uploaded_file(image_file)

        # إنشاء المنتج
        new_product = Product(
            name=name,
            description=description,
            price=price,
            discount=discount,
            stock=stock,
            image=main_image_filename,
            category_id=category_id
        )
        db.session.add(new_product)
        db.session.commit()

        # معالجة الصور الإضافية
        additional_images = request.files.getlist('additional_images')
        for file in additional_images:
            if file and allowed_file(file.filename):
                filename = save_uploaded_file(file)
                additional_image = AdditionalImage(
                    image=filename,
                    product_id=new_product.id
                )
                db.session.add(additional_image)

        db.session.commit()
        flash('تمت إضافة المنتج بنجاح!', 'success')
        return redirect(url_for('admin.products'))

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding product: {str(e)}')
        flash('حدث خطأ أثناء إضافة المنتج، الرجاء المحاولة مرة أخرى', 'error')
        return redirect(request.referrer)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{uuid4().hex}_{file.filename}")
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return filename
    return None

@admin.route('/add_category', methods=['POST'])
@admin_required
def add_category():
    try:
        name = request.form['name']
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('تمت إضافة القسم بنجاح!', 'success')
        return redirect(request.referrer)

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash('حدث خطأ أثناء إضافة القسم!', 'error')
        return redirect(request.referrer)

@admin.route('/products')
@admin_required
def products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=products, categories=categories)

@admin.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    additional_images = AdditionalImage.query.filter_by(product_id=product_id).all()
    additional_data = AdditionalData.query.filter_by(product_id=product_id).all()
    for image in additional_images:
        db.session.delete(image)
    for data in additional_data:
        db.session.delete(data)

    db.session.delete(product)
    db.session.commit()
    flash('تم حذف المنتج بنجاح!', 'success')
    return redirect(url_for('admin.products'))

@admin.route('/edit_product/<int:product_id>', methods=['POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        if 'name' in request.form and request.form['name']:
            product.name = request.form['name']
        if 'description' in request.form and request.form['description']:
            product.description = request.form['description']
        if 'price' in request.form and request.form['price']:
            product.price = float(request.form['price'])
        if 'discount' in request.form and request.form['discount']:
            product.discount = float(request.form['discount'])
        if 'quantity' in request.form and request.form['quantity']:
            product.stock = int(request.form['quantity'])
        if 'category' in request.form and request.form['category']:
            product.category_id = int(request.form['category'])

        # Handle Image Upload
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            product.image = image_path

        db.session.commit()
        flash('تم تعديل المنتج بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash('حدث خطأ أثناء تعديل المنتج!', 'error')
    return redirect(url_for('admin.products'))

@admin.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin.route('/delete_category/<int:category_id>', methods=['POST'])
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('تم حذف القسم بنجاح!', 'success')
    return redirect(url_for('admin.categories'))

@admin.route('/edit_category/<int:category_id>', methods=['POST'])
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    try:
        if 'name' in request.form and request.form['name']:
            category.name = request.form['name']
        db.session.commit()
        flash('تم تعديل القسم بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash('حدث خطأ أثناء تعديل القسم!', 'error')
    return redirect(url_for('admin.categories'))

@admin.route('/shipping')
@admin_required
def shipping():
    # shipping price valedat and if city dosent have a chiping price he make it 100
    
    cities = City.query.all()
    for city in cities:
        if not city.price:
            shipping_cost = ShippingCost(city_id=city.id, price=100)
            db.session.add(shipping_cost)
    db.session.commit()
    cities = City.query.all()
    return render_template('admin/shipping.html', cities=cities)
# update shipping cost
@admin.route('/update_shipping_cost', methods=['POST'])
@admin_required
def update_shipping_cost():
    city_id = request.form['city_id']
    price = float(request.form['price'])
    city = City.query.get(city_id)
    city.price[0].price = price
    db.session.commit()
    flash('تم تحديث تكلفة الشحن بنجاح!', 'success')
    return redirect(url_for('admin.shipping'))

@admin.route('/orders')
@admin_required
def orders():
    orders = Order.query.all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/order/<int:order_id>')
@admin_required
def order_detail(order_id):
    # Get the order record or return a 404 if not found
    order = Order.query.get_or_404(order_id)
    
    # Perform a left outer join between OrderItem and Product.
    # This returns a list of tuples: (order_item, product) where product can be None.
    order_items_with_product = (
        db.session.query(OrderItem, Product)
        .outerjoin(Product, OrderItem.product_id == Product.id)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    # Transform the joined data into a list of dictionaries.
    # If product is None, default name and price to "غير معروف".
    order_items = []
    for order_item, product in order_items_with_product:
        item_data = {
            'order_item': order_item,
            'product': {
                'id': product.id if product else None,
                'image': product.image if product else url_for('static', filename='images/default.jpg'),
                'name': product.name if product else "غير معروف",
                'price': product.price if product else "غير معروف"
            }
        }
        order_items.append(item_data)

    return render_template('admin/order.html', order=order, order_items=order_items)
@admin.route('/payment-gateways')
def payment_gateways():
    # يمكنك إضافة منطق إضافي هنا إذا لزم الأمر
    return render_template('admin/payment_gateways.html')
@admin.route('/order/<int:order_id>/ship', methods=['POST'])
def ship_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.shipping_status != 'pending':
        flash('تم شحن هذا الطلب بالفعل', 'error')
# ... (بقية استيرادات الفلاسك والنماذج السابقة)

@admin.route('/add_city', methods=['POST'])
@admin_required
def add_city():
    try:
        name = request.form['name']
        city_id = request.form['city_id']
        
        # التحقق من عدم تكرار المدينة
        existing_city = City.query.filter_by(city_id=city_id).first()
        if existing_city:
            flash('هذه المدينة مسجلة مسبقاً!', 'error')
            return redirect(url_for('admin.shipping'))
        
        new_city = City(name=name, city_id=city_id)
        db.session.add(new_city)
        
        # إضافة سعر شحن افتراضي
        default_shipping = ShippingCost(city=new_city, price=100)
        db.session.add(default_shipping)
        
        db.session.commit()
        flash('تمت إضافة المدينة بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error adding city: {e}")
        flash('حدث خطأ أثناء إضافة المدينة', 'error')
    return redirect(url_for('admin.shipping'))

@admin.route('/delete_city/<int:id>')
@admin_required
def delete_city(id):
    try:
        city = City.query.get_or_404(id)
        
        # حذف كل ما يرتبط بالمدينة
        ShippingCost.query.filter_by(city_id=id).delete()
        Zone.query.filter_by(city_id=id).delete()
        District.query.filter_by(city_id=id).delete()
        
        db.session.delete(city)
        db.session.commit()
        flash('تم حذف المدينة بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting city: {e}")
        flash('حدث خطأ أثناء حذف المدينة', 'error')
    return redirect(url_for('admin.shipping'))

@admin.route('/add_zone/<int:city_id>', methods=['POST'])
@admin_required
def add_zone(city_id):
    try:
        data = request.get_json()
        zone_name = data['name']
        
        city = City.query.get_or_404(city_id)
        
        # إنشاء معرف فريد للمنطقة
        new_zone = Zone(
            name=zone_name,
            city_id=city.id,
            zone_id=f"ZONE-{datetime.now().timestamp()}"
        )
        
        db.session.add(new_zone)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'zone': new_zone.serialize()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding zone: {e}")
        return jsonify({'status': 'error', 'message': 'فشل في إضافة المنطقة'}), 500

@admin.route('/delete_zone/<int:zone_id>', methods=['DELETE'])
@admin_required
def delete_zone(zone_id):
    try:
        zone = Zone.query.get_or_404(zone_id)
        db.session.delete(zone)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting zone: {e}")
        return jsonify({'status': 'error', 'message': 'فشل في حذف المنطقة'}), 500

@admin.route('/add_district/<int:city_id>', methods=['POST'])
@admin_required
def add_district(city_id):
    try:
        data = request.get_json()
        district_name = data['name']
        
        city = City.query.get_or_404(city_id)
        
        # إنشاء معرف فريد للحي
        new_district = District(
            name=district_name,
            city_id=city.id,
            district_id=f"DIST-{datetime.now().timestamp()}"
        )
        
        db.session.add(new_district)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'district': new_district.serialize()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding district: {e}")
        return jsonify({'status': 'error', 'message': 'فشل في إضافة الحي'}), 500

@admin.route('/delete_district/<int:district_id>', methods=['DELETE'])
@admin_required
def delete_district(district_id):
    try:
        district = District.query.get_or_404(district_id)
        db.session.delete(district)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting district: {e}")
        return jsonify({'status': 'error', 'message': 'فشل في حذف الحي'}), 500

# ... (بقية الروتات)
app.register_blueprint(shop)
app.register_blueprint(admin , url_prefix='/admin')
@app.errorhandler(404)
def page_not_found(e):
    return render_template("shop/400.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("shop/500.html"), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
