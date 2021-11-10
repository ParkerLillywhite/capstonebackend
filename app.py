
from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)



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
    #response = flask.Response()
    #response.headers['Access-Control-Allow-Origin'] = "*"
    class_id = request.json['class_id']
    class_name = request.json['class_name']
    class_description = request.json['class_description']

    

    new_id = Class(class_id, class_name, class_description)

    db.session.add(new_id)
    db.session.commit()

    class_item = Class.query.get(new_id.id)

    return class_schema.jsonify(class_item)

@app.route('/id_manual/result', methods=['GET'])
def get_manual():
    all_classes = Class.query.all()
    
    result = classes_schema.dump(all_classes)
    return jsonify(result)
    




if __name__ == '__main__':
        app.run(debug=True)