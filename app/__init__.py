from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import datetime
import shutil
from datetime import date
import boto3

app = Flask(__name__)

app.config.from_object('config.Development')

db = SQLAlchemy(app)
ma = Marshmallow(app)
s3 = boto3.client('s3')
CORS(app)


if __name__ == "__main__":
    app.run(debug=True)
