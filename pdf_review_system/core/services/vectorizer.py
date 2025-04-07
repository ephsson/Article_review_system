import fasttext
import os

# Proje kök dizinindeki .bin dosyasının tam yolu
MODEL_PATH = "C:/Users/emirp/Desktop/we are soo so back/pdf_review_system/cc.en.300.bin"
# FastText modelini yükle
ft_model = fasttext.load_model(MODEL_PATH)

def vectorize_text(text):
    return ft_model.get_sentence_vector(text).tolist()
