from flask import Flask, flash, redirect, render_template, request, session, abort
import pickle
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home(name):
    titles = []
    bodies = []
    comments = []
    topicset = set(["immigration", "abortion", "shooting", "education", "android"])
    with open("../finaldict.pickle", "rb") as f:
        datadict = pickle.load(f)

    for topic in topicset:
        for idx in datadict["topics"][topic][:5]:
            titles.append(datadict["titles"][idx])
            bodies.append(datadict["bodies"][idx])
            comments.append(datadict["comments"][idx][1][0])


    return render_template(
        'feed.html', titles=titles, bodies=bodies, comments=comments)


@app.route("/similar/<string:topic>/<int:lean>")
def similar(topic, lean):
    return (topic+str(lean))

@app.route("/shutdown")
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == "__main__":
    app.run()
