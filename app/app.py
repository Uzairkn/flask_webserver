import flask
import socket
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os


application = flask.Flask(__name__)
application.config["DEBUG"] = True


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80)
    
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(application)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content


db.create_all()

@application.route('/', methods=['GET'])
def home():
    return f"<H1>Item Created</H1><br>Container Id:{socket.gethostname()}"

@application.route('/items', methods=['GET'])
def get_items():
    items = []
    for item in db.session.query(Item).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)

@application.route('/items/<id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)

@application.route('/items', methods=['POST'])
def create_item():
    body = request.get_json()
    title = body['title']
    content = body['content']
    newItem = Item(title, content)
    db.session.add(newItem)
    db.session.commit()
    return f"item created"

@application.route('/items/<id>', methods=['PUT'])
def update_item(id):
    body = request.get_json()
    db.session.query(Item).filter_by(id=id).update(
        dict(title=body['title'], content=body['content']))
    db.session.commit()
    return "item updated"

@application.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(Item).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"