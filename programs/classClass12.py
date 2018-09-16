#author:Lorenzo Vianello 1805889
#THIS IS THE CODE TO TEST 12 CLASS OF BOAT, I CONSIDER ONLY THE MAX, DON'T WATCH THE OTHERS
#THE CLASS I WATCH ARE: ALILAGUNA, AMBULANZA, BARCHINO, LANCIAFINO10MBIANCA, LANCIAFINO10MMARRONE, LANCIAMAGGIORE10MBIANCA, MOTOTOPO, PATANELLA, POLIZIA, VAPORETTOACTV, VIGILI DEL FUOCO, WATER

#libraries for write read and execute from prompt
import os
from subprocess import Popen,PIPE

 
in_file = open("/home/lorenzo/Scrivania/sc5Test/ground_truth.txt","r")

dictB={}
l=0
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
    if(valB == "Patanella\n") or (valB == "Ambulanza\n") or (valB == "Barchino\n") or (valB == "Alilaguna\n") or (valB == "Mototopo\n") or (valB == "Snapshot Acqua\n") or (valB == "Polizia\n") or (valB == "Lancia: fino 10 m Bianca\n") or (valB == "Lancia: fino 10 m Marrone\n") or  (valB == "Lancia: maggiore di 10 m Bianca\n") or (valB == "Vaporetto ACTV\n"):
        dictB[keyB]=valB
        l=l+1

print("NOW WILL BE CLASSIFY",l,"IMAGES, WAIT UNTIL FINISH\n___________________________________\n")
#dir_image="//home//lorenzo//Scrivania//sc5Test//"
#variabiles which take count of the time that the algorithm correctly classify an image 
number_matching=0
number_mismatching=0
i=0
k=0
#for each image execute on the prompt the comand to classify it, collect the results and confront them with the real values
for x in dictB.keys():
    print( k,":\tName: ",x," \tType: ",dictB[x])
    k=k+1
    imagename=x
	#command to execute in the prompt to classify an image
    cmd= "bazel-bin/tensorflow/examples/label_image/label_image --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt --output_layer=final_result --image=/home/lorenzo/Scrivania/sc5Test/"+imagename+" --input_layer=Mul "
    l=Popen(cmd, stdout=PIPE,stderr=PIPE,shell=True)
	#collect what the command execution return
    (out,err) = l.communicate();
    #print (err)
    in_line=str(err)
    i=0
    word=""
    for index in range(0,len(in_line)):
        if in_line[index].isalnum():
             word=word+in_line[index]
             if((word == "vaporettoactv") or (word == "ambulanza") or (word== "barchino") or (word == "alilaguna") or (word == "mototopo") or (word == "lanciafino10mbianca") or (word == "patanella") or (word == "lanciamaggioredi10mbianca") or (word == "polizia") or (word == "vigilidelfuoco") or (word == "lanciafino10mmarrone") or (word == "water"))and i==0:
                 print(word, dictB[x])
                 if (word in dictB[x].lower().replace(" ","").replace(":","")) or (word== "water" and dictB[x]=="Snapshot Acqua\n") :
                     number_matching=number_matching+1
                     print("match")
                 else:
                     number_mismatching=number_mismatching+1
                     print("mismatch")
                 i=1
        else:
             word=""
print("NUMBER OF CORRECT CLASSIFY IMAGES:",number_matching)
print("NUMBER OF NOT CORRECT CLASSIFY IMAGES:",number_mismatching)

