import csv
from pathlib import Path
import nltk

# Download the punkt tokenizer if not already available
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

def chunk_text(text, max_words=200, overlap=50):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        # Check if adding this sentence exceeds max_words
        if current_length + word_count > max_words:
            # Save the current chunk
            chunks.append(' '.join(current_chunk))
            # Prepare next chunk with overlap
            overlap_words = ' '.join(' '.join(current_chunk).split()[-overlap:])
            current_chunk = [overlap_words] if overlap_words else []
            current_length = len(overlap_words.split())
        # Add sentence to current chunk
        current_chunk.append(sentence)
        current_length += word_count

    # Add any remaining text as the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def chunk_articles(input_csv, output_csv, max_words=200, overlap=50):
    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ['url', 'title', 'publish_date', 'chunk_id', 'text']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            url = row['url']
            title = row['title']
            date = row.get('publish_date', '')
            text = row['text']
            chunks = chunk_text(text, max_words, overlap)
            for idx, chunk in enumerate(chunks):
                writer.writerow({
                    'url': url,
                    'title': title,
                    'publish_date': date,
                    'chunk_id': idx,
                    'text': chunk
                })

if __name__ == "__main__":
    # Adjust paths as needed
    input_csv = "data/articles/articles.csv"
    output_csv = "data/articles/chunks.csv"
    chunk_articles(input_csv, output_csv)
    print(f"Chunks saved to {output_csv}")