from konlpy.tag import Okt
import fitz  # PyMuPDF
import re

# 1. PDF 텍스트 추출
pdf_path = "d:/csi_api_workspace/IndustrySafetyLaw/data/산업안전보건법(법률)(제19591호)(20240517).pdf"
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()

okt = Okt()

# 형태소 단위로 토큰화
tokens = okt.morphs(text)

filtered_okt_tokens = [
    tok for tok in tokens
    if len(tok) > 1 and re.search(r'[가-힣a-zA-Z0-9]', tok)
]

# 결과
print("정제 전 okt", len(tokens))
print("Okt 형태소 토큰 수:", len(filtered_okt_tokens))
