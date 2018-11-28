from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def anime():
    return render_template('anime.html')

@app.route("/manga")
def manga():
    return render_template('manga.html')    

@app.route("/about")
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)