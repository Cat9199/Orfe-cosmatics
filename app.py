from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session , send_from_directory , Blueprint , send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_ , DateTime , ForeignKey , Integer , String , Float , Text , Column
from datetime import datetime, timedelta, timezone
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
import pandas as pd
from io import BytesIO

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

def cleanup_expired_cart_items():
    """Delete cart items older than 24 hours"""
    try:
        expiration_time = datetime.utcnow() - timedelta(hours=24)
        expired_items = Cart.query.filter(Cart.created_at < expiration_time).all()
        for item in expired_items:
            db.session.delete(item)
        db.session.commit()
    except Exception as e:
        app.logger.error(f'Error cleaning up expired cart items: {str(e)}')
        db.session.rollback()

def check_session():
    """
    Check and manage user session, including:
    - Session creation/validation
    - Cart cleanup
    - User activity tracking
    - Session expiration handling
    """
    try:
        # 1. Check if session exists
        if 'session' not in session:
            # Create new session
            session['session'] = os.urandom(24).hex()
            session['cart_count'] = 0
            new_guest = Gusts(
                session=session['session'],
                last_activity=datetime.utcnow()
            )
            db.session.add(new_guest)
            db.session.commit()
            return

        # 2. Get existing guest
        guest = Gusts.query.filter_by(session=session['session']).first()
        
        if guest:
            # 3. Update last activity
            guest.last_activity = datetime.utcnow()
            
            # 4. Clean up expired cart items
            cleanup_expired_cart_items()
            
            # 5. Update cart count
            cart_count = Cart.query.filter_by(user_id=guest.id).count()
            session['cart_count'] = cart_count
            
            # 6. Check for session expiration (30 days of inactivity)
            expiration_time = datetime.utcnow() - timedelta(days=30)
            if guest.last_activity < expiration_time:
                # Clear old cart items
                Cart.query.filter_by(user_id=guest.id).delete()
                # Create new session
                session.clear()
                session['session'] = os.urandom(24).hex()
                session['cart_count'] = 0
                new_guest = Gusts(
                    session=session['session'],
                    last_activity=datetime.utcnow()
                )
                db.session.add(new_guest)
                db.session.commit()
                return
                
            db.session.commit()
        else:
            # 7. Handle orphaned session
            session.clear()
            session['session'] = os.urandom(24).hex()
            session['cart_count'] = 0
            new_guest = Gusts(
                session=session['session'],
                last_activity=datetime.utcnow()
            )
            db.session.add(new_guest)
            db.session.commit()
            
    except Exception as e:
        app.logger.error(f'Error in check_session: {str(e)}')
        db.session.rollback()
        # Ensure session is valid even if there's an error
        if 'session' not in session:
            session['session'] = os.urandom(24).hex()
            session['cart_count'] = 0

