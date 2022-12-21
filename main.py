from flask import Flask, render_template, send_from_directory
from os import path

app = Flask(__name__)

@app.route('/')
def hello_world():
  link = "answer123.txt"
  return render_template('index.html', link = link)

@app.route('/download/<path:filename>')
def downloading(filename):
  return send_from_directory('answers', filename, as_attachment=True)



if __name__ == '__main__':
    app.run()

#"{{url_for('static', filename='answer.txt')}}"