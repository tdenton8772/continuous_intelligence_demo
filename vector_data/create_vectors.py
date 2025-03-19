import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3
from langchain_aws.embeddings import BedrockEmbeddings
import json
import time
import uuid

session = boto3.Session(profile_name="default")
bedrock_client = session.client(service_name='bedrock-runtime', 
                              region_name='us-east-1')
# bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",
#                                        client=bedrock_client)
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",
                                        client=bedrock_client)



# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))

nltk.download('stopwords')
nltk.download('wordnet')


def clean_text(text):
    raw_text = text
    text = text.lower() 
    text = re.sub(r'https?://\S+|www\.\S+', '', text) 
    text = re.sub(r'<.*?>', '', text)  
    text = re.sub(r'@\w+', '', text)  
    text = re.sub(r'#\w+', '', text)  
    emoticons = {':)': 'smile', ':-)': 'smile', ':(': 'sad', ':-(': 'sad'}
    words = text.split()
    words = [emoticons.get(word, word) for word in words]
    text = " ".join(words)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)  
    text = re.sub(r'\s+', ' ', text, flags=re.I) 
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    stemmer = PorterStemmer()
    text = ' '.join(stemmer.stem(word) for word in text.split())
    lemmatizer = WordNetLemmatizer()
    text = ' '.join(lemmatizer.lemmatize(word) for word in text.split())

    return text

def extract_text_from_pdf(pdf_path):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return "\n".join(extracted_text)


def split_text_into_chunks(text, chunk_size=256, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)

pdf_path = "ttahtf_lookinside.pdf"  # Your PDF file
raw_text = extract_text_from_pdf(pdf_path)
split_text = split_text_into_chunks(raw_text)

records = []
for split in split_text:
    cleaned_text = clean_text(split)
    response = bedrock_embeddings.embed_query(cleaned_text)

    records.append({"original_text": split, 
                    "vector_data": response, 
                    "id": str(uuid.uuid4())})
    if len(records) == 10:
        with open(f"./data/{int(time.time())}.json", "w") as f:
            f.write(json.dumps(records, indent=3))
        records = []
with open(f"./data/{int(time.time())}.json", "w") as f:
    f.write(json.dumps(records))
