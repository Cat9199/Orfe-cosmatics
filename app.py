from flask import Flask, request, jsonify , render_template , redirect , url_for , flash , session , blueprints
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

from werkzeug.utils import secure_filename

# this is a shop for cosmatics prand with name orfe
app = Flask(__name__ , template_folder='templates' , static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orfe-shop.sqlite3'
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'orfe-shop'
# save sessiom 365 day 
app.config['PERMANENT_SESSION_LIFETIME'] = 365 * 24 * 60 * 60
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

# products and  Category and Card and Order and OrderItem and adintiol images and adintiol data to prodect amd promo code

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
      product_id = db.Column(db.Integer, nullable=False)
      quantity = db.Column(db.Integer, nullable=False)
      created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
class Order(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100), nullable=False)
      email = db.Column(db.String(100), nullable=False)
      phone = db.Column(db.String(100), nullable=False)
      address = db.Column(db.String(100), nullable=False)
      status = db.Column(db.String(100), nullable=False)
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


shop = blueprints.Blueprint('shop', __name__)
admin = blueprints.Blueprint('admin', __name__)

@shop.route('/')
def home():
      # chek if user have session or not and if not create new session for him time 365 day and save it in db 
      if 'session' not in session:
            session['session'] = os.urandom(24)
            new_user = User(session=session['session'])
            db.session.add(new_user)
            db.session.commit()
      categories = Category.query.all()
      last_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
      most_viewed = Product.query.order_by(Product.views.desc()).limit(6).all()
      return render_template('shop/index.html', categories=categories, last_products=last_products, most_viewed=most_viewed)

@shop.route('/shop')
def list():
      products = Product.query.all()
      categories = Category.query.all()
      return render_template('shop/shop.html', products=products, categories=categories)
@shop.route('/<int:product_id>')
def product(product_id):
      product = Product.query.get_or_404(product_id)
      additional_images = AdditionalImage.query.filter_by(product_id=product_id).all()
      additional_data = AdditionalData.query.filter_by(product_id=product_id).all()
      product.views += 1
      db.session.commit()
      random_products = Product.query.order_by(db.func.random()).limit(6).all()
      return render_template('shop/product.html', product=product, additional_images=additional_images, additional_data=additional_data, random_products=random_products)

@shop.route('/cart')
def cart():
      return render_template('shop/cart.html')

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

app.register_blueprint(shop)
app.register_blueprint(admin , url_prefix='/admin')

if __name__ == '__main__':
      with app.app_context():
            db.create_all()
      app.run(debug=True)