@app.before_request
def before_request():
    check_session()
    cleanup_expired_cart_items()  # Clean up expired items on each request
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
    try:
        # Clean up expired items first
        cleanup_expired_cart_items()
        
        # Get product and validate
        product = Product.query.get_or_404(product_id)
        if not product.stock > 0:
            flash('المنتج غير متوفر حالياً', 'danger')
            return redirect(url_for('shop.product', product_id=product_id))
            
        # Validate and get quantity
        try:
            quantity = int(request.form.get('quantity', 1))
            if quantity < 1:
                raise ValueError("Quantity must be positive")
        except ValueError:
            flash('الكمية غير صالحة', 'danger')
            return redirect(url_for('shop.product', product_id=product_id))
        
        # Check stock availability
        if quantity > product.stock:
            flash('الكمية المطلوبة غير متوفرة في المخزون', 'danger')
            return redirect(url_for('shop.product', product_id=product_id))
        
        # Get or create user session
        user = Gusts.query.filter_by(session=session['session']).first()
        if not user:
            flash('حدث خطأ في جلسة المستخدم', 'danger')
            return redirect(url_for('shop.product', product_id=product_id))
        
        # Check if item exists in cart
        cart_item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
        
        if cart_item:
            # Update existing cart item
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                flash('لا يمكن إضافة هذه الكمية، المخزون غير كافي', 'danger')
                return redirect(url_for('shop.cart'))
            
            cart_item.quantity = new_quantity
            cart_item.created_at = datetime.utcnow()  # Reset the creation time
        else:
            # Create new cart item
            cart_item = Cart(
                user_id=user.id,
                product_id=product_id,
                quantity=quantity,
                created_at=datetime.utcnow()
            )
        
        # Save changes
        db.session.add(cart_item)
        db.session.commit()
        
        # Update session cart count
        session['cart_count'] = Cart.query.filter_by(user_id=user.id).count()
        
        flash('تمت إضافة المنتج إلى السلة بنجاح!', 'success')
        
        # Handle checkout redirect
        if 'add-to-cart-checkout' in request.form:
            return redirect(url_for('shop.cart'))
        
        return redirect(url_for('shop.product', product_id=product_id))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding item to cart: {str(e)}')
        flash('حدث خطأ أثناء إضافة المنتج إلى السلة', 'danger')
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
        flash('سلة التسوق فارغة', 'danger')
        return redirect(url_for('shop.cart'))

    total = sum(item.product.price * item.quantity for item in cart_items)
    cities = City.query.all()
    discount = 0
    
    # Calculate shipping conditions
    product_3_count = sum(item.quantity for item in cart_items if item.product_id == 3)
    shipping_conditions = {
        'product_3_count': product_3_count,
        'needs_for_free_shipping_3': max(0, 3 - product_3_count),
        'total': total,
        'needs_for_free_shipping_total': max(0, 405 - total)
    }

    # Check for special discount (products 1, 2, and 3)
    product_ids = [item.product_id for item in cart_items]
    if all(id in product_ids for id in [1, 2, 3]):
        discount = total * 0.30  # 30% discount
        total = total - discount
        flash('تهاني! حصلت على خصم 30% عند شراء المنتجات المميزة 🎉', 'success')
    elif total == 860:
        discount = total * 0.30  # 30% discount
        total = total - discount

    return render_template('shop/checkout.html', 
                         cart_items=cart_items, 
                         total=total, 
                         cities=cities, 
                         discount=discount,
                         shipping_conditions=shipping_conditions)

from uuid import uuid4


def handle_fawaterak_payment(order):
    customer_name = order.name.strip().split(maxsplit=1)
    first_name = customer_name[0]
    last_name = customer_name[1] if len(customer_name) > 1 else 'N/A'

    if not all([first_name, last_name, order.phone]):
        flash('البيانات الأساسية للعميل غير مكتملة', 'danger')
        return redirect(url_for('shop.checkout'))

    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    shipping_cost = ShippingCost.query.filter_by(city_id=order.city).first()
    
    if not shipping_cost:
        flash('تكلفة الشحن غير متوفرة لهذه المدينة', 'danger')
        return redirect(url_for('shop.checkout'))

    cart_items = []
    cart_total = 0.0

    # Add shipping cost to cart items and total
    shipping_price = float(shipping_cost.price)
    cart_items.append({
        "name": "Shipping Cost",
        "price": str(round(shipping_price, 2)),
        "quantity": "1"
    })
    cart_total += shipping_price

    # Add product items to cart items and total
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
            cart_total += round(price * quantity, 2)

    if not cart_items:
        flash('سلة التسوق فارغة', 'danger')
        return redirect(url_for('shop.checkout'))

    # Prepare the payload for Fawaterak
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

    try:
        response = requests.post(
            app.config['FAWATERAK_API_URL'],
            headers=headers,
            json=payload,
            timeout=10
        )

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

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Fawaterak API Request Failed: {e}")
        flash('فشل في الاتصال بخدمة الدفع، الرجاء المحاولة مرة أخرى', 'danger')
        return redirect(url_for('shop.checkout'))
    
