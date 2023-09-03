import pandas as pd
def loading():
    file=open("input.txt","r")
    mylist=[]
    t_records=[]
    my_temp_t_records=[]
    for line in file:
        mylist.append(line.rstrip("\n").split("."))
        if line.startswith("T"):
            t_records.append(line.rstrip("\n").split("."))
            my_temp_t_records.append(line.rstrip("\n").split(".")[3:])
    starting_address=mylist[0][2]
    length=mylist[0][3]
    ending_address=hex(int(starting_address,16)+int(length,16))
    memory_addresses=[]
    memory_addresses.append(hex(int(starting_address,16)))
    mytempaddress=int(starting_address,16)
    while int(ending_address,16) >mytempaddress:
        mytempaddress+=16
        memory_addresses.append(hex(int(mytempaddress)))
    colomns=["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
    memory=pd.DataFrame(index=memory_addresses,columns=colomns,data="x")

    object_code_for_memory=[]
    print(t_records)
    for t_rec in t_records:
        object_codes=t_rec[3:]
        string_of_object_codes=""
        for elemnt in object_codes:
            string_of_object_codes+=elemnt
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
        print(start)
        begin=start[5]
        start=start[:5]+"0"
        print(start,begin,memory,sep="\n")
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
    gui=show(memory)
    