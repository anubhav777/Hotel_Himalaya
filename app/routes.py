from app import app
from models import *
from files import *
import boto3
import shutil
import os
from flask import request, jsonify, Response


@app.route('/getallalbum', methods=['GET'])
def getallalbum():
    result = Album.query.all()
    new_result = albums_schema.dump(result)
    return jsonify(new_result)


@app.route('/updatealbum/<id>', methods=["PUT"])
def updatealbum(id):

    res = request.json['status']
    interval = request.json['interval']

    album = Album.query.get(id)
    album.status = res
    album.interval = interval
    db.session.commit()
    return({'status': 'updated sucessfully'})


@app.route('/deletealbum/<id>', methods=['DELETE'])
def deletealbum(id):
    result = Album.query.get(id)

    print(result.id)
    newpath = 'D:\React\himalayafrontend\public\%s' % result.name
    os.chdir('D:\React\himalayafrontend\public')
    shutil.rmtree(r'D:\React\himalayafrontend\public\%s' % result.name)
    db.session.delete(result)
    db.session.commit()
    return({'status': 'deleted sucessfully'})


@app.route("/uploadfile", methods=['POST'])
def uploadfile():
    # album=request.headers['album']
    # filename=request.json['filename']
    albumid = None
    filepath = None
    try_filepath = None
    new_albumid = None
    # if album == "":
    #     filepath='D:\HotelHimalaya\%s'%filename
    # else:
    #     filepath='D:\HotelHimalaya\%s\%s'%(album,filename)
    # date=time()
    # albumid=None
    res = request.files.getlist('file')
    albumname = request.args.get('albumid')

    for i in range(len(res)):

        if not albumname:
            new_albumid = request.form['albumid']
        else:
            new_albumid = albumname
        print(new_albumid)
        album = Album.query.filter_by(id=new_albumid).first()

        check_filepath = folder_checker(album.name)
        filepath = check_filepath['path']
        print(filepath)
        try_filepath = "%s/%s" % (album.name, res[i].filename)
        print(try_filepath)
        albumid = new_albumid

        if not file_extension(res[i].filename):
            return ({'status': 'the picture is invalid'})
        if not File_checker(filepath, res[i].filename):
            return ({'status': 'the picture already exist with the same name'})

        filename = res[i].filename
        new_filepath = '%s/%s' % (filepath, filename)
        date = time()
        interval = album.interval
        status = "None"
        new_filename = f"{album.name}/{res[i].filename}"
        print('hi', new_filename)
        result = Filesdb(filename, try_filepath, date,
                         status, interval, albumid)
        db.session.add(result)
        db.session.commit()
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket('himalayastorage')
        res[i].save(os.path.join(filepath, res[i].filename))
        my_bucket.upload_file(Filename=new_filename, Key=new_filename)
        print(new_filepath)

    return({'status': 'file uploaded sucessfully'})
