from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.record'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app) #marsmallow object

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))

    def __init__(self,name,age,address):
        self.name = name
        self.age = age
        self.address = address

class RecordSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'age', 'address')

record_schema = RecordSchema(many=False) #for single record
records_schema = RecordSchema(many=True) #for multiple record

#Create a new Record
@app.route("/Record", methods=["POST"])
def add_record():
    name = request.json['name']
    age = request.json['age']
    address = request.json['address']
    new_record = Record(name, age, address)
    db.session.add(new_record)
    db.session.commit()
    return record_schema.jsonify(new_record)

#Search all Record
@app.route("/Record", methods=["GET"])
def get_records():
    all_record = Record.query.all()
    result = records_schema.dump(all_record)
    return jsonify(result)

#Search an individual Record
@app.route("/Record/<id>", methods=["GET"])
def get_record(id):
    product = Record.query.get(id)
    return record_schema.jsonify(product)

#Update a Record
@app.route("/Record/<id>", methods=["PUT"])
def update_record(id):
    record = Record.query.get(id)

    name = request.json['name']
    age = request.json['age']
    address = request.json['address']
    record.name = name
    record.age = age
    record.address = address
    db.session.commit()
    return record_schema.jsonify(record)
  
#Delete a Record
@app.route("/Record/<id>", methods=["DELETE"])
def delete_record(id):
    record = Record.query.get(id)
    db.session.delete(record)
    db.session.commit()
    return record_schema.jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)
