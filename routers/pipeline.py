from fastapi import APIRouter, HTTPException, status, UploadFile, File
from schema import Keyword
from models.predict_data import KeyWords
from preprocessing.Preprocessing_OS1 import Preprocessing_OS1
from preprocessing.Preprocessing_OS2 import Preprocessing_OS2
from fastapi.responses import JSONResponse
import re

pipelines = APIRouter(
    tags=["Text"]
)
def convert_dict(data):
    """ dict data 변환기 """
    # Input: {"고건영":64,"이 형진 20 소웨":48}
    new_li = []
    for i,j in data.items():
        new_li.append(i)
        new_li.append(j)
    # Output: ['고건영',64,'이형진',52]
    return new_li

def convert_json(data):
    date, daily_messages, daily_user, totalMessage ,chatTimes, frequency = data # data 반환
    frequency_li = convert_dict(frequency)
    json_data = {
        "date": date,
        "dailyMessages": daily_messages,
        "dailyUser": daily_user,
        "frequently": frequency_li,
        "keyword": None,
        "chatTimes": chatTimes,
        "totalMessage": totalMessage,
    }
    return json_data

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

    json_array = [convert_json(data) for data in pre_data.mergeConversation]
    ## frequently(당일 대화 개수), keyword(키워드), chattimes(당일 채팅 횟수), total_message(당일 대화)
    print(json_array[0])
    return JSONResponse(content=json_array)
    
# 키워드 추출 시
@pipelines.post('/keyword')
async def pipeline(item: Keyword) -> Keyword:
    print("응답이 왔습니다.")
    print(item.totalMessage)
    total_text = item.totalMessage
            
    print("============= Keywords Extractor =============")
    # Predict Text -> result
    keywords = KeyWords()
    keywords_result = keywords.pipeline(total_text.strip())
    
    print("============= Finish =============")
    print("PipeLine End. Result: ", keywords_result)
    tot = {"totalMessage":keywords_result}
    processed_item = Keyword(keywords=keywords_result, totalMessage=total_text)
    return processed_item
    # return {"totalMessage": keywords_result}
    # return JSONResponse(content=tot)

# curl -X POST -F "file=@/Users/goodyoung/Desktop/GIt/kakao-chat-analyzer/python-data-pipeline/data/test1.txt" http://127.0.0.1:8000/api/result
