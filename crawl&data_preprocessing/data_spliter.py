import csv
read_all_mode=0
if(read_all_mode==0):
    #user=['test']
    user=['James','Gene','Justin','Ting','Jam','Elsun','Frank','Justin_2']
else:
    user=['ALL']
hyper_link=[]
label_list=[]
author_list=[]
comment_list=[]
comment_idx=0
for i in range(0,len(user)):
    file=open("comment_label_"+str(user[i])+".txt",'r',encoding='UTF-8')
    input_list=file.readlines()
    if(read_all_mode==0):
        for i in range(0,len(input_list)):
            item=input_list[i]
            if(item.find("/bbs/Gossiping/")!=-1 and len(item.split(" "))==1):#hyperlink
                hyper_link.append([item.replace("\n",""),comment_idx])
                #print(item)
                
            else:#comment (1)label (2)user_name (3)content
                comment=item.split(" ")
                label_list.append(comment[0])
                author_list.append(comment[1].replace(":",""))
                comment_list.append(comment[2:])
                comment_idx=comment_idx+1
                #print("label:",comment[0],"user_name::",comment[1],"content:",comment[2:])
    else:
        for i in range(0,len(input_list)):
            item=input_list[i]
            comment=item.split(":")
            author_list.append(comment[0])
            comment_list.append(comment[1:])
            #print("label:",comment[0],"user_name::",comment[1],"content:",comment[2:])
file_url=open("train_url.txt",'w',encoding='UTF-8')
file_label=open("train_label.txt",'w',encoding='UTF-8')
file_author=open("train_author.txt",'w',encoding='UTF-8')
file_comment=open("train_comment.txt",'w',encoding='UTF-8')

for item in hyper_link:
    output=str(item[0])+","+str(item[1])+"\n"
    file_url.write(output)
for item in label_list:
    output=str(item)+"\n"
    file_label.write(output)
for item in author_list:
    output=str(item)+"\n"
    file_author.write(output)
for item in comment_list:
    output=""
    for word in item:
        output=output+str(word)
    output=output
    file_comment.write(output)


    