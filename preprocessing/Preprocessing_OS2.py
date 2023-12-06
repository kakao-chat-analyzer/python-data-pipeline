from . import re, datetime
from .BasePreprocessor import BasePreprocessor

class Preprocessing_OS2(BasePreprocessor):
    """ OS2 윈도우 버전 """
################################################################################################
    # init
    def __init__(self):
        super().__init__()
        self.today_date = ''

################################################################################################        
    # Main
    def isMessage(self, line:str):
        """
        메세지 특성 판별 
        '''
        --------------- 2023년 9월 12일 화요일 --------------- (1)
        이형진님이 고건영님, 승주님을 초대하였습니다. (2)
        [형진이] [오후 2:46] 고우 (3)
        '''
        1. 대화 시작
        2. 추가적인 대화
        3. 일반적인 대화
        
        """        
        pattern1 = r'\[([^\]]+)\] \[([^\]]+)\] (.+)'
        pattern2 = r'[-]+ (\d{4}년 \d{1,2}월 \d{1,2}일 [월화수목금토일]요일) [-]+'
        
        if re.match(pattern1, line): # 대화 시작이다.
            return 1
        elif re.match(pattern2, line): # 날짜이다.
            return 2
        else: # 추가적 대화이다.
            return 0
        
    def conversationSplit(self,line:str):
        """ 대화 분리 """
        num = self.isMessage(line)
        if num == 1: # 대화 시작
            line_set = re.findall(r'\[.+?\]|\[.+?\]|\S+', line)
            
            name = line_set[0][1:-1]
            self.dailyUserConversation(name) # 대화 유저(사용자) 처리
            line_set[1] = self.today_date +' ' + line_set[1][1:-1]
            message = ' '.join(line_set[2:])
            
            self.dailyPipeLine(message) #하루 대화 내용 저장 파이프라인 #메시지 값을 리턴 받아야 할 지 고민이다.
            self.dailyMessageCnt += 1
            
        elif num == 2: # 날짜
            self.dailyConversation() #그 전날까지의 대화 저장 (total)
            self.date.append(self.changeDateType(line))
        else: # 추가적 대화
            try:
                self.dailyPipeLine(line) #하루 대화 내용 저장 파이프라인
            except:
                pass
            
    def changeDateType(self,line:str):
        """ 대화 날짜 타입 변경 """
        line = re.findall(r'(\d{4}년 \d{1,2}월 \d{1,2}일 [월화수목금토일]요일)', line)[0]
        line = '-'.join(re.findall(r'\d+', line))
        dt = datetime.strptime(line, "%Y-%m-%d").strftime("%Y-%m-%d")
        self.today_date = dt
        return dt
        
    def changeTimeType(self,line:str):
        """ 대화 시간 타입 변경 """
        line = line.replace("오후","PM").replace("오전","AM")
        dt = datetime.strptime(line, "%Y-%m-%d %p %I:%M").strftime("%Y-%m-%d %H:%M")
        return dt