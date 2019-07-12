import re
import urllib.request
from bs4 import BeautifulSoup

# job info class
class JobInfo:
    def __init__(self, company, title, sub_title, career, education, location, employment_type, deadline, link):
        self.company = company
        self.title = title
        self.sub_title = sub_title
        self.career = career
        self.education = education
        self.location = location
        self.employment_type = employment_type
        self.deadline = deadline
        self.link = link
        self.co_link = 'http://www.jobkorea.co.kr/top100'

    def show_info(self):
        print('-------------------------------------------------------------------------')
        print('회사명 ({})'.format(self.company))
        print('메인 타이틀 ({})'.format(self.title))
        print('서브 타이틀 ({})'.format(self.sub_title))
        print('경력 구분 ({})'.format(self.career))
        print('학력 ({})'.format(self.education))
        print('지역 ({})'.format(self.location))
        print('고용 형태 ({})'.format(self.employment_type))
        print('마감 ({})'.format(self.deadline))
        print('링크 ({})'.format(self.co_link+self.link))
        print('-------------------------------------------------------------------------')

    def get_string(self):
        string = '-------------------------------------------------------------------------'+\
                 '회사명 ({})\n'.format(self.company) + \
                 '메인 타이틀 ({})\n'.format(self.title) + \
                 '서브 타이틀 ({})\n'.format(self.sub_title) + \
                 '경력 구분 ({})\n'.format(self.career) + \
                 '학력 ({})\n'.format(self.education) + \
                 '지역 ({})\n'.format(self.location) + \
                 '고용 형태 ({})\n'.format(self.employment_type) + \
                 '마감 ({})\n'.format(self.deadline) + \
                 '링크 ({})\n'.format(self.co_link + self.link)
        return string

    # setter
    def __setitem__(self, key, value):
        """Setting tag[key] sets the value of the 'key' attribute for the
        tag."""
        self.attrs[key] = value

    # getter
    def __getitem__(self, key):
        """tag[key] returns the value of the 'key' attribute for the tag,
        and throws an exception if it's not there."""
        return self.attrs[key]



# top 10 페이지 크롤링
def get_newbie_url(task):
    urls = {'경영':'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10012&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '마케팅': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10013&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            'IT': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10016&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '디자인': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10019&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '무역': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10014&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '디자인': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10015&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '무역': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10022&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '영업': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10015&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '서비스': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10022&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '연구개발': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10018&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '생산': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10017&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '교육': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10023&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '건설': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10021&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '의료': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10024&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '미디어': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10020&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '전문특수직': 'http://www.jobkorea.co.kr/starter/?schLocal=&schPart=10025&schMajor=&schEduLevel=&schWork=&schCType=&isSaved=1&LinkGubun=0&LinkNo=0&Page=1&schType=0&schGid=0&schOrderBy=0&schTxt=',
            '전체': 'http://www.jobkorea.co.kr/starter/'
            }

    return urls[task]


# top 10 페이지 url
def get_top10_url(task):
    urls = {}
    return urls[task]


def collect_url(url):
    # url = 'http://www.jobkorea.co.kr/starter'
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")
    page_button = soup.find('div', class_='tplPagination')
    urls = [url]
    for href in page_button.find_all('a'):
            urls.append('http://www.jobkorea.co.kr'+href.get('href'))
    return urls


def _crawl_newbie_info(task):

    # url = 'http://www.jobkorea.co.kr/Starter/?JoinPossible_Stat=0&schPart=%2C%2C10013%2C%2C&schOrderBy=0&LinkGubun=0&LinkNo=0&schType=0&schGid=0&Page=1'
    # print(urls)
    # # get_newbie_url(task)로 업무에 따른 url 반환
    # # collect_url(url)로 pagination된 전체 페이지 url 획득
    # urls = collect_url(get_newbie_url(task))

    urls = collect_url(get_newbie_url(task))
    jobs = []

    for url in urls:
        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code, "html.parser")

        filter_list = soup.find('ul', class_='filterList')

        for li in filter_list.find_all('li'):
            company = li.find('a', class_='coLink').getText()
            title = li.find('a', class_='link').getText()
            sub_title = li.find('div', class_='sTit').getText()
            sdsc = li.find('div', class_='sDesc')
            employment_type = sdsc.find('strong').getText()
            career = ''
            try:
                education = sdsc.find_all('span')[0].getText()
                location = sdsc.find_all('span')[1].getText()

            except IndexError:
                pass
            deadline = li.find('span', class_='day').getText()
            link = li.find('a', class_='coLink').get('href')
            if not link.startswith('http'):
                link = 'http://www.jobkorea.co.kr'+link
            job = JobInfo(company,
                          title,
                          sub_title,
                          career,
                          education,
                          location,
                          employment_type,
                          deadline,
                          link
            )
            # job.show_info()
            jobs.append(job)
    return jobs


# top 10 페이지 크롤링
def _crawl_job_info(task):
    url = get_top10_url(task)
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    jobs = []
    rank_list = soup.find('ol', class_='rankList')
    for li in rank_list.find_all('li'):
        company = li.find('a', class_='coLink').getText()
        title = li.find('a', class_='link').getText()
        sub_title = li.find('div', class_='sTit').getText()
        sdsc = li.find('div', class_='sDsc')
        try:
            career = sdsc.find_all('span')[0].getText()
            education = sdsc.find_all('span')[1].getText()
            location = sdsc.find_all('span')[2].getText()
            employment_type = sdsc.find_all('span')[3].getText()
        except IndexError:
            pass
        deadline = li.find('span', class_='day').getText()
        link = li.find('a', class_='coLink').get('href')
        job = JobInfo(company,
                      title,
                      sub_title,
                      career,
                      education,
                      location,
                      employment_type,
                      deadline,
                      link
        )
        jobs.append(job)
        # job.show_info()
    return jobs



# 크롤링 함수 구현하기
def _crawl_portal_keywords(text):
    url_match = re.search(r'<(http.*?)(\|.*?)?>', text)
    if not url_match:
        return '올바른 URL을 입력해주세요.'

    url = url_match.group(1)
    source_code = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(source_code, "html.parser")

    # 여기에 함수를 구현해봅시다.
    keywords = []
    if 'naver' in url:

        for i, keyword in enumerate(soup.find_all("span", class_="ah_k")):
            if i < 20:
                keywords.append(keyword.get_text())  # 한글 지원을 위해 앞에 unicode u를 붙혀준다.


    else:

        for i, keyword in enumerate(soup.find_all("a", class_="link_issue")):
            if i < 20:
                keyword = keyword.get_text()
                if keyword not in keywords:
                    keywords.append(keyword)

                    # 키워드 리스트를 문자열로 만듭니다.
    return '\n'.join(keywords)