@shop.route('/checkout/place_order', methods=['POST'])
def place_order():
    try:
        # 1. Validate required fields
        required_fields = ['name', 'phone', 'address', 'city', 'zone_id', 'district_id', 'total', 'payment_method']
        missing_fields = [field for field in required_fields if field not in request.form]
        if missing_fields:
            flash(f'الحقول التالية مطلوبة: {", ".join(missing_fields)}', 'danger')
            return redirect(url_for('shop.checkout'))

        # 2. Get user and validate cart
        user = Gusts.query.filter_by(session=session['session']).first()
        if not user:
            flash('حدث خطأ في جلسة المستخدم', 'danger')
            return redirect(url_for('shop.checkout'))

        cart_items = Cart.query.filter_by(user_id=user.id).all()
        if not cart_items:
            flash('سلة التسوق فارغة', 'danger')
            return redirect(url_for('shop.cart'))

        # 3. Validate payment method
        payment_method = request.form['payment_method']
        valid_payment_methods = ['cash_on_delivery', 'vodafone_cash', 'visa']
        if payment_method not in valid_payment_methods:
            flash('طريقة الدفع المختارة غير متاحة', 'danger')
            return redirect(url_for('shop.checkout'))

        # 4. Get and validate shipping cost
        shipping_cost = ShippingCost.query.filter_by(city_id=request.form['city']).first()
        if not shipping_cost:
            flash('تكلفة الشحن غير متوفرة لهذه المدينة', 'danger')
            return redirect(url_for('shop.checkout'))

        # 5. Calculate product total and validate stock
        try:
            product_total = float(request.form['total'])
        except ValueError:
            flash('قيمة الطلب غير صالحة', 'danger')
            return redirect(url_for('shop.checkout'))

        # 6. Check stock availability
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            if not product:
                flash(f'المنتج غير موجود', 'danger')
                return redirect(url_for('shop.cart'))
            
            if product.stock < cart_item.quantity:
                flash(f'الكمية المتاحة من {product.name} غير كافية', 'danger')
                return redirect(url_for('shop.cart'))

        # 7. Calculate shipping cost with special conditions
        shipping_price = shipping_cost.price
        
        # Check for free shipping conditions
        product_3_count = sum(item.quantity for item in cart_items if item.product_id == 3)
        if product_3_count >= 3:
            shipping_price = 0
            flash('تهاني! الشحن مجاني عند شراء 3 منتجات من المنتج رقم 3 🎉', 'success')
        elif product_total == 405:
            shipping_price = 0
            flash('تهاني! الشحن مجاني عند شراء منتجات بقيمة 405 جنيه 🎉', 'success')

        # 8. Calculate final total
        total_amount = product_total + shipping_price

        # 9. Create order
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

        # 10. Add order to session and commit to get the order ID
        db.session.add(order)
        db.session.commit()

        # 11. Create order items and update stock
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            order_item = OrderItem(
                order_id=order.id,  # Now we have the order ID
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)
            
            # Update product stock
            product.stock -= cart_item.quantity
            
            # Delete cart item
            db.session.delete(cart_item)

        # 12. Commit all changes
        db.session.commit()

        # 13. Handle payment method
        if payment_method == 'visa':
            return handle_fawaterak_payment(order)

        flash('تم إنشاء الطلب بنجاح!', 'success')
        return redirect(url_for('shop.order_confirmation', order_id=order.id))

    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error in place_order: {str(e)}')
        flash('حدث خطأ أثناء معالجة الطلب، الرجاء المحاولة مرة أخرى', 'danger')
        return redirect(url_for('shop.checkout'))

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
    all_last_orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).limit(10).all()
    cart_items = [
        {
            'id': item.Cart.id,
            'product': item.Product, 
            'quantity': item.Cart.quantity
        } for item in cart_query_result
    ]
    return render_template('shop/cart.html', cart_items=cart_items, total=total, all_last_orders=all_last_orders)
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
    total_shipping_cost = 0

    for order in Order.query.all():
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        product_total = sum(item.quantity * Product.query.get(item.product_id).price for item in order_items)
        shipping_cost = order.cod_amount - product_total
        total_shipping_cost += max(shipping_cost, 0)  # Ensure shipping cost is not negative

    total_revenue -= total_shipping_cost
    recent_orders = Order.query.order_by(Order.id.desc()).limit(20).all()

    # Generate chart data
    # Calculate orders chart data
    orders_chart = {
        'labels': [],
        'data': []
    }
    for _ in range(10):
        date = datetime.strptime("2021-06-01", '%Y-%m-%d')
        orders_count = Order.query.count()
        orders_chart['labels'].append(date.strftime('%Y-%m-%d'))
        orders_chart['data'].append(orders_count)

    # Calculate revenue chart data
    revenue_chart = {
        'labels': [],
        'data': []
    }
    for _ in range(6):
        date = datetime.strptime("2021-06-01", '%Y-%m-%d')
        revenue = db.session.query(db.func.sum(Order.cod_amount)).filter(Order.created_at >= date).scalar() or 0
        revenue_chart['labels'].append(date.strftime('%B'))
        revenue_chart['data'].append(revenue)

    return render_template('admin/index.html',
                            products_count=products_count,
                            orders_count=orders_count,
                            customers_count=customers_count,
                            total_revenue=total_revenue,
                            total_shipping_cost=total_shipping_cost,
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
        
        # Handle empty or invalid price
        price_str = request.form.get('price', '0').strip()
        try:
            price = float(price_str) if price_str else 0
        except ValueError:
            flash('السعر غير صالح', 'error')
            return redirect(request.referrer)
            
        # Handle empty or invalid discount
        discount_str = request.form.get('discount', '0').strip()
        try:
            discount = float(discount_str) if discount_str else 0
        except ValueError:
            flash('نسبة الخصم غير صالحة', 'error')
            return redirect(request.referrer)
            
        # Handle empty or invalid stock
        stock_str = request.form.get('quantity', '0').strip()
        try:
            stock = int(stock_str) if stock_str else 0
        except ValueError:
            flash('الكمية غير صالحة', 'error')
            return redirect(request.referrer)
            
        # Handle empty or invalid category
        category_str = request.form.get('category', '0').strip()
        try:
            category_id = int(category_str) if category_str else 0
        except ValueError:
            flash('التصنيف غير صالح', 'error')
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
    try:
        # Get all cities
        cities = City.query.all()
        
        # Ensure each city has a shipping cost
        for city in cities:
            shipping_cost = ShippingCost.query.filter_by(city_id=city.city_id).first()
            if not shipping_cost:
                shipping_cost = ShippingCost(city_id=city.city_id, price=100)
                db.session.add(shipping_cost)
        
        db.session.commit()
        return render_template('admin/shipping.html', cities=cities)
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error in shipping route: {str(e)}')
        flash('حدث خطأ أثناء تحميل صفحة الشحن', 'error')
        return redirect(url_for('admin.home'))

@admin.route('/delete_city/<int:id>')
@admin_required
def delete_city(id):
    try:
        city = City.query.get_or_404(id)
        
        # Delete associated shipping costs
        ShippingCost.query.filter_by(city_id=city.city_id).delete()
        
        # Delete associated zones
        Zone.query.filter_by(city_id=city.city_id).delete()
        
        # Delete associated districts
        District.query.filter_by(city_id=city.city_id).delete()
        
        # Delete the city
        db.session.delete(city)
        db.session.commit()
        
        flash('تم حذف المدينة بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting city: {str(e)}')
        flash('حدث خطأ أثناء حذف المدينة', 'error')
        
    return redirect(url_for('admin.shipping'))

@admin.route('/update_shipping_cost', methods=['POST'])
@admin_required
def update_shipping_cost():
    try:
        city_id = request.form.get('city_id')
        price = float(request.form.get('price', 0))
        
        if not city_id:
            flash('معرف المدينة مطلوب', 'error')
            return redirect(url_for('admin.shipping'))
            
        # Get or create shipping cost
        shipping_cost = ShippingCost.query.filter_by(city_id=city_id).first()
        if not shipping_cost:
            shipping_cost = ShippingCost(city_id=city_id, price=price)
            db.session.add(shipping_cost)
        else:
            shipping_cost.price = price
            
        db.session.commit()
        flash('تم تحديث تكلفة الشحن بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating shipping cost: {str(e)}')
        flash('حدث خطأ أثناء تحديث تكلفة الشحن', 'error')
        
    return redirect(url_for('admin.shipping'))

@admin.route('/orders')
@admin_required
def orders():
    try:
        # Get all orders with their details
        orders = Order.query.order_by(Order.id.desc()).all()
        
        # Add additional information to each order
        for order in orders:
            # Get city information
            city = City.query.filter_by(city_id=order.city).first()
            order.city_name = city.name if city else "غير معروف"
            
            # Get order items count
            order.items_count = OrderItem.query.filter_by(order_id=order.id).count()
            
            # Get shipping status display name
            shipping_statuses = {
                'pending': 'قيد الانتظار',
                'shipped': 'تم الشحن',
                'delivered': 'تم التوصيل',
                'cancelled': 'ملغي'
            }
            order.shipping_status_display = shipping_statuses.get(order.shipping_status, order.shipping_status)
            
            # Get payment status display name
            payment_statuses = {
                'pending': 'قيد الانتظار',
                'paid': 'تم الدفع',
                'failed': 'فشل الدفع',
                'refunded': 'تم الاسترجاع'
            }
            order.payment_status_display = payment_statuses.get(order.payment_status, order.payment_status)
            
            # Get payment method display name
            payment_methods = {
                'cash_on_delivery': 'الدفع عند الاستلام',
                'vodafone_cash': 'فودافون كاش',
                'visa': 'الدفع بالفيزا'
            }
            order.payment_method_display = payment_methods.get(order.payment_method, order.payment_method)
        
        return render_template('admin/orders.html', orders=orders)
        
    except Exception as e:
        app.logger.error(f'Error in orders route: {str(e)}')
        flash('حدث خطأ أثناء تحميل قائمة الطلبات', 'error')
        return redirect(url_for('admin.home'))

@admin.route('/order/<int:order_id>')
@admin_required
def order_detail(order_id):
    try:
        # Get the order record or return a 404 if not found
        order = Order.query.get_or_404(order_id)
        
        # Get city information
        city = City.query.filter_by(city_id=order.city).first()
        city_name = city.name if city else "غير معروف"
        
        # Get shipping cost
        shipping_cost = ShippingCost.query.filter_by(city_id=order.city).first()
        shipping_price = shipping_cost.price if shipping_cost else 0
        
        # Get order items with product details
        order_items_with_product = (
            db.session.query(OrderItem, Product)
            .join(Product, OrderItem.product_id == Product.id)
            .filter(OrderItem.order_id == order_id)
            .all()
        )
        
        # Calculate order totals
        subtotal = 0
        order_items = []
        for order_item, product in order_items_with_product:
            item_total = product.price * order_item.quantity
            subtotal += item_total
            
            item_data = {
                'order_item': order_item,
                'product': {
                    'id': product.id,
                    'image': product.image,
                    'name': product.name,
                    'price': product.price,
                    'stock': product.stock,
                    'category': product.category.name if product.category else "غير معروف"
                },
                'item_total': item_total
            }
            order_items.append(item_data)
        
        # Calculate final totals
        total_amount = subtotal + shipping_price
        
        # Get payment method display name
        payment_methods = {
            'cash_on_delivery': 'الدفع عند الاستلام',
            'vodafone_cash': 'فودافون كاش',
            'visa': 'الدفع بالفيزا'
        }
        payment_method_display = payment_methods.get(order.payment_method, order.payment_method)
        
        # Get shipping status display name
        shipping_statuses = {
            'pending': 'قيد الانتظار',
            'shipped': 'تم الشحن',
            'delivered': 'تم التوصيل',
            'cancelled': 'ملغي'
        }
        shipping_status_display = shipping_statuses.get(order.shipping_status, order.shipping_status)
        
        # Get payment status display name
        payment_statuses = {
            'pending': 'قيد الانتظار',
            'paid': 'تم الدفع',
            'failed': 'فشل الدفع',
            'refunded': 'تم الاسترجاع'
        }
        payment_status_display = payment_statuses.get(order.payment_status, order.payment_status)
        
        # Prepare order summary
        order_summary = {
            'subtotal': subtotal,
            'shipping_cost': shipping_price,
            'total_amount': total_amount,
            'items_count': len(order_items),
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': payment_method_display,
            'shipping_status': shipping_status_display,
            'payment_status': payment_status_display,
            'tracking_number': order.tracking_number or 'غير متوفر',
            'business_reference': order.business_reference or 'غير متوفر'
        }
        
        # Get all available products for adding new items
        available_products = Product.query.filter(Product.stock > 0).all()
        
        return render_template('admin/order.html',
                             order=order,
                             order_items=order_items,
                             order_summary=order_summary,
                             available_products=available_products,
                             city_name=city_name,
                             shipping_cost=shipping_cost)
                             
    except Exception as e:
        app.logger.error(f'Error in order_detail: {str(e)}')
        flash('حدث خطأ أثناء تحميل تفاصيل الطلب', 'error')
        return redirect(url_for('admin.orders'))

@admin.route('/add_item_to_order/<int:order_id>', methods=['POST'])
@admin_required
def add_item_to_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 1))
        
        if not product_id:
            flash('الرجاء اختيار منتج', 'error')
            return redirect(url_for('admin.order_detail', order_id=order_id))
            
        product = Product.query.get_or_404(product_id)
        
        # Validate stock
        if quantity > product.stock:
            flash('الكمية المطلوبة غير متوفرة في المخزون', 'error')
            return redirect(url_for('admin.order_detail', order_id=order_id))
            
        # Check if item already exists in order
        existing_item = OrderItem.query.filter_by(
            order_id=order_id,
            product_id=product_id
        ).first()
        
        if existing_item:
            # Update existing item
            existing_item.quantity += quantity
        else:
            # Create new item
            order_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(order_item)
        
        # Update order total
        order.cod_amount += product.price * quantity
        
        # Update product stock
        product.stock -= quantity
        
        db.session.commit()
        flash('تمت إضافة المنتج إلى الطلب بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding item to order: {str(e)}')
        flash('حدث خطأ أثناء إضافة المنتج إلى الطلب', 'error')
        
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin.route('/delete_item_from_order/<int:order_id>/<int:item_id>', methods=['POST'])
@admin_required
def delete_item_from_order(order_id, item_id):
    try:
        order_item = OrderItem.query.get_or_404(item_id)
        order = Order.query.get_or_404(order_id)
        product = Product.query.get_or_404(order_item.product_id)
        
        # Validate order item belongs to order
        if order_item.order_id != order_id:
            flash('عنصر الطلب غير موجود', 'error')
            return redirect(url_for('admin.order_detail', order_id=order_id))
        
        # Update order total
        order.cod_amount -= product.price * order_item.quantity
        
        # Restore product stock
        product.stock += order_item.quantity
        
        # Delete order item
        db.session.delete(order_item)
        db.session.commit()
        
        flash('تم حذف المنتج من الطلب بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting item from order: {str(e)}')
        flash('حدث خطأ أثناء حذف المنتج من الطلب', 'error')
        
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin.route('/update_shipping_status/<int:order_id>', methods=['POST'])
@admin_required
def update_shipping_status(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        status = request.form.get('status')
        
        if not status:
            flash('حالة الشحن مطلوبة', 'error')
            return redirect(url_for('admin.order_detail', order_id=order_id))
            
        valid_statuses = ['pending', 'shipped', 'delivered', 'cancelled']
        if status not in valid_statuses:
            flash('حالة الشحن غير صالحة', 'error')
            return redirect(url_for('admin.order_detail', order_id=order_id))
            
        order.shipping_status = status
        db.session.commit()
        
        flash('تم تحديث حالة الشحن بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating shipping status: {str(e)}')
        flash('حدث خطأ أثناء تحديث حالة الشحن', 'error')
        
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin.route('/delete_order/<int:order_id>', methods=['POST'])
@admin_required
def delete_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        
        # Restore product stock
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        for item in order_items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        
        # Delete order items
        OrderItem.query.filter_by(order_id=order_id).delete()
        
        # Delete order
        db.session.delete(order)
        db.session.commit()
        
        flash('تم حذف الطلب بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting order: {str(e)}')
        flash('حدث خطأ أثناء حذف الطلب', 'error')
        
    return redirect(url_for('admin.orders'))

@admin.route('/export_orders')
@admin_required
def export_orders():
    try:
        # Get all orders with their items
        orders = Order.query.all()
        
        data = []
        for order in orders:
            order_items = db.session.query(OrderItem, Product).join(Product, OrderItem.product_id == Product.id).filter(OrderItem.order_id == order.id).all()
            total_quantity = sum(item.OrderItem.quantity for item in order_items)
            product_names = ', '.join([item.Product.name for item in order_items if item.Product])
            city = City.query.filter_by(city_id=order.city).first()
            city_name = city.name if city else 'Unknown'
            
            # Prepare order data
            order_data = {
                'اسم العميل': order.name,
                'تليفون (محمول فقط)': order.phone,
                'المدينة': city_name,
                'المنطقة': order.zone_id,
                'العنوان': order.address,
                'قيمة التحصيل النقدي': order.cod_amount,
                'عدد القطع': total_quantity,
                'وصف الشحنة': product_names,
                'مرجع الطلب': order.business_reference or '',
                'قيمة الشحنة': order.cod_amount
            }
            data.append(order_data)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create the file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='الطلبات')
        
        output.seek(0)
        
        # Send the file as a response
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='الطلبات.xlsx'
        )
        
    except Exception as e:
        app.logger.error(f'Error exporting orders: {str(e)}')
        flash('حدث خطأ أثناء تصدير الطلبات', 'error')
        return redirect(url_for('admin.orders'))

