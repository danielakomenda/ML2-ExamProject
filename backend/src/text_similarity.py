import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine


def get_bert_embeddings(text, model, tokenizer):
    # Ensure the input is properly formatted as a list even if it's a single string
    if isinstance(text, str):
        text = [text]  # Wrap text in a list to handle it uniformly
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state
    mean_embeddings = embeddings.mean(dim=1)  # Average across the sequence length dimension
    return mean_embeddings[0]  # Return the first (and only) item to keep it consistent



def calculate_similarity(text1, text2):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    embeddings1 = get_bert_embeddings(text1, model, tokenizer)
    embeddings2 = get_bert_embeddings(text2, model, tokenizer)
    
    vec1 = embeddings1.numpy()  # Should already be 1-D
    vec2 = embeddings2.numpy()  # Should already be 1-D

    # Debugging print statements to ensure the dimensions are as expected
    print(vec1.shape)
    print(vec2.shape)

    similarity = 1 - cosine(vec1, vec2)
    return similarity


def notes_similarity(data):
    results = dict()
    for k, v in data["recommended"].items():
        v2 = data["manually"][k]
        results[k]=round(calculate_similarity(v, v2), 5)
    return results


def text_similarity(data):
    result = round(calculate_similarity(data["recommended"], data["manually"]), 5)
    return result
