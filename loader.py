import ABSOLUTE
import LINKING
type_of_loader=input("Enter type of file\n")
if type_of_loader=="SIC":
    ABSOLUTE.loading()
else:
    start=input("Enter the starting address\n")
    sequence=input("Enter the Sequence\n")
    LINKING.loading(start,sequence)
    
