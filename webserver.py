from flask import Flask
from flask import render_template, send_from_directory, Response

app = Flask(__name__,template_folder='assets/html',static_url_path='')

SERVER_ADDRESS = '127.0.0.1:55555'

def readFile(filename):
    with open(filename) as f:
        return f.read()

# App routes

@app.route("/") # Main page
def index():
    return render_template('game.html',serveraddr=SERVER_ADDRESS)

# Static files routes

@app.route('/js/<path:jsfile>')
def loadjs(jsfile):
    return send_from_directory('assets/js', jsfile)

@app.route('/textures/<path:text>')
def loadtexture(text):
    return send_from_directory('assets/textures', text)

@app.route('/css/<path:cssfile>')
def loadcssfile(cssfile):
    return send_from_directory('assets/css',cssfile)

# Clientside config file

@app.route('/gameconfig.js')
def loadjson():
    js = '{"ressources":' + readFile('assets/config/ressources.json') + \
    ',"objects":' + readFile('assets/config/objects.json') + \
    ',"entities":' + readFile('assets/config/entities.json') + \
    ',"items":'+ readFile('assets/config/items.json') +'}'
    js = "const GAMECONFIG = " + js
    return Response(js,mimetype='text/javascript')
