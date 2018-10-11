import numpy as np
file=open("confidence_dict.txt","r",encoding="UTF-8")
list_str=file.readlines()
list_sp1=[]
dict_con={}
for item in list_str:
    str1=item.split(":")
    con=str1[1].split(" ")
    pos=int(con[0])
    neg=int(con[1])
    con_val=-1
    if(pos+neg>20):
        con_val=pos/(pos+neg)
    dict_con[str1[0]]=con_val
#print(dict_con)
np.save('confidence.npy', dict_con) 

