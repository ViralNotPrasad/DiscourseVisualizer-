from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pickle
import time

app = Flask(__name__ , static_url_path="", static_folder="static")
datadict = {}
timelist = []
last_time = 0

@app.route("/home")
def home():
    titles = []
    bodies = []
    comments = []
    labels = []
    topics = []

    for topic in topicset:
        i = 0
        lcount = 0
        for idx in datadict["topics"][topic]:
            label = datadict["labels"][topic][i]
            i+=1
            body = datadict["bodies"][idx]
            if label > 0 and label <= 5 and len(body) < 2000:
                titles.append(datadict["titles"][idx])
                bodies.append(body)
                comments.append(datadict["comments"][idx][1][0])
                labels.append(label)
                topics.append(topic)

                lcount+=1

            if lcount == 5:
                break;
    timecheck("set")
    return render_template(
        'feed.html', l=len(titles), labels=labels, topics=topics, titles=titles, bodies=bodies, comments=comments)

@app.route("/", methods=['POST', 'GET'])
def root():
    return render_template("form.html")

@app.route("/home/click/<string:topic>/<int:label>")
def btnclk(topic, label):
    timecheck("delta", topic, label)
    return redirect(url_for('home'))

def timecheck(action, topic=None, label=None):
    global timelist
    global last_time
    if action == "set":
        last_time = time.time()
        return
    elif action == "delta":
        now_time = time.time()
        delta = now_time - last_time
        last_time = now_time
    timelist.append((topic, label, delta))
    print (timelist)
    return

@app.route('/form', methods=['POST', 'GET'])
def form():
    global last_time
    if request.method == 'POST':
        result = request.form
        print(result)
    timecheck("set")
    return redirect(url_for("home"))

@app.route("/similar/<string:topic>/<int:label>/<int:type>")
def similar(topic, type, label):
    timecheck("delta", topic, label)
    titles = []
    bodies = []
    comments = []
    labels = []
    i = 0
    lcount = 0
    label = int(label)
    if type == 1:  #if data is a comment
        label = abs(6 - label)
    for idx in datadict["topics"][topic]:
        label_new = int(datadict["labels"][topic][i])
        body = datadict["bodies"][idx]
        i+=1

        if label_new == label and len(body) <= 2000:
            titles.append(datadict["titles"][idx])
            bodies.append(body)
            comments.append(datadict["comments"][idx][1][0])
            labels.append(label_new)
            lcount += 1
            # print("lcount= ",lcount)

        if lcount == 5:
            break;
    return render_template('similar.html', titlen=len(titles), titles=titles, bodies=bodies, topic=topic)

@app.route("/shutdown")
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def main():
    global datadict
    global topicset
    with open("../finaldict.pickle", "rb") as f:
        datadict = pickle.load(f)
    with open("../labelled2.pickle","rb") as f:
        datadict["labels"] = pickle.load(f)
    topicset = set(["immigration", "abortion", "shooting", "education", "android"])

    app.run()

if __name__ == "__main__":
    main()
