from flask import Flask, render_template, request, redirect, url_for, flash, abort
import json
import os.path
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv('APP_SECRET')

FILE_PATH = os.getenv('FILE_PATH')

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
  if(request.method == 'POST'):
    urls = {}

    # First we need to check if the url already exists
    # in our file
    if os.path.exists('urls.json'):
      with open('urls.json') as urls_file:
        urls = json.load(urls_file)

      # If the url does not exist, we create it in our file
      if request.form['code'] in urls.keys():
        flash('This key is already taken. Please chose another one.')
        return redirect(url_for('home'))

      if 'url' in request.form.keys():
        urls[request.form['code']] = {'url': request.form['url']}
      else:
        f = request.files['file']
        full_name = request.form['code'] + secure_filename(f.filename)
        f.save(FILE_PATH + full_name)
        urls[request.form['code']] = {'file': full_name}

    with open('urls.json', 'w') as url_file:
      json.dump(urls, url_file)
    return render_template('your-url.html', code=request.form['code'])
  else:
    return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
  if os.path.exists('urls.json'):
    with open('urls.json', 'r') as url_file:
      urls = json.load(url_file)
      if code in urls.keys():
        if 'url' in urls[code].keys():
          return redirect(urls[code]['url'])
        else:
          return redirect(url_for('static', filename='user_files/' + urls[code]['file']))

  return abort(404)

@app.errorhandler(404)
def page_not_found(error):
  return render_template('page-not-found.html'), 404