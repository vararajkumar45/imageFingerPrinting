from email.mime import image
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from undouble import Undouble
import random
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generateRandom():
    aplha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(aplha) for i in range(20))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        
        ran = generateRandom()
        filename = ran + '.png'
        f.save(os.path.join(app.root_path, 'static/dataset/uploaded/'+filename))

        model = Undouble(method='ahash', hash_size=8)
        # ahash -> fossil
        # dhash -> sunflower
        # phash -> lotus

        # Import example data
        targetdir = './static/dataset'

        model.import_data(targetdir)

        # Compute image-hash
        model.compute_hash()

        model.group(threshold=10000)

        #img 
        #filenames
        #pathnames
        #url
        #img_hash_bin
        #img_hash_hex
        #adjmat
        #select_pathnames
        #select_scores
        #select_idx

        scores = list(model.results['select_scores'][0])
        filenames = list(model.results['filenames'])
        pathnames = list(model.results['pathnames'])

        indexOfFile = filenames.index(filename)
        scoreOfFile = scores[indexOfFile]

        threshold = 1
        allIndexes = [i for i, x in enumerate(scores) if x == scoreOfFile]
        
        allPathnames = [pathnames[i].replace('./static/dataset', '') for i in allIndexes]
        allPathnames = [i for i in allPathnames if 'uploaded' not in i]

    return render_template('index.html', similarUploaded =  allPathnames[:20])

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':

        # Get the search term
        image_type = request.form['image_type']
            
        # Initialize model
        # phash, ahash, whash, dhash
        model = Undouble(method='dhash', hash_size=8)

        # Import example data
        targetdir = './static/dataset/'

        if image_type != 'all':
            targetdir += image_type+'/'

        # Importing the files files from disk, cleaning and pre-processing
        model.import_data(targetdir)

        # Compute image-hash
        model.compute_hash()

        model.group(threshold=10)

        for i in range(len(model.results['pathnames'])):
            model.results['pathnames'][i] = model.results['pathnames'][i].replace('./static/dataset/', '')

        return render_template('index.html',search=model.results['pathnames'][:9])

if __name__ == '__main__':
    app.run(debug=True)