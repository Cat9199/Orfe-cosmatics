from flask import Flask, request, jsonify , render_template , redirect , url_for , flash , session , blueprints ,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
from models.bosta import BostaService

from werkzeug.utils import secure_filename
bosta_service = BostaService()
# this is a shop for cosmatics prand with name orfe
app = Flask(__name__ , template_folder='templates' , static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orfe-shop.sqlite3'
app.config['SECRET_KEY'] = 'secret-key'
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
    orders = db.relationship('Order', backref='gust', lazy=True)
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
    user_id = db.Column(db.Integer, db.ForeignKey('gusts.id'), nullable=False)  # Add this line
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

shop = blueprints.Blueprint('shop', __name__)
admin = blueprints.Blueprint('admin', __name__)

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
    return redirect(url_for('shop.cart'))
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
    cities = bosta_service.get_cities()

    return render_template('shop/checkout.html', 
                         cart_items=cart_items,
                         total=total,
                         cities=cities)
from uuid import uuid4
@shop.route('/checkout/place_order', methods=['POST'])
def place_order():
    try:
        # التحقق من وجود الحقول المطلوبة
        required_fields = ['name', 'email', 'phone', 'address', 'city', 'zone_id', 'district_id', 'total', 'payment_method']
        for field in required_fields:
            if field not in request.form:
                flash(f'الحقل {field} مطلوب', 'danger')
                return redirect(url_for('shop.checkout'))

        user = Gusts.query.filter_by(session=session['session']).first()
        cart_items = Cart.query.filter_by(user_id=user.id).all()

        if not cart_items:
            flash('سلة التسوق فارغة', 'danger')
            return redirect(url_for('shop.cart'))

        # التحقق من طريقة الدفع
        payment_method = request.form['payment_method']
        if payment_method not in ['cash_on_delivery', 'vodafone_cash']:
            flash('طريقة الدفع المختارة غير متاحة', 'danger')
            return redirect(url_for('shop.checkout'))

        # إنشاء مرجع فريد للطلب
        business_ref = str(uuid4())[:8]

        # إنشاء سجل الطلب
        new_order = Order(
            user_id=user.id,
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            address=request.form['address'],
            city=request.form['city'],
            zone_id=request.form['zone_id'],
            district_id=request.form['district_id'],
            business_reference=business_ref,
            cod_amount=float(request.form['total']),
            payment_method=payment_method,  # حفظ طريقة الدفع
            status='pending'
        )

        db.session.add(new_order)
        db.session.commit()

        # إنشاء عناصر الطلب
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )
            db.session.add(order_item)
            db.session.delete(cart_item)

        db.session.commit()

        flash('تم إنشاء الطلب بنجاح!', 'success')
        return redirect(url_for('shop.order_confirmation', order_id=new_order.id))

    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ: {str(e)}', 'danger')
        return redirect(url_for('shop.checkout'))

@shop.route('/api/cities')
def get_cities():
    cities = BostaServiceget_cities()
    return jsonify(cities)

# /api/zones?city_id=
@shop.route('/api/zones')
def get_zones():
    city_id = request.args.get('city_id')
    zones = bosta_service.get_zones(city_id)
    return jsonify(zones)

# /api/districts?city_id=
@shop.route('/api/districts')
def get_districts():
    city_id = request.args.get('city_id')
    zones = bosta_service.get_districts(city_id)
    return jsonify(zones)

@shop.route('/api/shipping-cost')
def get_shipping_cost():    
    delivery_type = request.args.get('delivery_type')
    cod = request.args.get('cod')
    
    price = bosta_service.get_shipping_cost(city_id, zone_id, package_size, delivery_type, cod)
    return jsonify({'price': price})

@shop.route('/cart')
def cart():
    user = Gusts.query.filter_by(session=session['session']).first()
    # Change the query to use correct relationship between Cart and Product
    cart_query_result = db.session.query(Cart, Product).join(Product).filter(Cart.user_id == user.id).all()
    total = sum(item.Product.price * item.Cart.quantity for item in cart_query_result)
    cart_items = [
        {
            'product': item.Product,  # Product object from the join
            'quantity': item.Cart.quantity
        } for item in cart_query_result
    ]
    return render_template('shop/cart.html', cart_items=cart_items, total=total)

@admin.route('/')
def home():
    categories = Category.query.all()
    return render_template('admin/index.html', categories=categories)

@admin.route('/add_product', methods=['POST'])
def add_product():
    try:
      name = request.form['name']
      description = request.form['description']
      price = float(request.form['price'])
      discount = float(request.form.get('discount', 0))  # Optional
      stock = int(request.form['quantity'])
      category_id = int(request.form['category'])

      # Handle Main Product Image
      image_file = request.files['image']
      if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
      else:
        flash('الصورة الرئيسية مطلوبة!', 'error')
        return redirect(request.referrer)

      # Create Product
      new_product = Product(
        name=name,
        description=description,
        price=price,
        discount=discount,
        stock=stock,
        image=image_path,
        category_id=category_id
      )
      db.session.add(new_product)
      db.session.commit()

      # Handle Additional Images
      additional_images = request.files.getlist('additional_images')
      for file in additional_images:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Add image to AdditionalImage table
            additional_image = AdditionalImage(
              image=image_path,
              product_id=new_product.id
            )
            db.session.add(additional_image)

      db.session.commit()
      flash('تمت إضافة المنتج بنجاح!', 'success')
      return redirect(url_for('dashboard'))  # Update with your actual dashboard route

    except Exception as e:
      db.session.rollback()
      print(f"Error: {e}")
      flash('حدث خطأ أثناء إضافة المنتج!', 'error')
      return redirect(request.referrer)
@admin.route('/add_category', methods=['POST'])
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
def products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin/products.html', products=products, categories=categories)
@admin.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
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

# categories
@admin.route('/categories', methods=['GET', 'POST'])
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)
@admin.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('تم حذف القسم بنجاح!', 'success')
    return redirect(url_for('admin.categories'))
@admin.route('/edit_category/<int:category_id>', methods=['POST'])
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
# admin shipping
@admin.route('/shipping')
def shipping():
    return render_template('admin/shipping.html')
@admin.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/order/<int:order_id>')
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

app.register_blueprint(shop)
app.register_blueprint(admin , url_prefix='/admin')
@app.errorhandler(404)
def page_not_found(e):
    return render_template("shop/400.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    # Optionally, add: db.session.rollback() if you are using SQLAlchemy
    return render_template("500.html"), 500
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
