from app import app
import os

# Adding Secret Key to our App
app.secret_key = 'make this hard to guess1!'
if __name__ == '__main__':

	app.run(debug=True)
