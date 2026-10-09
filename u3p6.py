import os
import json
import datetime
from google import genai


client = genai.Client(api_key="AQ.Ab8RN6IchY-eZdwtvubIKZvO_gQLTnEMamhh7pHvaBcWZA_qQA")

def log_status(filename, status, error="None"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] File: {filename} | Status: {status} | Error: {error}\n"
    
    with open("app.log", "a") as log_file:
        log_file.write(log_line)

def process_file(file_path):
    filename = os.path.basename(file_path)

    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    
    if not text:
        print(f"Skipping empty file: {filename}")
        log_status(filename, "Skipped", "File is empty")
        return

    word_count = len(text.split())

    prompt = f"""
    Summarize the following text and respond ONLY with a valid JSON object.
    Do not include markdown tags like ```json or markdown formatting.

    JSON fields required:
    - "title": a short title or main topic
    - "summary": concise summary in 2-3 lines
    - "keywords": list of key terms (array of strings)

    Text to summarize:
    {text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )
        raw_text = response.text.strip()
        
        # Strip code block markers if the model includes them
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            raw_text = raw_text.rsplit("```", 1)[0].strip()

        # 4. Safe JSON parsing
        data = json.loads(raw_text)

        required_fields = ["title", "summary", "keywords"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        data["word_count"] = word_count
        data["source_file"] = filename

        os.makedirs("output", exist_ok=True)
        
        with open("summaries.json", "a", encoding="utf-8") as out_file:
            json.dump(data, out_file, indent=4)

        print(f"Successfully processed: {filename}")
        log_status(filename, "Success")

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON for {filename}")
        log_status(filename, "Failed", f"JSON Error: {str(e)}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        log_status(filename, "Failed", str(e))

def main():
    user_input = input("Enter the file or folder path: ").strip()

    if not os.path.exists(user_input):
        print("Invalid path. File or folder does not exist.")
        return
        
    files_to_process = []
    if os.path.isfile(user_input) and user_input.endswith(".txt"):
        files_to_process.append(user_input)
    elif os.path.isdir(user_input):
        for fname in os.listdir(user_input):
            if fname.endswith(".txt"):
                files_to_process.append(os.path.join(user_input, fname))

    if not files_to_process:
        print("No .txt files found.")
        return

    total = len(files_to_process)
    print(f"\nFound {total} file(s) to process.\n")

    for index, file_path in enumerate(files_to_process, start=1):
        print(f"[{index}/{total}] Processing {os.path.basename(file_path)}...")
        process_file(file_path)

    print("\n Processing complete! Check 'output/summaries.json' and 'app.log'.")
    
if __name__ == "__main__":
    main()
