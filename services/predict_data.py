# !pip3 install -U deep-translator
import torch
from services import h2_model,h2_tokenizer
from deep_translator import GoogleTranslator

class KeyWords:
    """ 한국어 대화 내용을 키워드 분석 """
    
    def translator(self,text,src='ko',trt='en'):
        """ 번역기 """
        return GoogleTranslator(source=src, target=trt).translate(text)

    def extractor(self,text):
        """ 키워드 추출기 """
        # 문장 토큰화 (인코딩)
        input_ids = h2_tokenizer(text, return_tensors="pt").input_ids.to('cpu')
        with torch.no_grad():
            # 모델 predict
            output = h2_model.generate(input_ids, max_length=300)
        # 문장 디코딩
        keywords = h2_tokenizer.decode(output[0], skip_special_tokens=True).lower()
        return keywords

    def pipeline(self,text):
        """
        키워드 추출 파이프라인
        1. 한국어 -> 영어로 변환
        2. 영어 -> 키워드 추출 (pretrained model)
        3. 영어 -> 한국어 변환
        """
        import time
        pre = time.time()
        # 번역(한->영)
        text = self.translator(text,src='ko',trt='en')
        print(f"번역 완료: [Time]: {time.time()-pre}"); pre = time.time()
        # 키워드 추출
        text = self.extractor(text)
        print(f"추출 완료: [Time]: {time.time()-pre}"); pre = time.time()
        # 번역(영->한)
        text = self.translator(text,src='en',trt='ko')
        print(f"번역 완료: [Time]: {time.time()-pre}")

        keywords_list = text.strip().split(',')
        keywords_list = list(map(lambda x: x.strip(), keywords_list))
        return keywords_list