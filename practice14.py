from flask import Flask, request 
from flask_sqlalchemy import SQLAlchemy

url = "https://solana-gateway.moralis.io/nft/mainnet/6NqLaD1U3N3rsUm42XyPRfd9Nd4TiygYvpcWwkiuC4Yf/metadata"

headers = {

    "accept": "application/json",
    "X-API-Key": "test"

}

response = requests.get(url, headers=headers)

print(response.text)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/flaskmovie'
app.debug = True
db = SQLAlchemy(app) 

# Define models
roles_users = db.Table('nft_details')
db.Column('nft_id', db.Integer(), db.ForeignKey('nft.id'))

class nft(db.Model, RoleMixin):
    nft_id = db.Column(db.Integer(), primary_key=True)
    nft_name = db.Column(db.String(80), unique=True)
    nft_description = db.Column(db.String(255))



@app.route("/")
def index():
    return render_template('nft.html', nft_name=nft_name)



# allow both GET and POST requests
@app.route('/form-example', methods=['GET', 'POST'])
def form_example():
    
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        print(language)
    
    return '''
                  <h1>The information about NFT {}</h1>'''.format(language)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>URL of NFT <input type="text" name="language"></label></div>
               <input type="submit" value="Submit">
           </form>'''

if __name__ == '__main__':

    app.run(debug=True) #

