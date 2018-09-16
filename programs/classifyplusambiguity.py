#author:Lorenzo Vianello 1805889
#THIS IS THE CODE TO TEST 4 CLASS OF BOAT, I CONSIDER ONLY THE 2 BIGGERS PROBABILITIES , DON'T WATCH THE OTHERS, IF FIRST<SECOND*ALPHA THEN AMBIGUITY

#libraries for write read and execute from prompt
import os
from subprocess import Popen,PIPE

in_file = open("/home/lorenzo/Scrivania/sc5Test/ground_truth.txt","r")

dictB={}
l=0
#constant that represent the coefficient that the program multiply for the second bigger probability  
alpha=2
#open file ground_truth inside sc5Test to take the names of images and the types
while 1:
    in_line=in_file.readline()
    if in_line=="":
        break
    i=0
    keyB=""
    valB=""
    for index in range(0,len(in_line)):
        if in_line[index]==";":
             i=1
        elif i==0:
             keyB=keyB+in_line[index]
        elif i==1:
             valB=valB+in_line[index]
    if(valB == "Gondola\n") or (valB == "Ambulanza\n") or (valB == "Barchino\n") or (valB == "Alilaguna\n") or (valB == "Patanella\n") or (valB == "Snapshot Barca Parziale\n"):
        dictB[keyB]=valB
        l=l+1

print("NOW WILL BE CLASSIFY",l,"IMAGES, WAIT UNTIL FINISH\n___________________________________\n")
#dir_image="//home//lorenzo//Scrivania//sc5Test//"
#variabiles which take count of the time that the algorithm correctly classify an image and also the cases in wich in image is ambiguous 
number_matching=0
number_mismatching=0
number_ambiguity=0
#variabiles that take the first and the second types whit bigger probability and their probability
type1=""
prob1=""
type2=""
prob2=""
i=0
k=0
#for each image execute on the prompt the comand to classify it, collect the results and confront them with the real values
for x in dictB.keys():
    print( k,":\tName: ",x," \tType: ",dictB[x])
    k=k+1
    imagename=x
	#command to execute in the prompt to classify an image
    cmd= "bazel-bin/tensorflow/examples/label_image/label_image --graph=/home/lorenzo/Scrivania/output_graph.pb --labels=/home/lorenzo/Scrivania/output_labels.txt --output_layer=final_result --image=/home/lorenzo/Scrivania/sc5Test/"+imagename+" --input_layer=Mul "
    l=Popen(cmd, stdout=PIPE,stderr=PIPE,shell=True)
	#collect what the command execution return
    (out,err) = l.communicate();
    #print (err)
    in_line=str(err)
    i=0
    word=""

    for index in range(0,len(in_line)):
        if (in_line[index].isalnum() or in_line[index]=="." or in_line[index]=="\n") and i<5:
             word=word+in_line[index]
             f=word.replace(".","").replace(" ","")
             #print(f)

             if((word == "gondola") or (word == "ambulanza") or (word== "barchino") or (word == "alilaguna"))and i==0:
                     type1=word
                     word=""
                     i=1
             if  f.isdigit() and i==1:
                     mom=float(word)
                     if mom>0 and mom<1:
                         prob1=mom
                         word=""
                         i=2
             if((word == "vaporettoactv") or (word == "ambulanza") or (word== "barchino") or (word == "alilaguna") or (word == "mototopo") or (word == "lanciafino10mbianca") or (word == "patanella") or (word == "lanciamaggioredi10mbianca") or (word == "polizia") or (word == "vigilidelfuoco") or (word == "lanciafino10mmarrone") or (word == "water"))and i==2:
                     type2=word
                     word=""
                     i=3
             if( f.isdigit() and i==3):
                     mom=float(word)
                     if mom>0 and mom<1:
                         prob2=mom
                         word=""
                         i=10
        else:
            word=""     
    print(type1,prob1,type2,prob2) 
    if prob1>float(prob2*alpha): 
        if((type1 == "gondola") or (type1 == "ambulanza") or (type1== "barchino") or (type1 == "alilaguna")):
            if type1 in dictB[x].lower():
                number_matching=number_matching+1
                print("match")
            else:
                number_mismatching=number_mismatching+1
                print("mismatch")
            i=1 
    else:
        number_ambiguity=number_ambiguity+1
        print("ambiguity")

print("NUMBER OF CORRECT CLASSIFY IMAGES:",number_matching)
print("NUMBER OF NOT CORRECT CLASSIFY IMAGES:",number_mismatching)
print("NUMBER OF CASES CONSIDERED AMBIGUOUS ARE:",number_ambiguity)




