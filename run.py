from app import app


# context = SSL.context(SSL.TLSv1_2_METHOD)
# context.use_certificate('mycert.crt')
# context.use_privatekey('myprivatekey.key')
# Adding Secret Key to our App
app.secret_key = 'make this hard to guess1!'

# app.run(debug=True,ssl_context=('certificate.pem','key.pem'))
app.run(debug=True)

# use openssl generate self signed certificate 

# percival xss stuff not removed yet
