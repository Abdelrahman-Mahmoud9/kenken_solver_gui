import codecs

def ReadInput(fileName):
        
    file = open('inputs/'+fileName,'r')
    fileContents=[]
    for line in file:
        fileContents.append(line.strip("\n"))

    N = int(fileContents[0].replace('\ufeff', ''))

    Cliques=[]
    for i in range(1,len(fileContents)):
        cl=[]

        s = fileContents[i].replace("[","").replace("]","").replace("(","").split(" ")
        if(s[0]==""):
            break;

        coordinates = s[0].split("),")
        operation = s[1]
        result = s[2]

        if(operation == "add"):
            cl.append("+")
        elif(operation == "sub"):
            cl.append("-")
        elif(operation == "mult"):
            cl.append("*")
        elif(operation == "div"):
            cl.append("/")
        else:
            cl.append(None)

        cl.append(int(result))
        cm=[]

        for coord in coordinates:
            
            c = coord.replace(",","").replace(")","")       
            cm.append(c)

        cl.append(cm)
        Cliques.append(cl)

    return [int(N),Cliques]








