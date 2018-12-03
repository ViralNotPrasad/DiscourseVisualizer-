from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pickle
import time

app = Flask(__name__ , static_url_path="", static_folder="static")
datadict = {}
timelist = []
last_time = 0
current_topic_time = None
current_label_time = None
current_tot_post_len = None
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
    timecheck("delta", current_topic_time, current_label_time, current_tot_post_len)
    return render_template(
        'feed.html', l=len(titles), labels=labels, topics=topics, titles=titles, bodies=bodies, comments=comments)

@app.route("/", methods=['POST', 'GET'])
def root():
    return render_template("form.html")

@app.route("/home/click/<string:topic>/<int:label>")
def btnclk(topic, label):
    return redirect(url_for('home'))

def timecheck(action, topic=None, label=None, postlen=None):
    global timelist
    global last_time
    global current_topic_time
    global current_label_time
    global current_tot_post_len
    if action == "set":
        last_time = time.time()
        current_topic_time = topic
        current_label_time = label
        current_tot_post_len = postlen
        return
    elif action == "delta":
        now_time = time.time()
        delta = now_time - last_time
        last_time = now_time

    timelist.append((topic, label, delta, postlen))
    print (timelist)
    return

@app.route('/form', methods=['POST', 'GET'])
def form():
    global last_time
    if request.method == 'POST':
        result = request.form
        print(result)
        with open("form_result.pickle", "wb") as f:
            pickle.dump(result, f)
    return redirect(url_for("home"))

@app.route("/similar/<string:topic>/<int:label>/<int:type>")
def similar(topic, type, label):
    titles = []
    bodies = []
    comments = []
    labels = []
    i = 0
    lcount = 0
    label = int(label)
    bodies_len = 0
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
            bodies_len += len(body)
            lcount += 1
            # print("lcount= ",lcount)

        if lcount == 5:
            break;

    timecheck("set", topic, label, bodies_len) # start the clock when user goes to similar right before rendering the page
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
