from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
import atexit
import cf_deployment_tracker
import os
import json
import ibm_db
import text_scraper

# Emit Bluemix deployment event
from text_to_speech import text_to_speech_list, text_to_speech_string

cf_deployment_tracker.track()

UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pptx', 'pdf', 'docx'])

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]
    appenv = json.loads(os.environ['VCAP_APPLICATION'])
    print('Found VCAP_SERVICES')
    print(os.environ['VCAP_SERVICES'])
    #vcap = json.loads(os.getenv('VCAP_SERVICES'))
else:
    db2cred = json.loads("""{
                "port": 50000,
                "db": "BLUDB",
                "username": "xmp20848",
                "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;",
                "host": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
                "https_url": "https://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
                "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=xmp20848;PWD=w6kpwnbc1z3-3rst;",
                "hostname": "dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net",
                "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
                "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=xmp20848;PWD=w6kpwnbc1z3-3rst;Security=SSL;",
                "uri": "db2://xmp20848:w6kpwnbc1z3-3rst@dashdb-txn-sbox-yp-dal09-03.services.dal.bluemix.net:50000/BLUDB",
                "password": "w6kpwnbc1z3-3rst"
            }""")
    #raise ValueError('Expected cloud environment')

db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")

#     if 'Db2-Sherlock2018' in vcap:
#         creds = vcap['Db2-Sherlock2018'][0]['credentials']
#         user = creds['username']
#         password = creds['password']
#         url = 'https://' + creds['host']
#         client = Cloudant(user, password, url=url, connect=True)
#         db = client.create_database(db_name, throw_on_exists=False)
# elif os.path.isfile('vcap-local.json'):
#     with open('vcap-local.json') as f:
#         vcap = json.load(f)
#         print('Found local VCAP_SERVICES')
#         creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
#         user = creds['username']
#         password = creds['password']
#         url = 'https://' + creds['host']
#         client = Cloudant(user, password, url=url, connect=True)
#         db = client.create_database(db_name, throw_on_exists=False)
# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/social_media.html')
def social_media():
    return render_template('social_media.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader.html', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      lang=request.form['language']
      if allowed_file(f.filename):
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        name, ext = os.path.splitext(filename)
        if ext =='.docx':
            text_docx_list = text_scraper.read_docx(filename)
            audioName=text_to_speech_list(text_docx_list,name,lang)

        elif ext=='.pdf':
            text_pdf_list = text_scraper.read_pdf(filename)
            audioName =text_to_speech_list(text_pdf_list, name, lang)
        elif ext =='.pptx':
            text_pptx_string = text_scraper.read_pptx(filename)
            audioName =text_to_speech_string(text_pptx_string,name,lang)
        return '''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sherlock 2018 - Investigate Your Notes</title>

    <!-- Bootstrap -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <link href="../static/styles.css" rel="stylesheet">
</head>

<body><nav>
  <h4><a href="index.html">Home</a> |
  <a href="about.html">About</a> |
  <a href="social_media.html">Social Media</a> </h4>
</nav>


  <!-- Changes to logo location -->
  <div class = "content" align = "center">
    <img class = "logo" src="../static/SherlockLogo.png" alt="Sherlock Logo" width= "40%">
      <div class="container">
          <h1>Investigate your notes.</h1>
          <audio controls>
            <source src="''' + str(audioName[0]) + '''"type="audio/mp3">
          </audio>
</body>
</html>
'''
      else:
        return 'file failed'

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    if client:
        data = {'name':user}
        db.create_document(data)
        return 'Hello %s! I added you to the database.' % user
    else:
        print('No database')
        return 'Hello %s!' % user

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
