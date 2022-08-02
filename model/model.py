import pandas as pd
import streamlit as st
import torch

from transformers import BertTokenizer
from tqdm import tqdm

from model.model_class import BertClassifier


def prediction(reviews, model, tokenizer, MAX_LEN=41):
    result = ""
    
    if reviews:
        input_ids, attention_mask, _ = bert_tokenizer(reviews, MAX_LEN, tokenizer)
        with torch.no_grad():
            pred = model(input_ids, attention_mask)
        df = pd.DataFrame([reviews, pred], index=["리뷰", "긍정확률"]).T
        df["감정"] = df["긍정확률"].apply(lambda x: "긍정" if x >= 0.5 else "부정")
        result = {
            "all": df["리뷰"],
            "positive": df[df["감정"] == "긍정"]["리뷰"],
            "negative": df[df["감정"] == "부정"]["리뷰"],
        }
        
    return result


@st.cache
def load_model():
    model = BertClassifier("klue/bert-base", linear_size=256, num_class=1)
    model.load_state_dict(torch.load("model/model.pt", map_location="cpu"))
    model.eval()
    return model


@st.cache(allow_output_mutation=True)
def load_tokenizer():
    return BertTokenizer.from_pretrained("klue/bert-base", do_lower_case=False)


def bert_tokenizer(sentences, max_len, tokenizer):
    input_ids = []
    attention_mask = []
    token_type_ids = []
    for sentence in tqdm(sentences):
        encoded = tokenizer.encode_plus(
            text=sentence,
            add_special_tokens=True,
            max_length=max_len,
            truncation=True,
            padding="max_length",
            return_attention_mask=True,
        )
        input_ids.append(encoded["input_ids"])
        attention_mask.append(encoded["attention_mask"])
        token_type_ids.append(encoded["token_type_ids"])

    return (
        torch.tensor(input_ids),
        torch.tensor(attention_mask),
        torch.tensor(token_type_ids),
    )
