import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
print("Model Download Start...")
h2_tokenizer = AutoTokenizer.from_pretrained("transformer3/H2-keywordextractor", cache_dir="./cache_dir/")
h2_model = AutoModelForSeq2SeqLM.from_pretrained("transformer3/H2-keywordextractor", cache_dir="./cache_dir/")
# # 모델 양자화
# h2_model = torch.quantization.quantize_dynamic(
#     h2_model, {torch.nn.Linear}, dtype=torch.qint8
# )
print("Model Download Complete...")