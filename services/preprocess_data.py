import re
from datetime import datetime

class Preprocessing:
    """
    카카오톡 txt 형식
    2023년 3월 19일 일요일
    2023. 3. 19. 오후 4:52, 이 형진 20 소웨 : 건영 
    """
################################################################################################
    # init
    def __init__(self):
        self._conversation = [] # 총 대화
        self._date = [] # 대화 날짜
        self._mergeConversation = [] # 하루 대화 총합
        self._dailyMessageList = [] # 하루대화
        self._dailyMessageStr = ''

################################################################################################
    # Property
    @property
    def conversation(self): return self._conversation

    @property
    def date(self): return self._date
        
    @property
    def mergeConversation(self): return self._mergeConversation
        
    @property
    def dailyMessageList(self): return self._dailyMessageList

    @property
    def dailyMessageStr(self): return self._dailyMessageStr
    
################################################################################################        
    # Main
    def isMessage(self,line:str):
        """ 
        메세지 특성 판별 
        
        '''
        
        2023년 3월 19일 일요일 (1)
        2023. 3. 19. 오후 4:52, 이 형진 20 소웨 : 건영  (2)
        뭐할거야 (3)
        ...
        
        '''
        
        1. 대화 시작
        2. 그 전과 이어진 대화인지
        3. 시작한 날짜인지
        """
        pattern1 = r'\d{4}\. \d{1,2}\. \d{1,2}\. [오후|오전]* \d{1,2}:\d{1,2}'
        pattern2 = r'^\d{4}\년 \d{1,2}\월 \d{1,2}\일 [월화수목금토일]요일+$' # ^는 문자열 시작 $는 문자열 끝부분
        if re.match(pattern1, line): # 대화 시작이다.
            return 1
        elif re.match(pattern2, line): # 날짜이다.
            return 2
        else: # 추가적 대화이다.
            return 0
            
    def messagePreprocess(self,message:str):
        """ 
        대화 전처리 
        1. 웃음, 울음 (ㅋㅋ, ㅎㅎ)
            - ㅋㅋㅋㅋ, ㅎㅎㅎㅎㅎ
        2. 느낌표 (!) , 물음표 (?)
            - !, !!!!!!!, !?!?
        3. 쉼표(,), 점(.)
            - ……. ,,,,,,
        4. 이모티콘 타입 1 (입 중심)
            - :) :D
        5. 이모티콘 타입 1 (눈 중심)
            - ^^, ㅜㅜ
        """
        pattern1 = "(\(.+?\))|([ㄴㅋㅎㅇzㅠㅜ!?~]{3,})|[,.]{2,}|([;:]{1}[\^'-]?[)(DPpboOX] )|([>ㅜㅠㅡ@+\^][ㅁㅇ0oO\._\-]*[\^ㅜㅠㅡ@+<];*)"
        message = re.sub(pattern1,'',message)
        if message: #전처리 결과 대화가 있을 경우
            return message.strip()
        else:
            return '' #or None
    
    def dailyConversation(self):
        """ 하루 대화 """
        if len(self._date) != 0:
            totalConversation = [self._date[-1], self._dailyMessageList,self._dailyMessageStr]
            self.mergeConversation.append(totalConversation) # 대화 넣기
            self._dailyMessageList = [] # 그날 대화 초기화
            self._dailyMessageStr = ''
        
    def conversationSplit(self,line:str):
        """ 대화 분리 """
        num = self.isMessage(line)
        if num == 1: # 대화 시작
            line_set = line.split(',', maxsplit=1)
            line_set[0] = self.changeTimeType(line_set[0]) # 날짜 형식 변환 "%Y-%m-%d %H:%M"로
            pop_line = line_set.pop()
            name, message = pop_line.split(':', maxsplit=1) # 대화 이름, 대화 내용 분리
            message = self.messagePreprocess(message) # 대화 전처리
            if message:
                self._dailyMessageList.append(message) #그 날 대화 종합 
                self._dailyMessageStr = self._dailyMessageStr + ' ' + message

            line_sets = line_set + [name.strip(), message]
            self._conversation.append(line_sets)
        elif num == 2: # 날짜
            self.dailyConversation() #그 전날 대화 총합
            self._date.append(self.changeDateType(line))
            
        else: # 추가적 대화
            self._conversation[-1].append(line)

    def changeDateType(self,line:str):
        """ 대화 날짜 타입 변경 """
        line = '-'.join(re.findall(r'\d+', line))
        dt = datetime.strptime(line, "%Y-%m-%d").strftime("%Y-%m-%d")
        return dt

    def changeTimeType(self,line:str):
        """ 대화 시간 타입 변경 """
        line = line.replace("오후","PM").replace("오전","AM")
        dt = datetime.strptime(line, "%Y. %m. %d. %p %I:%M").strftime("%Y-%m-%d %H:%M")
        return dt
    