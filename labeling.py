from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
import random, string

@app.route("/", methods=['GET', 'POST'])
def hello():
   name = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
   
   if request.method == 'POST':
      get_keypress = request.get_data()
      print(get_keypress)
   return render_template('hello.html', name=name)

if __name__ == "__main__":
   app.run()
