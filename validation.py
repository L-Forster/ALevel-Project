def validate_scores():    
    ## Removing '#'
    highScores = open("highScores.txt","r")
    lines = highScores.readlines()
    highScores = open("highScores.txt","w")
    for i in range(len(lines)):
        if str(lines[i])[0] == '#':
            lines[i] = str(lines[i])[1:]

    ##If the data is not an integer, remove it 
    invalid = True
    i=0
    while invalid:
        if len(lines) > i: #when not all indexes have been validated
            temp_data = lines[i].strip("\n")
            try:  #try to cast the data as an integer
                int(temp_data)
            except:# if this doesn't work, remove it from the list
                lines.remove(lines[i])
                i-=1 #removes 1 from i, so that it will check this index again in the next cycle of the loop
        else: 
            invalid = False
        i = i +1

    
    ##If the data is negative or not a multiple of 100
    for i in range(len(lines)):    
        if int(lines[i].strip('\n')) < 0 or int(lines[i].strip('\n'))%100 != 0:
            lines[i] = "0\n"  # set that data to 0
    
   
           
    highScores = open("highScores.txt","w")  
    ##If there is < 5 pieces of data
    while len(lines) < 5:
        lines.append("0\n")
            
         
    ##if there are > 5 pieces of data
    sorted = False #sorts the data in descending order.
    if len(lines) > 5:
        while not(sorted):
            passes= 0
            for i in range(len(lines)-1):
                if int(lines[i]) < int(lines[i+1][0:]) or int(lines[i]) < int(lines[i+1]):
                    temp=lines[i]
                    lines[i] = lines[i+1]
                    lines[i+1]=temp
                    passes += 1
            if passes == 0:
                sorted = True
      
    #removes the data past fifth
        while len(lines) > 5:
            lines.remove(lines[5])   
            
            
    #If it does not contain '\n' at the end
    for i in range(len(lines)-1):
        if "\n" not in lines[i]:
            lines[i] = (lines[i]+str("\n")) # adds '\n'
    
    #putting the new scores into the file.
    for i in range(len(lines)):  # for every line
        highScores.write(lines[i]) #add the line to the file
