import pandas as pd
def loading(start,seq):
    sequece=seq.split("+")
    print(seq)
    starting_address=int(start,16)
    file=open("input.txt")
    data=[]
    number_of_progs=0
    i=-1
    indicies=[]
    for line in file:
        data.append(line.rstrip("\n").split("."))
        i+=1
        if line.startswith("H"):
            number_of_progs+=1
            indicies.append(i)
    indicies.append(len(data))
    mylist=[]
    for i in range(0,len(indicies)-1):
        mylist.append(data[indicies[i]:indicies[i+1]])
    length_of_all_progs=0
    for prog in mylist:
        length_of_all_progs+=int(prog[0][3],16)
    length_of_all_progs=hex(length_of_all_progs)
    correct_order_progs=[]
    for sec in sequece:
        for i in range(0,len(mylist)):
            if mylist[i][0][1]==sec:
                correct_order_progs.append(mylist[i])
    tmp_address=starting_address
    for prog in correct_order_progs:
        for record in prog:
            if record[0]=="H":
                record[2]=hex(int(record[2],16)+tmp_address)[2:].zfill(6)
                addition=int(record[3],16)
            elif record[0]=="M":
                record[1]=hex(int(record[1],16)+tmp_address)[2:].zfill(6)
            elif record[0]=="T":
                record[1]=hex(int(record[1],16)+tmp_address)[2:].zfill(6)
            elif record[0]=="D":
                for i in range(0,len(record)):
                    if record[i].startswith("0"):
                        record[i]=hex(int(record[i],16)+tmp_address)[2:].zfill(6)
        tmp_address+=addition


    ##########################################################################################

    starting_address=hex(starting_address)[2:].zfill(6)
    ending_address=hex(int(starting_address,16)+int(length_of_all_progs[2:],16))
    memory_addresses=[]
    memory_addresses.append(hex(int(starting_address,16)))
    mytempaddress=int(starting_address,16)
    while int(ending_address,16) >mytempaddress:
        mytempaddress+=16
        memory_addresses.append(hex(int(mytempaddress)))
    colomns=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    memory=pd.DataFrame(index=memory_addresses,columns=colomns,data="x")



    d_records=[]
    for prog in correct_order_progs:
        for record in prog:
            if record[0]=="D":d_records.append(record[1:])
    for prog in correct_order_progs:
        for record in prog:
            l=[]
            if record[0]=="H":
                l.append(record[1])
                l.append(record[2])
                d_records.append(l)
    file=open("enternalsymboltable.txt","w")
    for rec in d_records:
        for i in range(0,len(rec),2):
            file.write(rec[i]+" "+rec[i+1]+"\n")
    #print(d_records)
    s={}
    for rec in d_records:
        for i in range(0,len(rec),2):
            s[rec[i]]=rec[i+1]
    print(s)

    M_record=[]
    for prog in correct_order_progs:
        for record in prog:
            if record[0]=="M":M_record.append(record[1:])
    #print(M_record)
    t_records=[]
    for prog in correct_order_progs:
        for record in prog:
            if record[0]=="T":t_records.append(record)
    object_code_for_memory=[]

    for t_rec in t_records:
        addresses_of_trecords=t_rec[1:3]
        minimum=hex(int(addresses_of_trecords[0],16))
        maximum=hex(int(addresses_of_trecords[0],16)+int(addresses_of_trecords[1],16))
        object_codes=t_rec[3:]
        string_of_object_codes=""
        for elemnt in object_codes:
            string_of_object_codes+=elemnt
        for m_rec in M_record:
            if int(m_rec[0],16)>=int(minimum[2:],16) and int(m_rec[0],16)<=int(maximum[2:],16):
                print(m_rec,minimum,string_of_object_codes)########################################
                modi=int(m_rec[0],16)-int(minimum[2:],16)
                to_be_added_or_subtracted=m_rec[2][1:]
                operation=m_rec[2][:1]
                to_be_added_or_subtracted=s[to_be_added_or_subtracted]
                if m_rec[1]=="05":
                    if operation=="+":
                        added=hex(int(to_be_added_or_subtracted,16)+int(string_of_object_codes[modi*2+1:modi*2+6],16))[2:].zfill(5)
                        string_of_object_codes=string_of_object_codes[:modi*2+1]+added+string_of_object_codes[modi*2+6:]
                        print(string_of_object_codes)
                    else:
                        added=hex(int(string_of_object_codes[modi*2+1:modi*2+6],16)-int(to_be_added_or_subtracted,16))[2:].zfill(5)
                        print(string_of_object_codes)
                        if added.startswith("-"): 
                            print(int(added,16))
                            added=hex(int(added,16) &0xfffff)
                            print(added)
                            added=added[2:].zfill(5)
                        else:
                            added=added[2:].zfill(5)
                        string_of_object_codes=string_of_object_codes[:modi*2+1]+added+string_of_object_codes[modi*2+6:]
                else:
                    if operation=="+":
                        added=hex(int(to_be_added_or_subtracted,16)+int(string_of_object_codes[modi*2:modi*2+6],16))[2:].zfill(6)
                        string_of_object_codes=string_of_object_codes[:modi*2]+added[-6:]+string_of_object_codes[modi*2+6:]
                        print(string_of_object_codes)                
                    else:
                        
                        added=hex(int(string_of_object_codes[modi*2:modi*2+6],16)-int(to_be_added_or_subtracted,16))
                        if added.startswith("-"): 
                            print(int(added,16))
                            added=hex(int(added,16) &0xffffff)
                            print(added)
                            added=added[2:].zfill(6)
                        else:
                            added=added[2:].zfill(6)
                        string_of_object_codes=string_of_object_codes[:modi*2]+added[-6:]+string_of_object_codes[modi*2+6:]
                        print(string_of_object_codes)
                        
                    #print(string_of_object_codes[modi*2:modi*2+6])
        object_code_for_memory.append(string_of_object_codes)
    object_codes_to_be_used=[]
    for element in object_code_for_memory:
        tmplist=[]
        i=1
        lengthh=len(element)
        for j in range(0,lengthh-1,2):
            tmpstr=element[j]+element[i]
            i+=2
            tmplist.append(tmpstr)
        object_codes_to_be_used.append(tmplist)
    for i in range(0,len(t_records)):
        start=t_records[i][1]
        begin=start[5]
        start=start[:5]+"0"
        object_code=object_codes_to_be_used[i]
        for code in object_code:
            start=hex(int(start,16))
            memory[begin][start]=code
            begin=int(begin,16)+1
            begin=hex(begin)[2:]
            if begin=="10":
                start=int(start[2:],16)+16
                start=hex(start)[2:]
                begin="0"
    with open("memory.txt","w") as f:
        string=memory.to_string()
        f.write(string)
    from pandasgui import show
    show(memory)
    
