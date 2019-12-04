from app import db, ma
from datetime import date


class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(100))
    usertype = db.Column(db.String(100))
    registertime = db.Column(db.String(100))
    is_verified = db.Column(db.String(100))
    login = db.relationship('Logindb', backref='loguser', lazy='dynamic')

    def __init__(self, email, fullname, address, phone, password, usertype, registertime, is_verified):
        self.email = email
        self.fullname = fullname
        self.address = address
        self.phone = phone
        self.password = password
        self.usertype = usertype
        self.registertime = registertime
        self.is_verified = is_verified


class Album(db.Model):
    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date(), default=date.today())
    status = db.Column(db.String(100))
    interval = db.Column(db.String(100), nullable=False)
    files = db.relationship('Filesdb', backref='album', lazy='dynamic')

    def __init__(self, name, date, status, interval):
        self.name = name
        self.date = date
        self.status = status
        self.interval = interval


class Filesdb(db.Model):
    __tablename__ = "filesdb"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(100))
    date = db.Column(db.Date(), default=date.today())
    status = db.Column(db.String(100))
    interval = db.Column(db.String(100), nullable=False)
    albumid = db.Column(db.Integer, db.ForeignKey('album.id'))

    def __init__(self, filename, filepath, date, status, interval, albumid):
        self.filename = filename
        self.filepath = filepath
        self.date = date
        self.status = status
        self.interval = interval
        self.albumid = albumid


class Ppt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date = db.Column(db.String(100))
    userid = db.Column(db.Integer, db.ForeignKey('signup.id'))

    def __init__(self, status, name, date, userid):
        self.status = status
        self.name = name
        self.date = date
        self.userid = userid


class Trydb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, name, status):
        self.name = name
        self.status = status


class SignupSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'fullname', 'address', 'phone',
                  'password', 'usertype', 'registertime', 'is_verified')


class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', 'date', 'interval')


class PptSchema(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'linknamename', 'date', 'userid')


class FilesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'filename', 'filepath', 'date',
                  'status', 'interval', 'albumid')


class TrydbSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status')


signup_schema = SignupSchema()
signups_schema = SignupSchema(many=True)

ppt_schema = PptSchema()
ppt_schema = PptSchema(many=True)

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

file_schema = FilesSchema()
files_schema = FilesSchema(many=True)

trydb_schema = TrydbSchema()
trydbs_schema = TrydbSchema(many=True)
