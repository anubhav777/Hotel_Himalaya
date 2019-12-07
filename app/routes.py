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


@app.route('/signup', methods=['POST'])
def register():
    email = request.form['email']
    fullname = request.form['fullname']
    address = request.form['address']
    phone = request.form['phone']
    new_password = request.form['password']
    usertype = request.form['usertype']
    hash_password = generate_password_hash(new_password, method='sha256')
    password = hash_password
    registertime = time()
    is_verified = 'False'
    filepath = request.files['file']
    filename = filepath.filename
    picturepath = f"Users/{filename}"

    path = makefolder('Users')

    validator = Signup.query.filter_by(email=email).first()

    if validator:
        return ({'status': 'error', 'noty': 'This email has already been registered'})
    else:
        if not profile_checker(picturepath):
            return({'status': 'error', 'noty': 'the pictiure seems to be in wrong format or seems to have been uploaded'})
        else:
            filepath.save(os.path.join(path, filename))
            upload_file(picturepath, 'greenhorse')
            new_data = Signup(email, fullname, address, phone, password,
                              usertype, registertime, is_verified, picturepath)
            db.session.add(new_data)
            db.session.commit()
            remove_file = os.path.join(path, filename)
            file_remove(remove_file)
            # return signup_schema.jsonify(new_data)
            return({'status': 'success', 'noty': 'Sucessfully registered'})


@app.route('/getuser/<id>', methods=['GET'])
@token
def getuser(currrentuser, id):
    user = Signup.query.filter_by(id=currrentuser).first()
    if not user:
        return ({'status': 'error', 'noty': 'you cannot perfom this action'})

    if user.usertype != "admin":

        new_user = Signup.query.get(user.id)
        return signup_schema.jsonify(new_user)

    new_user = Signup.query.get(id)
    return signup_schema.jsonify(new_user)


@app.route('/getalluser', methods=["GET"])
@token
def getalluser(currentuser):
    new_user = Signup.query.filter_by(id=currentuser).first()

    if not new_user:
        return ({'status': 'error', 'noty': 'you cannot perfom this action'})

    if new_user.usertype != "admin":
        return ({'status': 'error', 'noty': 'you cannot perfom this action'})

    newuser = Signup.query.all()
    result = signups_schema.dump(newuser)

    return jsonify({'data': result, 'user': new_user.usertype})


@app.route('/tryuser', methods=["GET"])
def gettryuser():

    newblauser = Signup.query.all()
    result = signups_schema.dump(newblauser)

    return jsonify(result)


@app.route('/updateuser/<uid>', methods=['PUT'])
@token
def updateuser(currentuser, uid):
    user = None
    new_usertype = None
    new_user = Signup.query.filter_by(id=currentuser).first()

    if not new_user:
        return {'please login first'}

    if new_user.usertype == "staff":
        user = Signup.query.filter_by(id=new_user.id).first()
        new_usertype = 'staff'
    if new_user.usertype == "admin":
        user = Signup.query.filter_by(id=uid).first()
        new_usertype = request.json['usertype']

    curr_user = user.id
    email = request.json['email']
    fullname = request.json['fullname']
    address = request.json['address']
    phone = request.json['phone']

    user.email = email
    user.fullname = fullname
    user.address = address
    user.phone = phone
    user.usertype = new_usertype

    db.session.commit()

    return jsonify({'status': 'success', 'noty': 'User Sucessfully Updated'})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth:
        return ({'status': 'error', 'noty': 'you login credetials do not match'})

    user = Signup.query.filter_by(email=auth.username).first()

    if not user:
        return ({'status': 'error', 'noty': 'you login credetials do not match'})
    if user.is_verified != "True":
        return({'status': 'error', 'noty': 'Your account is not verified'})

    if check_password_hash(user.password, auth.password):
        obj = {'id': user.id, 'exp': datetime.datetime.utcnow() +
               datetime.timedelta(hours=4)}
        data = jwt.encode(obj, key)
        loginchecker(user.id)

        return jsonify({'token': data.decode('UTF-8'), 'status': 'success', 'usertype': user.usertype, 'filepath': user.picturepath, 'userid': user.id})

    return ({'status': 'error', 'noty': 'you login credetials do not match'})
