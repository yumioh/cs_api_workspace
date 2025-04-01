from transformers import AutoTokenizer
import tiktoken
import re
import fitz  # PyMuPDF

# 1. PDF 텍스트 추출
pdf_path = "d:/csi_api_workspace/IndustrySafetyLaw/data/산업안전보건법(법률)(제19591호)(20240517).pdf"
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()
doc.close()

# 2. BERT 토크나이저 로드 및 토큰화
bert_tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")
bert_tokens = bert_tokenizer.tokenize(text)

# BERT 기준: 1글자 이하 또는 특수문자만인 토큰 제거
filtered_bert_tokens = [
    tok for tok in bert_tokens
    if len(tok) > 1 and re.search(r'[가-힣a-zA-Z0-9]', tok)
]

# 3. cl100k_base 토크나이저 로딩 및 토큰화
encoding = tiktoken.get_encoding("cl100k_base")
cl100k_token_ids = encoding.encode(text)

# 토큰 ID를 문자열로 디코딩 후 필터링
# 숫자값으로 나오므로 문자열로 decode 해야함
decoded_tokens = [encoding.decode([tid]) for tid in cl100k_token_ids]
filtered_cl100k_tokens = [
    tok for tok in decoded_tokens
    if re.search(r'[가-힣a-zA-Z0-9]', tok)
]

# 4. 출력
print("전체 글자 수:", len(text))
print("원래 BERT 토큰 수:", len(bert_tokens))
print("필터링된 BERT 토큰 수:", len(filtered_bert_tokens))
print("원래 cl100k_base 토큰 수:", len(cl100k_token_ids))
print("필터링된 cl100k_base 토큰 수:", len(filtered_cl100k_tokens))

print("샘플 BERT 토큰 10개:", filtered_bert_tokens[:10])
print("샘플 cl100k_base 토큰 10개:", filtered_cl100k_tokens[:10])
