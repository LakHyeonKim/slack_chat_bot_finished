# 블록 클래스를 사용하는 데 필요한 import 문입니다.
from flask import Flask
from slack import WebClient
from slack.web.classes.blocks import *
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = 'xoxb-691797361766-689184678356-0H4RfMhRMctD17vM3qd4awhn'
SLACK_SIGNING_SECRET = '56c25316dd82cc632339a6dc295701d3'

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)
company = 'Elice'
type = '경력'
location = '중국'

# block = {
#     "type": "section",
#     "text": {
#         "type": "mrkdwn",
#         "text": "*"+company+"*\n"+type+'\n'+location
#     }
# }
#
#
# # "type": "section",
# # 		"text": {
# # 			"type": "mrkdwn",
# # 			"text": "*<fakeLink.toHotelPage.com|Windsor Court Hotel>*\n★★★★★\n$340 per night\nRated: 9.4 - Excellent"
# # 		}
# divider = {
#     "type": "divider"
# }
# # sample_block = {
# # {
# #     "type": "section",
# #     "text": {
# #         "type": "mrkdwn",
# #         "text": "We found *205 Hotels* in New Orleans, LA from *12/14 to 12/17*"
# #     }
# # }
# #
# # }


# 섹션 블록: 한 덩어리의 텍스트를 표시합니다..
block1 = SectionBlock(
    text="*There are many companies for you, Check it out, Take your wings*"
)

# 섹션 블록: 짧은 문구 여러 개를 2줄로 표시합니다 (최대 10개).
block2 = SectionBlock(
    fields=["text1", "text2", "text1", "text2"]
)

# 이미지 블록: 큰 이미지 하나를 표시합니다..
block3 = ImageBlock(
    image_url="이미지의 URL",
    alt_text="이미지가 안 보일 때 대신 표시할 텍스트"
)

head_block = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*There are many companies for you, Check it out, Take your wings*"
    }
}

# blocks = [[block]]
# for

# 챗봇이 멘션을 받았을 경우 (이벤트 처리 부분)
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    # if text == '<@UL9K54M32>':
    #     keywords = '아가리'
    # else:
    #     keywords = _chat_with_mybot(text)
    slack_web_client.chat_postMessage(
        channel=channel,
        blocks=extract_json([block1, block1, block2])
    )


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    # _crawl_job_info('text')
    # jobs = _crawl_newbie_info('전체')
    # for job in jobs:
    # print(job.__getattribute__('company'))
    app.run('127.0.0.1', port=5000)

