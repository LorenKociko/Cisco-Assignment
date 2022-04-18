from flask_bcrypt import Bcrypt

bc = Bcrypt()

passw = bc.generate_password_hash('password').decode('utf-8')

print(bc.check_password_hash(passw, 'password'))