from transitions.extensions import GraphMachine

from utils import send_text_message

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

    def on_exit_user(self,event):
        print("hey here")
        global answer
        answer= list(str(random.randint(1000,9999)))

    def on_enter_playgame(self,event):
        reply_token=event.reply_token
        text='Enter a 4-digit number to guess'
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
        for i in range(3):
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
        send_text_message(event.reply_token,"WIN\nEnter play to play again")
        self.go_back()

    def on_enter_lose(seld,event):
        send_text_message(event.reply_token,"LOSE\nEnter play to play again")
        self.go_back()

    def on_enter_answeruser(self, event):
        global win
        global answer
        reply_token=event.reply_token
        print(answer)
        self.go_to_game(event)
        


        #guess = list(event.message.text)
       # print(guess)
        #correct = decide(guess,answer,len(answer))
       # if correct == len(answer):
       #     win=True

        #if win:
        #    self.go_to_win(event)
       # elif not win:
       #     self.go_to_lose(event)





        
