from flask import Flask, request
import requests
import psycopg2

app = Flask(__name__)

def check_in_db(address):
    conn = psycopg2.connect("dbname=solana user=postgres password='123'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM solana where url='"+address+"'")
    if(cur.rowcount==0):
        return False
    return True

@app.route('/query-example')
def query_example():
    return 'Query String Example'

@app.route('/json-example')
def json_example():
    return 'JSON Object Example'
    
@app.route('/', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        returnValue=""
        address = request.form.get('address')
        if(check_in_db(address)):
            conn = psycopg2.connect("dbname=solana user=postgres password='123'")
            cur = conn.cursor()
            cur.execute("SELECT information FROM solana where url='"+address+"'")
            records = cur.fetchall()
            returnValue=records[0][0]
        else:            
            url = "https://solana-gateway.moralis.io/nft/mainnet/{}/metadata".format(address)
            headers = {
                "accept": "application/json",
                "X-API-Key": "OjvXHY7ltVwY7xKG1p9HtQmLfKuRiodrazyFMLx2ZAAzECrZY7soe5LMcTTIvj8z"
            }
            returnValue = requests.get(url, headers=headers).text
            conn = psycopg2.connect("dbname=solana user=postgres password='123'")
            cur = conn.cursor()
            cur.execute("insert into solana(url,information) values('{}','{}')".format(address, returnValue))
            conn.commit()
        return '''
                <h1>{}</h1>
                  '''.format(returnValue)
    
    return '''
           <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-5">
        <a class="navbar-brand" href="{{ url_for('index') }}"> NFT</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="{{ url_for('posts.posts_list') }}"> Information <span class="sr-only"></span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Link</a>
            </li>
            
          </ul>

          
           <form method="POST"style="margin: auto; width: 220px; text-align: center; " placeholder="Search" aria-label="Search">
               <div><label>address: <input type="text" name="address"></label></div>

            <button class="btn btn-outline-success my-2 my-sm-0" 
            type="submit">Search</button>

           </form>
        </div>
      </nav>
      <img src="{{url_for('solana', filename=nft.jpg)}}">

</body>
</html>'''



if __name__ == '__main__':
    app.run(debug=True, port=5000)


