import os
import json
import pandas as pd


def analyze_dataset(file_path: str):
    #Analyzes CSV or JSON Dataset And Exports Report to JSON.

    #Handle Missing File
    if not os.path.exists(file_path):
        print(f"Error: The File '{file_path}' Does Not Exist.")
        return

    #Identify File Format and Read Dataset
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    try:
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext == '.json':
            df = pd.read_json(file_path)
        else:
            #Handle Unsupported File Format
            print(f"Error : Unsupported File Format '{ext}'. Please Provide .csv or .json File.")
            return

    except pd.errors.EmptyDataError:
        print("Error : The Provided CSV File is Completely Empty.")
        return
    except ValueError as e:
        print(f"Error : Invalid JSON Structure or Syntax. Details: {e}")
        return
    except Exception as e:
        print(f"Error Reading File: {e}")
        return

    #Handle Empty DataFrame (e.g., Valid JSON Structure Like [] or Empty Headers)
    if df.empty:
        print("Error: The File Contains No Records to Analyze.")
        return

    #Perform Analysis
    num_records, num_fields = df.shape
    field_names = df.columns.tolist()
    missing_values = df.isnull().sum().to_dict()

    #Identify Data Types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    text_cols = df.select_dtypes(include=['object', 'string', 'category']).columns.tolist()

    #Generate Statistical Summary
    summary_dict = {}
    if numeric_cols:
        summary_dict['numeric_summary'] = df[numeric_cols].describe().to_dict()
    if text_cols:
        summary_dict['textual_summary'] = df[text_cols].describe().to_dict()

    #Assemble Analysis Report
    report = {
        "file_name": os.path.basename(file_path),
        "file_format": ext.replace('.', '').upper(),
        "num_records": num_records,
        "num_fields": num_fields,
        "field_names": field_names,
        "missing_val_per_field": missing_values,
        "field_classification": {
            "numeric_fields": numeric_cols,
            "textual_fields": text_cols
        },
        "dataset_summary": summary_dict
    }

    # 4. Display Results in Terminal
    
    print("DATASET ANALYSIS REPORT")
   
    print(f"File Analyzed : {report['file_name']} ({report['file_format']})")
    print(f"Total Records : {num_records}")
    print(f"Total Fields : {num_fields}")
    print(f"Field Names : {', '.join(field_names)}")
    print(f"Numeric Fields : {', '.join(numeric_cols) if numeric_cols else 'None'}")
    print(f"Textual Fields : {', '.join(text_cols) if text_cols else 'None'}")
    
    print("\nMissing Values Per Field:")
    for field, count in missing_values.items():
        print(f"  - {field}: {count}")

    print("\nStatistical Summary (Sample):")
    print(df.describe(include='all'))

    # 5. Save Report to JSON
    output_filename = f"analysis_report_{os.path.splitext(report['file_name'])[0]}.json"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, default=str)
        print(f"\nSuccess: Analysis Report Saved To '{output_filename}'.\n")
    except Exception as e:
        print(f"Error Saving JSON Report: {e}")


if __name__ == "__main__":
    user_file = input("Enter The Path To Your CSV or JSON File: ").strip()
    analyze_dataset(user_file)