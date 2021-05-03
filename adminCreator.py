from modules.models import User
from modules import bcrypt,db

username = input('Enter username')
email = input('Enter email ID:')
password = input('Password')
cpassword = input('Confirm Password')

if password == cpassword:
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username ,email=email, password=hashed_password, admin=1)
    db.session.add(user)
    db.session.commit()
else:
    print('Please enter the password again!!!')
