from konlpy.tag import Kkma
import crawl

def _read_file_job_category(filename):
   jobs = {'first': '1'}
   with open(filename) as file:
      for line in file:
         job, category = line.strip().split(':')
         jobs[job] = category.strip()
   return jobs

def _chat_with_mybot(text):
    # 키워드 매칭을 위한 딕셔너리
    words = {'jobs': [],
             'names': ['이름', '성함'],
             'age': ['나이', '살', '쌀'],
             'question': ['취업정보', '질문'],
             'greetings': ['안녕', '반가워', '하이', '방가']}
    jobs = _read_file_job_category('job_category.txt')
    anw = []
    check = True
    if text == '<@UL9K54M32>':
        anw.append(u'안녕나는 챗봇이얌~~!! 취업정보를 알려주는 봇이얌 ^_^ 난 한국말만 알아들어~!!')
        return u'\n'.join(anw)
    kkma = Kkma()
    keywords = kkma.nouns(text)
    words['jobs'] = list(jobs.keys())

    #print(keywords) # 사용자 입력 키워드 추출 (확인용)

    for i in range(len(words['greetings'])):
        if words['greetings'][i] in keywords:
            anw.append('안녕~ 나도' + words['greetings'][i] + '^_^\n')
            check = False

    for i in range(len(words['names'])):
        if words['names'][i] in keywords:
            anw.append('내 이름은 봇이얌 봇봇봇~!!\n')
            check = False

    for i in range(len(words['question'])):
        if words['question'][i] in keywords:
            anw.append(words['question'][i] + '??' + '알았어~~\n')
            check = False

    for i in range(len(words['age'])):
        if words['age'][i] in keywords:
            anw.append('내 나이는 20살이야~ 아주 젊지 ^_*\n')
            check = False

    for i in range(len(words['jobs'])):
        if words['jobs'][i] in keywords:
            # 크롤링한 직업정보 반환받고
            #print(jobs[words['jobs'][i]])
            _jobs = crawl._crawl_newbie_info(jobs[words['jobs'][i]])

            return _jobs

    if check:
        anw.append('뭐라는 거야 ~~ -3- 그건 몰라~\n')

    return u'\n'.join(anw)
## ^^
