import fasttext.util

# En hafif model için 'wiki.simple' indirebilirdik, ama burada büyük olanı indiriyoruz:
fasttext.util.download_model('en', if_exists='ignore')  # cc.en.300.bin

print("FastText English model downloaded successfully.")