#!/usr/bin/env python
# coding: utf-8

# In[31]:


#List Of Tuples
lot = [('immigration',5,20,155),("education",4,10,260),('immigration',4,17,750),("education",2,19,700),('immigration',4,18,100)]


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

