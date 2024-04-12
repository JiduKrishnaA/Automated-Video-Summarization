from summarizer import Summarizer
import os

def count_sentences_in_text(text_content):
    # Counting the number of sentences in the text content
    return text_content.count('.') + text_content.count('!') + text_content.count('?')

def summarize_text(input_path, output_path):
    # Read text file
    with open(input_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Count the number of sentences in the text content
    num_sentences_in_text = count_sentences_in_text(text_content)

    # Calculate the number of sentences for the summary (15% of the total sentences)
    num_sentences_in_summary = int(0.158 * num_sentences_in_text)

    # Use bert-extractive-summarizer to summarize the text content
    summarizer = Summarizer()
    summarized_text = summarizer(text_content, num_sentences=num_sentences_in_summary)

    # Write the summarized text to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(summarized_text)

if __name__ == "__main__":
    # Specify the path to the input text file
    input_text_path = r'D:\D-KTS\Audgen\aud_text\output.txt'

    # Specify the path for the output summary file
    output_summary_path = "F:\out.txt"

    # Summarize the text content
    summarize_text(input_text_path, output_summary_path)
