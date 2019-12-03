from app import db, ma
from datetime import date


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


class Trydb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, name, status):
        self.name = name
        self.status = status


class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', 'date', 'interval')


class FilesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'filename', 'filepath', 'date',
                  'status', 'interval', 'albumid')


class TrydbSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status')


album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

file_schema = FilesSchema()
files_schema = FilesSchema(many=True)

trydb_schema = TrydbSchema()
trydbs_schema = TrydbSchema(many=True)
