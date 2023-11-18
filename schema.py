from pydantic import BaseModel
from typing import List

# class TextData(BaseModel):
#     raw_data: str
#     mod: str 
    
#     class Config:
#         schema_extra = {
#             "example": {
#                 "raw_data": "raw data",
#                 "mod": "빈도수"
#             }
#         }
class Keyword(BaseModel):
    raw_data: str
    keyword: dict 
    
    class Config:
        json_schema_extra = {
            "example": {
                "raw_data": "Conversation data set(.txt)",
                "keyword": "keyword by text data"
            }
        }