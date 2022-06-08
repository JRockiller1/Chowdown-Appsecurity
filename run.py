from app import app
# from OpenSSL import SSL

# Adding Secret Key to our App
app.secret_key = 'make this hard to guess1!'

app.run(debug=True)