from abc import abstractmethod, ABC
from preprocessing import re

class BasePreprocessor(ABC):
################################################################################################
    # init
    def __init__(self):
        self._conversation = [] # 총 대화
        self._date = [] # 대화 날짜
        self._mergeConversation = [] # 하루 대화 총합
        self._dailyMessageList = [] # 하루 대화
        self._dailyMessageStr = ''
        self._dailyMessageCnt = 0
        self._userName = ''
        self._dailyUserList = []

################################################################################################
    # Property
    @property
    def conversation(self): return self._conversation
    @conversation.setter
    def conversation(self, value): self._conversation = value

    @property
    def date(self): return self._date
    @date.setter
    def date(self, value): self._date = value

    @property
    def mergeConversation(self): return self._mergeConversation
    @mergeConversation.setter
    def mergeConversation(self, value): self._mergeConversation = value

    @property
    def dailyMessageList(self): return self._dailyMessageList
    @dailyMessageList.setter
    def dailyMessageList(self, value): self._dailyMessageList = value

    @property
    def dailyMessageStr(self): return self._dailyMessageStr
    @dailyMessageStr.setter
    def dailyMessageStr(self, value): self._dailyMessageStr = value

    @property
    def dailyMessageCnt(self): return self._dailyMessageCnt
    @dailyMessageCnt.setter
    def dailyMessageCnt(self, value): self._dailyMessageCnt = value   
    
    @property
    def userName(self): return self._userName
    @userName.setter
    def userName(self, value): self._userName = value   
    
    @property
    def _dailyMessageUser(self): return self._dailyMessageUser
    @_dailyMessageUser.setter
    def _dailyMessageUser(self, value): self._dailyMessageUser = value  
    
################################################################################################        
    # AbstractMethod
    @abstractmethod
    def isMessage(self,line:str):
        """ 메세지 특성 판별 """
        pass
    
    @abstractmethod
    def conversationSplit(self,line:str):
        """ 대화 분리 """
        pass
    
    @abstractmethod
    def changeDateType(self,line:str):
        """ 대화 날짜 타입 변경 """
        pass
    
    @abstractmethod
    def changeTimeType(self,line:str):
        """ 대화 시간 타입 변경 """
        pass
    
################################################################################################        
    # Method
    def initVariable(self):
        """ 인스턴스 변수 초기화 """
        self._dailyMessageList = [] # 그날 대화 초기화
        self._dailyUserList = [] # 그날 유저 초기화
        self._dailyMessageStr = ''
        self._dailyMessageCnt = 0
        
        
    def dailyMessage(self, message: str):
        """ 메시지 종합 """
        if message: 
            self._dailyMessageStr = self._dailyMessageStr + ' ' + message

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
        pattern1 = "(\(.+?\))|([ㄴㅋㅎㅇzㅠㅜ!?~]{3,})|[,.]{2,}|([;:]{1}[\^'-]?[)(DPpboOX] )|([>ㅜㅠㅡ@+\^][ㅁㅇ0oO\._\-]*[\^ㅜㅠㅡ@+<];*)|사진"
        message = re.sub(pattern1,'',message)
        
        if message: #전처리 결과 대화가 있을 경우
            return message.strip()
        else:
            return '' #or None
        
    def dailyConversation(self):
        """ 하루 대화 종합 """
        if len(self._date) != 0:
            totalConversation = [self._date[-1], self._dailyMessageList, self._dailyUserList ,self._dailyMessageStr, self._dailyMessageCnt]
            self.mergeConversation.append(totalConversation) # 대화 넣기
            self.initVariable() #변수 초기화
            
    def dailyIndividualConversation(self,message:str):
        """ 각 사용자의 대화 """
        self._dailyMessageList.append(message) #그 날 대화 종합
        self._dailyUserList.append(self.userName.strip()) #그 날 대화 이름
    
    def dailyPipeLine(self, message: str):
        """ 하루 대화 내용 저장 파이프라인 """
        self.dailyIndividualConversation(message) #각 사용자 별 대화 저장
        message = self.messagePreprocess(message) # 대화 전처리
        self.dailyMessage(message) #메세지 종합

    

