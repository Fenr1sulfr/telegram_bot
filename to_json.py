import  json
ar=[]
with open("Fuckwords.txt",encoding='utf-8') as file:
    for i in file:
        n=i.lower().split('\n')[0]
        if n !='':
            ar.append(n)

with open("badword.json",'w',encoding='utf-8') as jsonfile:
    json.dump(ar,jsonfile)