from transitions.extensions import GraphMachine

from utils import send_text_message,send_image_message,send_button_message

import random


answer=[]
MAX_GUESS = 10
guess = []
win=False

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def get_ans():
        global answer
        return answer

    def is_going_to_playgame(self, event):
        text = event.message.text
        return text.lower() == "play"

    def is_going_to_ask(self,event):
        text = event.message.text
        return text.lower() == 'test'

    
    def on_enter_ask(self,event):
        send_text_message(event.reply_token,"請問 1+1 是多少")
    
    
    def right1(self,event):
        return event.message.text=='10'
    
    
    def wrong1(self,event):
        return event.message.text!='10'
        
        
    def right2(self,event):
        return event.message.text == '大象的左耳' or event.message.text == '大象的左耳朵'
    
    def wrong2(self,event):
        return event.message.text != '大象的左耳' and event.message.text != '大象的左耳朵'
    
    def on_enter_ask3_rr(self,event):
        send_text_message(event.reply_token,"唉呦 不錯嘛\n您的 IQ 是 100")
        self.go_back()
    
    def on_enter_ask3_wr(self,event):
        send_text_message(event.reply_token,"還過得去歐\n您的 IQ 是 50")
        self.go_back()
        
    def on_enter_ask3_rw(self,event):
        send_text_message(event.reply_token,"勉強當你是人類...\n您的 IQ 是 5")
        self.go_back()
    
    
    def on_enter_ask3_ww(self,event):
        send_text_message(event.reply_token,"很笨嘛\n您的 IQ 是 -100")
        self.go_back()
    
    
    
    
    def on_enter_ask2_r(self,event):
        send_text_message(event.reply_token,"🈹 太聰明了😎\n那請問你知道什麼東西長得像大象的右耳朵嗎 🤓🤓")
        
    
    def on_enter_ask2_w(self,event):
        send_text_message(event.reply_token,"笨😅😅😅\n那請問你知道什麼東西長得像大象的右耳朵嗎 🤓🤓")
        
    
    
    def on_exit_user(self,event):
        print("hey here")
        global answer
        
        answer= list(str(random.randint(1000,9999)))
        tempy=answer
        
        for i in range(4):
            for j in range(4):
                if i == j:
                    continue
                while answer[i] == answer [j]:
                    answer[i]=str(random.randint(0,9))
        
        
        

    def on_enter_playgame(self,event):
        reply_token=event.reply_token
        text='輸入一個4位數的數字'
        send_text_message(reply_token,text)
        print("in playgame")
        self.advance(event)
        



    def on_enter_tell_user(self,event):
        global win
        global answer
        a=0
        b=0
        reply_token=event.reply_token
        guess=list(event.message.text)
        print(guess)
        for i in range(4):
            if answer[i]==guess[i]:
                a+=1
            elif answer[i] in guess:
                b+=1

        #send_text_message(event.reply_token,"%dA%dB"%(a,b))
        print("%dA%dB"%(a,b))

    
    def on_enter_user_answer(self,event):
        global win
        global answer
        reply_token=event.reply_token


    def on_enter_win(self,event):
        send_text_message(event.reply_token,"你運氣很好 ! ! \n輸入 PLAY 可以再賽一次")
        self.go_back()

    def on_enter_lose(seld,event):
        send_text_message(event.reply_token,"你輸了==\n但沒關係 輸入 PLAY 來雪恥")
        self.go_back()

    def on_enter_answeruser(self, event):
        global win
        global answer
        reply_token=event.reply_token
        print(answer)
        self.go_to_game(event)
        


    





        
