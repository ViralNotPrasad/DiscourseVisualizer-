#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
form_data = pickle.load( open( "form_result.pickle", "rb" ) )


# In[2]:


form_data=dict(form_data)
form_data_list={k: v for k, v in form_data.items()}
print(type(form_data_list))
print(form_data_list)


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


user_lean={"immigration":int(round(immi/4)), "shooting":int(round(gun/4)), "abortion":int(round(abort/4)), "immigration":int(round(immi/4)), "shooting":int(round(gun/4)), "android":int(round(andd/4)),"education":int(round(edu/4))}


# In[5]:


print(user_lean)


# In[8]:


# PICKLE CODE IF U WANT
fileObject = open("user_lean.pickle",'wb') 
pickle.dump(user_lean,fileObject)   
fileObject.close()

