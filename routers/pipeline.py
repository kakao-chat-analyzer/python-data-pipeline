from fastapi import APIRouter, HTTPException, status, UploadFile, File
from schema import Keyword
from services.predict_data import Predict
from services.preprocess_data import Preprocessing


pipelines = APIRouter(
    tags=["Text"]
)

@pipelines.post('/result')
async def pipeline(file: UploadFile = File(...)) -> dict:
    
    # Raw data Amazon S3 upload??
    # Preprocessing Text
    pre_data = Preprocessing(file)
    
    # Predict Text -> result
    result = Predict(pre_data)
    
    # 
    # Keyword.keyword = 
    return result