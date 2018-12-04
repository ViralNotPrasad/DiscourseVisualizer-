#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# user_lean={'name':'dhruvaaas','immigration': 2.25, 'shooting': 2.5, 'abortion': 4.0, 'android': 2.25, 'education': 3.5}
# observed_lean={:'immigration': 4.389004149377593, 'shooting': 0, 'abortion': 0, 'education': 3.172529313232831, 'android': 0}


# In[10]:


# import pandas as pd
# ReadExcel = pd.read_excel ('exit.xlsx')
# df = ReadExcel
# df.columns = ['timestamp', 'email', 'name', 'age', 'gender', 'i1', 'e1', 'an1', 'ab1', 'i2','g1','ab2','an2','i3','an3','g2','e2','blah','ab3','an4','g3','e3','ab4','i4','e4','g4','e5']
# exit=df.to_dict('records')
# print(exit)


# In[ ]:


# import pickle
# with open("dict_tup.pickle","rb") as f:
#     d_t_pickle = pickle.load(f)
# print(d_t_pickle)


# In[30]:

#NEED EXCEL SHEET IN THE SAME  FOLDER

def excel(exit):
    immi=0
    gun=0
    abort=0
    andd=0
    edu=0
    for e in exit:
        immi=6-e['i1']
        immi+=6-e['i2']
        immi+=6-e['i3']
        immi+=6-e['i4']
        gun=e['g1']
        gun+=6-e['g2']
        gun+=6-e['g3']
        gun+=e['g4']
        abort=6-e['ab1']
        abort+=6-e['ab2']
        abort+=e['ab3']
        abort+=e['ab4']
        andd=6-e['an1']
        andd+=6-e['an2']
        andd+=e['an3']
        andd+=e['an4']
        edu=e['e1']
        edu+=e['e2']
        edu+=6-e['e3']
        edu+=e['e4']
        exit_lean={"name":e['name'],"immigration":immi/4, "shooting": gun/4, "abortion": abort/4, "android": andd/4,"education": edu/4}
    return exit_lean


# In[31]:


def record(user_lean, observed_lean):
    recorded_metric={'name':user_lean['name']}
    for key in observed_lean.keys():
        if key != 'name':
            recorded_metric[key]=user_lean[key]-observed_lean[key]
    print(recorded_metric)
    return recorded_metric


# In[32]:


def gen_metrics(d_t_pickle,exit_leann):
    for x in d_t_pickle:
        metric1=record(x[0],x[1])
        metric2=record(x[0],exit_leann[x[0]['name'][0]])#SAVE THE NAME AS A  STRING
        metrics={'name':x[0]['name'],'recorded metric':metric1,'reported metric':metric2}
    print(metrics)    


# In[33]:


def main():
    import pandas as pd
    ReadExcel = pd.read_excel ('exit.xlsx')
    df = ReadExcel
    df.columns = ['timestamp', 'email', 'name', 'age', 'gender', 'i1', 'e1', 'an1', 'ab1', 'i2','g1','ab2','an2','i3','an3','g2','e2','blah','ab3','an4','g3','e3','ab4','i4','e4','g4','e5']
    exit=df.to_dict('records')
    print(exit)
    
    import pickle
    with open("dict_tup.pickle","rb") as f:
        d_t_pickle = [pickle.load(f)]
    print(d_t_pickle)
    
    exit_leann=excel(exit)
    gen_metrics(d_t_pickle,exit_leann)


# In[34]:


main()

