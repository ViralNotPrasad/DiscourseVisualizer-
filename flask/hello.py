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
form_dict = None
glob_name = None
topicset = {}
def find_observed_lean(lot):

    # In[32]:


    immil=[]
    shootl=[]
    andl=[]
    abl=[]
    edul=[]

    immia=[]
    shoota=[]
    anda=[]
    aba=[]
    edua=[]

    immiaa=0
    shootaa=0
    andaa=0
    abaa=0
    eduaa=0

    for x in lot:
        if x[0]=='immigration':
            immil.append(x[1])
            la=x[2]/x[3]
            immia.append(la)
            immiaa+=la
        elif x[0] == 'shooting':
            shootl.append(x[1])
            shoota.append(x[2]/x[3])
            shootaa+=x[2]/x[3]
        elif x[0] == 'education':
            edul.append(x[1])
            print(x[1])
            la2=x[2]/x[3]
            print(la2)
            eduaa+=la2
            edua.append(la2)
        elif x[0] == 'android':
            andl.append(x[1])
            anda.append(x[2]/x[3])
            andaa+=x[2]/x[3]
        elif x[0] == 'abortion':
            abl.append(x[1])
            aba.append(x[2]/x[3])
            abaa+=x[2]/x[3]

    observed_lean={}

    summ=0
    for x,y in zip(immia,immil):
        summ+=y*(x/immiaa)
    observed_lean['immigration']=summ

    summ=0
    for x,y in zip(shoota,shootl):
        summ+=y*(x/shootaa)
    observed_lean['shooting']=summ

    summ=0
    for x,y in zip(aba,abl):
        summ+=y*(x/abaa)
    observed_lean['abortion']=summ

    summ=0
    for x,y in zip(edua,edul):
        summ+=y*(x/eduaa)
    observed_lean['education']=summ

    summ=0
    for x,y in zip(anda,andl):
        summ+=y*(x/andaa)
    observed_lean['android']=summ

    print(observed_lean)
    return observed_lean

def process_form_results(form_data):
    global glob_name
    form_data=dict(form_data)
    form_data_list={k: v for k, v in form_data.items()}
    print(type(form_data_list))
    print(form_data_list)

    name = form_data_list["name"][0]
    glob_name = name
    # In[3]:


    #HIGHER SCORE MEANS

    immi=0
    immi+=6-int(form_data_list['immi1'].pop()[6])
    immi+=6-int(form_data_list['immi2'].pop()[6])
    immi+=6-int(form_data_list['immi3'].pop()[6])
    immi+=6-int(form_data_list['immi4'].pop()[6])
    #ProImmmi

    gun=0
    gun+=6-int(form_data_list['gun1'].pop()[6])
    gun+=6-int(form_data_list['gun2'].pop()[6])
    gun+=int(form_data_list['gun3'].pop()[6])
    gun+=int(form_data_list['gun4'].pop()[6])
    #ProGunControl

    abort=0
    abort+=int(form_data_list['abort1'].pop()[6])
    abort+=6-int(form_data_list['abort2'].pop()[6])
    abort+=int(form_data_list['abort3'].pop()[6])
    abort+=6-int(form_data_list['abort4'].pop()[6])
    #ProAbortion

    andd=0
    andd+=int(form_data_list['android1'].pop()[6])
    andd+=6-int(form_data_list['android2'].pop()[6])
    andd+=int(form_data_list['android3'].pop()[6])
    andd+=6-int(form_data_list['android4'].pop()[6])
    #ProAndroid_AntiApple

    edu=0
    edu+=int(form_data_list['edu1'].pop()[6])
    edu+=int(form_data_list['edu2'].pop()[6])
    edu+=6-int(form_data_list['edu3'].pop()[6])
    edu+=int(form_data_list['edu4'].pop()[6])


    # In[4]:


    user_lean={"name":name, "immigration": immi/4, "shooting": gun/4, "abortion": abort/4, "immigration": immi/4, "shooting": gun/4, "android": andd/4,"education": edu/4}


    # In[5]:


    print(user_lean)

    return user_lean

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
        topic_leans = []
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
                topic_leans.append(abs(form_dict[topic] - label))

                lcount+=1

            if lcount == 5:
                break;
    timecheck("delta", current_topic_time, current_label_time, current_tot_post_len)
    return render_template(
        'feed.html', l=len(titles), labels=labels, topics=topics, titles=titles, bodies=bodies, comments=comments, topic_leans=topic_leans)

@app.route("/", methods=['POST', 'GET'])
def root():
    return render_template("form.html")

@app.route("/exit")
def exit():
    obs_dict = find_observed_lean(timelist)
    obs_dict["name"] = glob_name
    dict_tup = (form_dict,obs_dict)
    with open("dict_tup.pickle", "wb") as f:
        pickle.dump(dict_tup, f)
    return redirect("https://goo.gl/forms/yCyHS66ilLNk12Xv2")

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
    global form_dict
    if request.method == 'POST':
        result = request.form
        # print(result)
        # with open("form_result.pickle", "wb") as f:
        #     pickle.dump(result, f)
        form_dict = process_form_results(result)
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
