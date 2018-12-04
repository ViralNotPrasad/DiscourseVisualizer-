#!/usr/bin/env python
# coding: utf-8
import pickle
# In[31]:

#List Of Tuples
with open("../finaldict.pickle", "rb") as f:
    d = pickle.load(f)


with open("../labelled2.pickle","rb") as f:
    l = pickle.load(f)


topicset = set(["immigration", "abortion", "shooting", "education", "android"])



print(len(d["titles"]))
sum = 0
for topic in d["topics"]:
    toplen = len(d["topics"][topic])
    sum+=toplen
    print(topic," ",toplen)

print(sum)

labeldict = {}
for topic in topicset:
    rel = 0
    nrel = 0
    for entry in l[topic]:
        if entry > 0:
            rel+=1
        elif entry == 0:
            nrel+=1
    labeldict[topic] = (rel, nrel)

print("Topics Relevant Not-Relevant")
for topic in topicset:
    print(topic,labeldict[topic][0],labeldict[topic][1])
