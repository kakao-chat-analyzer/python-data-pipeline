from fastapi import APIRouter, HTTPException, status, UploadFile, File
from schema import Keyword
from services.predict_data import KeyWords
from services.preprocess_data import Preprocessing


pipelines = APIRouter(
    tags=["Text"]
)

@pipelines.post('/result')
async def pipeline(file: UploadFile = File(...)) -> dict:
    # Raw data Amazon S3 upload??
    
    print("============= PipeLine Start =============")
    # Get File
    file_contents = await file.read()
    data = file_contents.decode().splitlines()
    
    print("============= Preprocessing Start =============")
    # Preprocessing Text
    pre_data = Preprocessing()
    for idx, line in enumerate(data[2:]):
        if line != '':
            pre_data.conversationSplit(line.replace('\n','').strip())
            
        if idx == (len(data) - 3): # 데이터 마지막이면
            pre_data.dailyConversation()
            
    print("============= Keywords Extractor =============")
    # Predict Text -> result
    text =pre_data.mergeConversation[-2][2].strip()
    keywords = KeyWords()
    result = keywords.pipeline(text)
    
    print("============= Finish =============")
    print("PipeLine End. Result: ", result)
    return {"keywords": result}
# curl -X POST -F "file=@/Users/goodyoung/Desktop/GIt/kakao-chat-analyzer/python-data-pipeline/data/test1.txt" http://127.0.0.1:8000/api/result
