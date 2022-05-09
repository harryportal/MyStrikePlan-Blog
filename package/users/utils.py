import os
import secrets
from package import mail, create_app
from PIL import Image
from flask_mail import Message
from flask import render_template
import boto3


app = create_app()


def save_image_s3(image):
    session = boto3.Session(
        aws_access_key_id=app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=app.config['AWS_SECRET_KEY']
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(app.config['AWS_BUCKET'])

    # create a new filename to avoid duplication
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image.filename)
    image_file = random_hex + file_ext
    #upload image to s3 bucket
    bucket.upload_fileobj(image, image_file, ExtraArgs={'ACL':'public-Read'})
    return image_file




def save_picture(image):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image.filename)
    image_file = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', image_file)

    output_size = (125, 125)  # resize the image
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(picture_path)
    return image_file


def reset_token(user):
    token = user.get_token()
    msg = Message('Password Reset Request', sender='My Strike Plans', recipients=[user.email])
    msg.html = render_template('mail/passwordreset.html', user=user, token=token)
    mail.send(msg)


def email_token(user):
    token = user.get_token()
    msg = Message('Confirm your Email', sender='My Strike Plans', recipients=[user.email])
    msg.html = render_template('mail/mail.html', user=user, token=token)
    mail.send(msg)


school_list = ['Abubakar Tafawa Balewa University', 'Ahmadu Bello University',
               'Bayero University', 'Federal University Gashua', 'Federal University of Petroleum Resources',
               'Federal University of Technology, Akure', 'Federal University of Technology, Owerri',
               'Federal University, Dutse',
               'Federal University, Dutsin-Ma', 'Federal University of Kashere', 'Federal University of Lafia',
               'Federal University, Lokoja', 'Federal University of Ndifu-Alike',
               'Federal University, Otuoke', 'Federal University of Oye-Ekiti',
               'Federal University, Wukari', 'Federal University of Birnin Kebbi',
               'Federal University of Gusau Zamfara', 'Michael Okpara University of Agricultural Umudike',
               'Modibbo Adama University of Technology', 'National Open University of Nigeria, Lagos',
               'Nnamdi Azikiwe University', 'University of Abuja', '	Federal University of Agriculture, Abeokuta',
               'University of Agriculture, Makurdi', '	University of Benin', 'University of Calabar',
               'University of Ibadan',
               'University of Ilorin', 'University of Jos', 'University of Lagos',
               'University of Maiduguri', 'University of Nigeria,Nsukka', 'University of Port-Harcourt',
               'University of Uyo', 'Others']
