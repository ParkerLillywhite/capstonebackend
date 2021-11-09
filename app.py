
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.String(100), unique=True)
    class_name = db.Column(db.String(200), unique=False)
    class_description = db.Column(db.String(300), unique=False)

    def __init__(self, class_id, class_name, class_description):
        self.class_id = class_id
        self.class_name = class_name
        self.class_description = class_description

class ClassSchema(ma.Schema):
    class Meta:
        fields = ('class_id', 'class_name', 'class_description')

class_schema = ClassSchema()
classes_schema = ClassSchema(many=True)

@app.route('/id_manual/post', methods=['POST'])
def add_id():
    class_id = request.json['class_id']
    class_name = request.json['class_name']
    class_description = request.json['class_description']

    new_id = Class(class_id, class_name, class_description)

    db.session.add(new_id)
    db.session.commit()

    guide = Class.query.get(new_id.id)

    return class_schema.jsonify(guide)

@app.route('/id_manual/result', methods=['GET'])
def get_manual():
    all_guides = Class.query.all()
    result = classes_schema.dump(all_guides)
    return jsonify(result)
    




if __name__ == '__main__':
        app.run(debug=True)