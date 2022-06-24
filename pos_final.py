from PIL import Image
import numpy as np 
import argparse
import math
import csv
import os 
import sys 
import glob 

delta_sig=20 # valores escogido de forma prueba/error que mejores se ajustaban a las imagenes de peor calidad
ratio_sig=0.26 #max/min
max_sig= delta_sig*ratio_sig
min_sig= -delta_sig*(1-ratio_sig)
j=0
k=0

def sigma_correction(x): # no sigma function, only used to normalize values
    x=x-min(x)
    x=(max_sig-min_sig)*(x/max(x)) 
    return x


def contrast_corretion(x): # second correction for invertion

    x=255*x
    x=255-x #inverting color
    x=x-min(x)
    x=255*(x/max(x))
    return x.astype(int)



def sigmoid(x): 
    x = x+min_sig
    for i in range(0,len(x)):
    	s[i] = 1/(1+math.exp(-x[i]))  # used function -> https://en.wikipedia.org/wiki/Sigmoid_function
    return s

filepath=glob.glob("**/*.jpg",recursive=True)

   
name_in=filepath #args.in_name

f=open('final.csv','w')
writer=csv.writer(f)

while j<len(name_in):
    
    im = Image.open("%s" %name_in[j]).convert('L')
    path_temp=name_in[j].split("/")
    
    if path_temp[2]=='caps' or  path_temp[2]=='Caps' or path_temp[2]=='CAPS':
        k=3
        path_temp[k]=path_temp[k].replace('.jpg','').upper()
    else:
        k=2
        path_temp[k]=path_temp[k].replace('.jpg','').lower()

    im_temp_np = np.array(im)  

    x=im_temp_np.reshape((im_temp_np.shape[0]*im_temp_np.shape[1],1))
    s=np.zeros((x.shape[0],x.shape[1]))
    

    x=sigma_correction(x)

    s=sigmoid(x)

    s=contrast_corretion(s)

    s_list=s[:,0].tolist()
    
    writer.writerow([path_temp[1],path_temp[k],s_list])

    s=s.reshape((-1,28))


    name_in[j]=name_in[j].replace('.jpg','.png')
    im_t=Image.fromarray(s.astype('uint8'))
    
    im_t.save("%s" %name_in[j], format="png")
    j=j+1   

f.close()