@admin.route('/export_selected_orders', methods=['POST'])
@admin_required
def export_selected_orders():
    try:
        selected_order_ids = request.form.getlist('order_ids')
        if not selected_order_ids:
            flash('الرجاء اختيار طلبات للتصدير', 'error')
            return redirect(url_for('admin.orders'))
            
        order_ids = [int(order_id) for order_id in selected_order_ids]
        orders = Order.query.filter(Order.id.in_(order_ids)).all()
        
        data = []
        for order in orders:
            order_items = db.session.query(OrderItem, Product).join(Product, OrderItem.product_id == Product.id).filter(OrderItem.order_id == order.id).all()
            total_quantity = sum(item.OrderItem.quantity for item in order_items)
            product_names = ', '.join([item.Product.name for item in order_items if item.Product])
            city = City.query.filter_by(city_id=order.city).first()
            city_name = city.name if city else 'Unknown'
            
            # Prepare order data
            order_data = {
                'اسم العميل': order.name,
                'تليفون (محمول فقط)': order.phone,
                'المدينة': city_name,
                'المنطقة': order.zone_id,
                'العنوان': order.address,
                'قيمة التحصيل النقدي': order.cod_amount,
                'عدد القطع': total_quantity,
                'وصف الشحنة': product_names,
                'مرجع الطلب': order.business_reference or '',
                'قيمة الشحنة': order.cod_amount
            }
            data.append(order_data)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create the file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='الطلبات')
        
        output.seek(0)
        
        # Send the file as a response
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='الطلبات المحددة.xlsx'
        )
        
    except Exception as e:
        app.logger.error(f'Error exporting selected orders: {str(e)}')
        flash('حدث خطأ أثناء تصدير الطلبات المحددة', 'error')
        return redirect(url_for('admin.orders'))

@admin.route('/order/<int:order_id>/ship', methods=['POST'])
@admin_required
def ship_order(order_id):
    try:
        order = Order.query.get_or_404(order_id)
        
        # Check if order is already shipped
        if order.shipping_status == 'shipped':
            flash('تم شحن هذا الطلب بالفعل', 'warning')
            return redirect(url_for('admin.order_detail', order_id=order_id))
            
        # Check if order is cancelled
        if order.shipping_status == 'cancelled':
            flash('لا يمكن شحن طلب ملغي', 'error')
            return redirect(url_for('admin.order_detail', order_id=order_id))
            
        # Update shipping status
        order.shipping_status = 'shipped'
        
        # Generate tracking number if not exists
        if not order.tracking_number:
            order.tracking_number = f"TRK-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order.id}"
        
        # Generate business reference if not exists
        if not order.business_reference:
            order.business_reference = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{order.id}"
        
        db.session.commit()
        
        flash('تم تحديث حالة الشحن بنجاح!', 'success')
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error shipping order: {str(e)}')
        flash('حدث خطأ أثناء تحديث حالة الشحن', 'error')
        
    return redirect(url_for('admin.order_detail', order_id=order_id))

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

    app.run(debug=True,host='0.0.0.0',port=8765)

