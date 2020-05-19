from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# bahan class Class/Model
class Bahan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300))
    status = db.Column(db.String)

    # def __init__(self, name, description, status):
    #     self.name = name
    #     self.description = description
    #     self.status = status

    def __repr__(self):
        return f"Bahan('{self.name}','{self.description}','{self.status}')"


# Bahan Schema
class BahanSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "status")


# Init Schema
bahan_schema = BahanSchema()
bahans_schema = BahanSchema(many=True)

# Insert Bahan
@app.route("/bahan", methods=["POST"])
def add_bahan():
    name = request.json["name"]
    description = request.json["description"]
    status = request.json["status"]

    new_bahan = Bahan(name, description, status)

    db.session.add(new_bahan)
    db.session.commit()

    return bahan_schema.jsonify(new_bahan)


# get all bahan
@app.route("/bahan", methods=["GET"])
def get_bahans():
    all_bahan = Bahan.query.all()
    result = bahans_schema.dump(all_bahan)
    return jsonify(result)


# get single bahan
@app.route("/bahan/<id>", methods=["GET"])
def get_bahan(id):
    bahan = Bahan.query.get(id)
    return bahan_schema.jsonify(bahan)


# get single bahan
@app.route("/periksa/<bahan>", methods=["GET"])
def periksa_bahan(bahan):
    periksa = bahan.split(",")
    hasil = Bahan.query.filter(Bahan.name.in_(periksa)).all()
    result = bahans_schema.dump(hasil)
    return jsonify(result)


# PENCARIAN BAHAN
@app.route("/periksa", methods=["POST"])
def periksa_search():
    bahan = request.json["bahan"]
    periksa = bahan.split(",")
    hasil = Bahan.query.filter(Bahan.name.in_(periksa)).all()
    result = bahans_schema.dump(hasil)
    return jsonify(result)


# Update Bahan
@app.route("/bahan/<id>", methods=["PUT"])
def update_bahan(id):
    bahan = Bahan.query.get(id)
    name = request.json["name"]
    description = request.json["description"]
    status = request.json["status"]

    bahan.name = name
    bahan.description = description
    bahan.status = status

    db.session.commit()

    return bahan_schema.jsonify(bahan)


# Delete Product
@app.route("/bahan/<id>", methods=["DELETE"])
def delete_bahan(id):
    bahan = Bahan.query.get(id)
    db.session.delete(bahan)
    db.session.commit()

    return bahan_schema.jsonify(bahan)


# run
if __name__ == "__main__":
    app.run(debug=True)
