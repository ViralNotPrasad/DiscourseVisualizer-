#!/usr/bin/env python
# coding: utf-8

# In[31]:


#List Of Tuples
import pickle

with open("dict_tup.pickle", "rb") as f:
    dict_tup= pickle.load(f)

print(dict_tup)
