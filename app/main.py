from flask import Flask, render_template, request, make_response, jsonify
from os import abort
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import json
import random

app = Flask(__name__)
CORS(app)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

db = SQLAlchemy(app)


class WrapperStore(db.Model):
    __tablename__ = 'wrapper_store'
    storeID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    hppName = db.Column(db.String(700))
    template = db.Column(db.Integer)
    logo = db.Column(db.String(700))
    status = db.Column(db.Integer)
    options = db.Column(db.String(700))

    def __init__(self, storeID, userID, hppName, template, logo, status, options):
        self.userID = userID
        self.storeID = storeID
        self.hppName = hppName
        self.template = template
        self.logo = logo
        self.status = status
        self.options = options


class WrapperProduct(db.Model):
    __tablename__ = 'wrapper_product'
    uid = db.Column(db.Integer)
    name = db.Column(db.String(700))
    price = db.Column(db.Integer)
    description = db.Column(db.String(700))
    picture = db.Column(db.String(700))
    size = db.Column(db.String(500))
    color = db.Column(db.String(700))
    category = db.Column(db.String(500))
    gender = db.Column(db.String(500))
    itemID = db.Column(db.Integer, primary_key=True)

    def __init__(self, uid, price, name, description, picture, size, color, category, gender, itemID):
        self.uid = uid
        self.price = price
        self.name = name
        self.description = description
        self.picture = picture
        self.size = size
        self.color = color
        self.category = category
        self.gender = gender
        self.itemID = itemID


class Orders(db.Model):
    __tablename__ = "orders"
    userID = db.Column(db.Integer, default=0)
    productID = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer, default=0)

    def __init__(self, userID, productID, quantity, price):
        self.userID = userID
        self.productID = productID
        self.quantity = quantity
        self.price = price


class Data(db.Model):
    __tablename__ = "data"
    productId = db.Column(db.Integer, primary_key=True)
    storeID = db.Column(db.Integer, default=0)
    name = db.Column(db.String(700), nullable=False, default=None)
    descShort = db.Column(db.String(1200), default=None)
    descLong = db.Column(db.String(1200), default=None)
    visible = db.Column(db.Integer, default=1)
    stock = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, default=0)
    categories = db.Column(db.String(2500), default=None)
    image = db.Column(db.String(2500), default=None)
    featuredProduct = db.Column(db.Integer, default=0)
    options = db.Column(db.String(2500), default=None)
    color = db.Column(db.String(2500), default=None)
    size = db.Column(db.String(2500), default=None)
    gender = db.Column(db.String(2500), default=None)

    def __init__(self, productId, storeID, name, descShort, descLong, visible, stock, price, categories, image,
                 featuredProduct, options, color, size, gender):
        self.productId = productId
        self.storeID = storeID
        self.name = name
        self.descShort = descShort
        self.descLong = descLong
        self.visible = visible
        self.stock = stock
        self.price = price
        self.categories = categories
        self.image = image
        self.featuredProject = featuredProduct
        self.options = options
        self.color = color
        self.size = size
        self.gender = gender


class Store(db.Model):
    __tablename__ = "store"
    storeID = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(2500), default=None)
    hpp = db.Column(db.String(2500), default=None)
    image = db.Column(db.String(2500), default=None)
    filters = db.Column(db.String(2500), default=None)

    def __init__(self, storeID, header, hpp, image, filters):
        self.storeID = storeID
        self.header = header
        self.hpp = hpp
        self.image = image
        self.filters = filters

    def __repr__(self):
        return {'storeID': self.storeID, 'header': self.header, 'hpp': self.hpp, 'image': self.image,
                'filters': self.filters}


@app.route('/')
def index():
    return render_template('index.html')


# Data Route - Shows the loaded information
@app.route('/data')
@cross_origin()  # allow all origins all methods.
def data():
    retVal = 'Rows = ' + str(len(Data.query.all())) + '<br />'

    for row in Data.query.all():
        retVal += '<br />' + str(row.__repr__())
    return retVal


# Data Route - Shows the JSON data
@app.route('/products')
@cross_origin()  # allow all origins all methods.
def results():
    retVal = []
    for row in Data.query.all():
        print(row.productId)
        retVal.append(
            {'productId': row.productId, 'storeID': row.storeID, 'name': row.name, 'descShort': row.descShort,
             'descLong': row.descLong,
             'visible': row.visible, 'stock': row.stock, 'price': row.price, 'categories': row.categories,
             'image': row.image, 'options': row.options})
    return jsonify(retVal), {'content-type': 'application/json'}


# Store Route- Shows all the general store information
@app.route('/store/<storeid>')
def storeInfo(storeid):
    retVal = []
    store_query = Store.query.filter(Store.storeID == storeid).all()
    for row in store_query:
        print(row.storeID)
        retVal.append(
            {'storeID': row.storeID, 'header': row.header, 'hpp': row.hpp, 'image': row.image, 'filters': row.filters})
        return jsonify(retVal), {'content-type': 'application/json'}


