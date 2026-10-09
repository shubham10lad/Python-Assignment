import sys
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def simulated_summarize(text):
    sentences = text.split(".")
    cleaned_sentences = [s.strip() for s in sentences if s.strip()]
    
    if not cleaned_sentences:
        return "No content to summarize."
    
    summary = ". ".join(cleaned_sentences[:2]) + "."
    return summary

def main():
    logging.info("Program started")

    parser = argparse.ArgumentParser(description="Simple Text Summarizer")
    parser.add_argument("--input", required=True, help="Input text file path")
    parser.add_argument("--output", required=True, help="Output text file path")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        logging.error("Invalid command-line arguments")
        sys.exit(1)

    input_file = args.input
    output_file = args.output

    try:
        logging.info(f"Processing input file: {input_file}")
        with open(input_file, "r") as f:
            text = f.read()

        if not text.strip():
            logging.error("Input file is empty")
            print("Error: The input file is empty.")
            sys.exit(1)

        logging.info("Generating summary")
        summary = simulated_summarize(text)

        logging.info(f"Saving summary to output file: {output_file}")
        with open(output_file, "w") as f:
            f.write(summary)

        print("Summarization completed successfully!")

    except FileNotFoundError:
        logging.error(f"Missing input file: {input_file}")
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        logging.error(f"API/model failure or unexpected error: {e}")
        print(f"An error occurred: {e}")

    logging.info("Program ended")

if __name__ == "__main__":
    main()