import os

model  = "gemini 2,5"
temp = 0.9
max_tkn= 2048
api_ver = "v1beta"


print(f"Model Name : {model}")
print(f"Temperature : {temp}")
print(f"Maximum Tokens : {max_tkn}")
print(f"API Version : {api_ver}")


stud1 = {
    "name" : "shubham",
    "Coyurce" : "PGDCA",
    "Sem" : 1,
    "Mark" : 97
}

print(stud1)

uodate_marks = int(input("Enter Update Marks : "))
stud1["Mark"]= uodate_marks

print(stud1)



def check_file_status():
    
    file = input("Enter File name of the text file: ").strip()

    
    if os.path.isfile(file):
        
        file_size = os.path.getsize(file)
        print("\n File Name : ", file)
        print(f"File Size : {file_size} bytes")

        
        if file_size == 0:
            print(" File is Empty ")
        else:
            print(" File is Non-Empty ")
    else:
        # Display an appropriate error message
        print(f"\nError: This file '{file}' does not exist ")

if __name__ == "__main__":
    check_file_status()