# Data Route - Shows the JSON data
@app.route('/store/<storeid>/products/')
@cross_origin()  # allow all origins all methods.
def storeResults(storeid):
    retVal = []
    product_query = Data.query.filter(Data.storeID == storeid).all()
    for row in product_query:
        print(row.productId)
        retVal.append(
            {'productId': row.productId, 'storeID': row.storeID, 'name': row.name, 'descShort': row.descShort,
             'descLong': row.descLong,
             'visible': row.visible, 'stock': row.stock, 'price': row.price, 'categories': row.categories,
             'image': row.image, 'options': row.options, 'color': row.color, 'size': row.size, 'gender': row.gender})
    return jsonify(retVal), {'content-type': 'application/json'}


@app.route('/store/<storeparam>/products/<productparam>')
@cross_origin()  # allow all origins all methods.
def resultIs(storeparam, productparam):
    product_query = Data.query.filter(Data.productId == productparam, Data.storeID == storeparam).one_or_none()
    queryObj = {}
    if product_query is None:
        abort(
            404,
            "Person not found for Id",
        )
    if product_query.options:
        queryObj = {'productId': product_query.productId, 'name': product_query.name,
                    'descShort': product_query.descShort,
                    'descLong': product_query.descLong, 'visible': product_query.visible, 'stock': product_query.stock,
                    'price': product_query.price, 'categories': product_query.categories, 'image': product_query.image,
                    'options': product_query.options, 'color': product_query.color, 'size': product_query.size,
                    'gender': product_query.gender}
    else:
        queryObj = {'productId': product_query.productId, 'name': product_query.name,
                    'descShort': product_query.descShort,
                    'descLong': product_query.descLong, 'visible': product_query.visible, 'stock': product_query.stock,
                    'price': product_query.price, 'categories': product_query.categories, 'image': product_query.image,
                    'color': product_query.color, 'size': product_query.size, 'gender': product_query.gender}
    return jsonify(queryObj), {'content-type': 'application/json'}


@app.route('/order/remove/<p_id>', methods=['GET', 'POST'])
@cross_origin()
def orderRemove(p_id):
    Orders.query.filter_by(productID=p_id).delete()
    db.session.commit()
    return 'success', 200


@app.route('/order/add', methods=['GET', 'POST'])
@cross_origin()  # allow all origins all methods.
def orderAdd():
    userID = request.args.get('userID')
    productID = request.args.get('productID')
    quantity = request.args.get('quantity')
    price = request.args.get('price')
    # product_id_query = Orders.query.filter(Orders.productID == productID)
    # print(product_id_query)
    if price:
        # there is no matching product id already
        obj = Orders(int(userID), int(productID), int(quantity), int(price))
        db.session.add(obj)
        db.session.commit()
        res = make_response(
            jsonify(
                {"userID": int(userID), "productID": int(productID), "quantity": int(quantity), "price": int(price)}
            )
        )
    else:
        res = make_response('duplicate product id', 400)
    return res


@app.route('/order/delete/<userid>', methods=['POST'])
@cross_origin()
def orderDelete(userid):
    db.session.query(Orders).filter(Orders.userID == userid).delete()
    db.session.commit()
    return 'success', 200


@app.route('/wrapper/stores/all', methods=['GET'])
@cross_origin()
def wrapperStores():
    wrapper_query = db.session.query(WrapperStore).all()
    queryObj = []
    for row in wrapper_query:
        queryObj.append(
            {'storeID': row.storeID, 'userID': row.userID, 'hppName': row.hppName,
             'template': row.template, 'logo': row.logo, 'status': row.status,
             'options': row.options
             })
    return jsonify(queryObj), {'content-type': 'application/json'}


@app.route('/wrapper/user/<userID>/stores/all', methods=['GET'])
@cross_origin()
def getWrapperStores(userID):
    wrapper_store_query = db.session.query(WrapperStore).filter(WrapperStore.userID == userID).all()
    queryObj = []
    if wrapper_store_query is None:
        abort(
            404,
            'This is not a valid user ID'
        )
    else:
        for row in wrapper_store_query:
            queryObj.append(
                {'storeID': row.storeID, 'userID': row.userID, 'hppName': row.hppName,
                 'template': row.template, 'logo': row.logo, 'status': row.status,
                 'options': row.options
                 })
        return jsonify(queryObj), {'content-type': 'application/json'}


@app.route('/wrapper/save', methods=['POST'])
@cross_origin()
def wrapperSave():
    data = request.get_json(force=True)
    uid = random.randint(0, 1000000)
    for product in data:
        obj = WrapperProduct(int(uid), str(product['name']), int(product['price']), str(product['description']),
                             str(product['picture']), str(product['size']), str(product['color']),
                             str(product['category']), str(product['gender']))
        db.session.add(obj)
    db.session.commit()
    return jsonify({'saveID': uid}), {'content-type': 'application/json'}


@app.route('/wrapper/retrieve/id/<id>', methods=['GET'])
@cross_origin()
def wrapperRetrieval(id):
    wrapper_product_query = db.session.query(WrapperProduct).filter(WrapperProduct.uid == id).all()
    queryObj = []
    if wrapper_product_query is None:
        abort(
            404,
            "This is not a valid ID"
        )
    else:
        for row in wrapper_product_query:
            print('hi')
            queryObj.append(
                {'uid': row.uid, 'price': row.price, 'name': row.name, 'description': row.name, 'picture': row.picture,
                 'size': row.size,
                 'color': row.color, 'category': row.category, 'gender': row.gender, 'itemID': row.itemID
                 })
        return jsonify(queryObj), {'content-type': 'application/json'}