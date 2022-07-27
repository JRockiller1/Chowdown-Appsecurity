from app import app
import os

cert = os.path.join(os.path.dirname(__file__), 'certificate.pem')
key = os.path.join(os.path.dirname(__file__), 'key.pem')
# print(cert)
# print(key)
# context = SSL.context(SSL.TLSv1_2_METHOD)
# context.use_certificate('mycert.crt')
# context.use_privatekey('myprivatekey.key')
# Adding Secret Key to our App
app.secret_key = 'make this hard to guess1!'

app.run(debug=True,ssl_context=(cert,key))
# app.run(debug=True)

# use openssl generate self signed certificate 
