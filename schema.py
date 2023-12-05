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
    totalMessage: str
    keywords: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "totalMessage": "Conversation data set(.txt)",
                "keywords": "Keyword"
                # "keyword": "keyword by text data"
            }
        }