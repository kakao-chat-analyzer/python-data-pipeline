from fastapi import APIRouter, HTTPException, status, UploadFile, File
from schema import Keyword
from models.predict_data import KeyWords
from preprocessing.Preprocessing_OS1 import Preprocessing_OS1
from preprocessing.Preprocessing_OS2 import Preprocessing_OS2
import re

pipelines = APIRouter(
    tags=["Text"]
)

# 파일 업로드 시
@pipelines.post('/file')
async def pipeline(file: UploadFile = File(...)) -> dict:
    # Raw data Amazon S3 upload??
    print("============= Pre_PipeLine Start =============")
    
    # Get File
    file_contents = await file.read()
    data = file_contents.decode().splitlines()
    print("============= Preprocessing Start =============")
    
    # Preprocessing Text
    # OS1 인지 OS2 인지 확인 작업 (data의 첫번째 글이 '~.txt'형이면 OS1이다.)
    text = data[0].replace('\n','')
    if re.findall('.txt',text): # OS1
        print("Preprocessing_OS1")
        pre_data  = Preprocessing_OS1()
    else: # OS2
        print("Preprocessing_OS2")
        pre_data = Preprocessing_OS2()
        
    for idx, line in enumerate(data[2:]):
        if line != '':
            pre_data.conversationSplit(line.replace('\n','').strip())
            
        if idx == (len(data) - 3): # 데이터 마지막이면
            pre_data.dailyConversation()
    # 여기서 전체 대화 데이터를 넘겨줘야한다.
    text =pre_data.mergeConversation[-1]
    ## return value 
    ## frequently(당일 대화 개수), keyword(키워드), chattimes(당일 채팅 횟수), total_message(당일 대화)
    return {"keywordss": list(text)}
    
# 키워드 추출 시
@pipelines.post('/keyword')
async def pipeline(item: Keyword) -> dict:
    total_text = item.raw_data
            
    print("============= Keywords Extractor =============")
    # Predict Text -> result
    keywords = KeyWords()
    keywords_result = keywords.pipeline(total_text.strip())
    
    print("============= Finish =============")
    print("PipeLine End. Result: ", keywords_result)
    
    return {"keywords": keywords_result}

# curl -X POST -F "file=@/Users/goodyoung/Desktop/GIt/kakao-chat-analyzer/python-data-pipeline/data/test1.txt" http://127.0.0.1:8000/api/result
