import json
import pandas as pd


num_of_stud = int(input("Enter Number of Student : "))

student = []
print(" : Fill Student Details : ")
for i in range(num_of_stud):
    print(f"\nEnter details for Student {i + 1}:")
    
    name = input("Name: ")
    age = int(input("Age: "))
    course = input("Course: ")
    
    
    student_data = {
        "name": name,
        "age": age,
        "course": course
    }

    student.append(student_data)

print(student)

with open('data.json', 'r') as file:
    data = json.load(file)

new_data = student_data
data.append(new_data)

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

print(data)


df = pd.read_json('data.json')

print(df.head(2))

print(df.tail(2))

num_row = df.shape[0]
num_column = df.shape[1]

print(f"Rows: {num_row}, Columns: {num_column}")

print(df.columns)
print(df.dtypes)