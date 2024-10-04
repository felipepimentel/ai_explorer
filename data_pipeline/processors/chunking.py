import nltk
nltk.download('punkt')

def chunk_text(text, chunk_size=1000, overlap=100):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_size = len(sentence)
        if current_size + sentence_size <= chunk_size:
            current_chunk.append(sentence)
            current_size += sentence_size
        else:
            chunks.append(' '.join(current_chunk))
            overlap_size = sum(len(s) for s in current_chunk[-3:])  # Overlap with last 3 sentences
            current_chunk = current_chunk[-3:]
            current_size = overlap_size
            current_chunk.append(sentence)
            current_size += sentence_size

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks