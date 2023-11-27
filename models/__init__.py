from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
print("Model Download Start...")
h2_tokenizer = AutoTokenizer.from_pretrained("transformer3/H2-keywordextractor", cache_dir="./cache_dir/")
h2_model = AutoModelForSeq2SeqLM.from_pretrained("transformer3/H2-keywordextractor", cache_dir="./cache_dir/")
print("Model Download Complete...")