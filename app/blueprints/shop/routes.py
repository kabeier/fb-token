from app import db
from .import bp as shop
from flask import render_template, redirect, url_for, request, flash, session, jsonify, current_app as app
from .models import Product, Category, Cart
from app.blueprints.authentication.models import User
from flask_login import login_required, current_user
from datetime import datetime as dt
import stripe


@shop.route('/', methods=['GET'])
@login_required
def index():
    context = {
        'products': Product.query.all()
    }
    return render_template('shop/index.html', **context)

@shop.route('/checkout', methods=['POST'])
def checkout():
    stripe.api_key = app.config.get('STRIPE_SK_TEST')
    _display_cart = session.get('display_cart').values()
    display_cart = []
    for p in _display_cart:
        item_dict = {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(p['price']*100),
                        'product_data': {
                            'name': p['name'],
                            'images': [p['image']],
                        },
                    },
                    'quantity': p['quantity']
                }
        display_cart.append(item_dict)
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=display_cart,
        mode='payment',
        success_url='http://localhost:5000/shop/checkout/success',
        cancel_url=redirect(url_for('shop.checkout_fail')),
    )
    # try:
    #     return jsonify({'id': checkout_session.id})
    # except Exception as e:
    #     return jsonify(error=str(e)), 403
    flash("Payment handled successfully", 'success')
    return checkout_session

@shop.route('/checkout/success', methods=['GET'])
def checkout_success():
    return "Success"

@shop.route('/checkout/fail', methods=['GET'])
def checkout_fail():
    return "Fail"


@shop.route('/product', methods=['GET'])
@login_required
def single():
    product_id = request.args.get('id')

    context = {
        'p': Product.query.get(product_id)
    }
    return render_template('shop/single.html', **context)

@shop.route('/cart', methods=['GET'])
def show_cart():
    if current_user.is_anonymous:
        context ={ 'products': []}
    else:
        context = {
            'products': [Product.query.get(i.product_id) for i in Cart.query.filter_by(user_id=current_user.id).all()]
        }
    return render_template('shop/cart.html', **context)

@shop.route('/cart/remove', methods=['GET'])
def delete_from_cart():
    product_id = request.args.get('id')
    [db.session.delete(i) for i in Cart.query.filter_by(product_id=product_id).all()]
    db.session.commit()
    flash(f'{Product.query.get(product_id).name} removed successfully.', 'warning')
    return redirect(url_for('shop.show_cart'))

@shop.route('/cart/add', methods=['GET'])
def add_to_cart():
    user = User.query.get(current_user.id)
    if not user.is_customer:
        user.is_customer = True
        db.session.commit()
    product_id = request.args.get('id')
    data = {
        'user_id': user.id,
        'product_id': product_id,
    }
    cart = Cart()
    cart.from_dict(data)
    cart.save()
    flash(f'{Product.query.get(product_id).name} added successfully', 'success')
    return redirect(request.referrer)

@shop.route('/category', methods=['GET'])
@login_required
def category():
    category_id = request.args.get('id')

    context = {
        'category': Category.query.get(category_id),
        'products': Product.query.filter_by(category_id=category_id).all()
    }
    return render_template('shop/index.html', **context)


