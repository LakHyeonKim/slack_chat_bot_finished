from slack.web.classes.blocks import *
from slack.web.classes.elements import *


# make_block(Job_class, int)
def make_block(_jobs, current):

    blocks = []

    for i in range(current-5, current):
        company = _jobs[i].__getattribute__('company')
        title = _jobs[i].__getattribute__('title')
        sub_title = _jobs[i].__getattribute__('sub_title')
        career = _jobs[i].__getattribute__('career')
        education = _jobs[i].__getattribute__('education')
        location = _jobs[i].__getattribute__('location')
        employment_type = _jobs[i].__getattribute__('employment_type')
        deadline = _jobs[i].__getattribute__('deadline')
        link = _jobs[i].__getattribute__('link')

        block = SectionBlock(
            text="*<" + link + " | " + company + ">*\n\n" + title + "\n" + sub_title + '\n경력 : ' + career +
                 "무관   |   학력 : " + education + "   |   지역 : " + location + "\n고용 형태 : " + employment_type +
                 "   |   마감일 : " + deadline +
                 "\n-------------------------------------------------------------------------------------------------\n"
        )
        blocks.append(block)

    button_actions = ActionsBlock(
        block_id='button',
        elements=[
            ButtonElement(
                text="이전 5개",
                action_id="last_5", value=str(current - 5)
            ),
            ButtonElement(
                text="다음 5개",
                action_id="next_5", value=str(current + 5)
            ),
        ]
    )

    blocks.append(button_actions)

    return blocks






