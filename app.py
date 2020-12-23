import os
import sys
import random

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image_message

load_dotenv()


machine = TocMachine(
    states=["user", "state1", "state2","playgame","answeruser","lose","win","tell_user","user_answer","ask","ask2_r","ask2_w","ask3_rr","ask3_rw","ask3_wr","ask3_ww"],
    transitions=[
        {"trigger": "advance","source": "user","dest": "playgame","conditions": "is_going_to_playgame"},
        {"trigger": "advance","source": "user","dest": "ask","conditions": "is_going_to_ask"},
        {"trigger": "advance","source":"playgame","dest":"answeruser"},
        {"trigger": "ask_go","source": "ask","dest": "ask2_r","conditions": "right1"},
        {"trigger": "ask_go","source": "ask","dest": "ask2_w","conditions": "wrong1"},
        {"trigger": "ask_go_2","source": "ask2_r","dest": "ask3_rr","conditions": "right2"},
        {"trigger": "ask_go_2","source": "ask2_r","dest": "ask3_rw","conditions": "wrong2"},
        {"trigger": "ask_go_2","source": "ask2_w","dest": "ask3_wr","conditions": "right2"},
        {"trigger": "ask_go_2","source": "ask2_w","dest": "ask3_ww","conditions": "wrong2"},
        {"trigger": "go_back", "source": ["playgame","answeruser","lose","win","ask","ask3_rr","ask3_rw","ask3_wr","ask3_ww"], "dest": "user"},
        {"trigger": "go_back_guess", "source": "answeruser", "dest": "playgame"},
        {"trigger": "go_to_win", "source": "tell_user", "dest": "win"},
        {"trigger": "go_to_lose", "source": "tell_user", "dest": "lose"},
        {"trigger": "go_to_game","source": ["answeruser","tell_user"],"dest": "tell_user"},
        {"trigger": "go_to_answer","source": "tell_user","dest": "user_answer"},

    ],
    initial="user",
    queued=True,
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


channel_access_token = "91xFl2RPQAVenKkLweKDwVPlGN0MAQ4/RD2zuqWunfBz7KFSLjGlj6mMpcZqHEmpT+4L89diO5nGokJVzkW7aMO2nrreYfVnhIeUcFgecqpkyl7i01Upe512uLtX5epSUHNJGvZfxlnD9iHjfcwDuQdB04t89/1O/w1cDnyilFU="

# get channel_secret and channel_access_token from your environment variable
channel_secret = "ffdf310f16f5bd02899f0dc8e3f7e77a"

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
mode = 0

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"



@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        a=b=0 
        count=0
        
        
        if event.message.text=="幹":
            send_text_message(event.reply_token,"幹")
            
        if event.message.text=="笑死":
            send_text_message(event.reply_token,"笑三小")
        
        if event.message.text=="好難":
            send_text_message(event.reply_token,"這也不會==\n"+str(TocMachine.get_ans()))
            
        if event.message.text=="早安":
            choose = random.randint(0,4)
            
            if choose == 0:
                send_image_message(event.reply_token,"https://i.imgur.com/1WUoYts.jpg")
            elif choose == 1:
                send_image_message(event.reply_token,"https://i.imgur.com/Uoc2KuS.jpg")
            elif choose == 2:
                send_image_message(event.reply_token,"https://i.imgur.com/mUBO1k0.jpg")
            elif choose == 3:
                send_image_message(event.reply_token,"https://i.imgur.com/XzLuVgj.png")
            elif choose == 4:
                send_image_message(event.reply_token,"https://i.imgur.com/4CMsVpG.jpg")
                

        if event.message.text.lower()=='play' and machine.state=="user":
            machine.advance(event)       
            continue
        elif event.message.text.lower()=='test' and machine.state=="user":
            machine.advance(event)
            continue
        elif machine.state=="ask":
            machine.ask_go(event)
            continue
        elif machine.state=='ask2_r' or machine.state=='ask2_w':
            machine.ask_go_2(event)
            continue
        elif machine.state=="user" :
            send_text_message(event.reply_token,"輸入 PLAY 來開始遊戲 ! \n或是輸入 TEST 來測測看IQ !")
            continue
        elif machine.state=='tell_user':
            answer=TocMachine.get_ans()
            guess=list(event.message.text)
            if len(guess) != 4:
                send_text_message(event.reply_token,"輸入4位數==")
                continue
            
            
            for i in range(4):
                if answer[i]==guess[i]:
                    a+=1
                elif answer[i] in guess:
                    b+=1
            text=("%dA%dB"%(a,b))
            count+=1
            if count ==20:
                machine.go_to_lose(event)
                continue
            elif a==4:
                machine.go_to_win(event)
                continue
            send_text_message(event.reply_token,text)
            continue
            



    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
