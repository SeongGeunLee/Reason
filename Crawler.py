import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from itertools import count
n = 0
def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')
            return ret
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getResumeAddress(result):
    global n
    for page_idx in range(0, 38000):
        try:
            Resume_URL = 'http://www.saramin.co.kr/zf_user/public-recruit/coverletter?real_seq=%s' % str(page_idx)

            # rcv_data = urllib.request.urlopen(Resume_URL)
            # print()
            rcv_data = get_request_url(Resume_URL)
            soupData = BeautifulSoup(rcv_data, 'html.parser')
            answers = soupData.findAll('div', attrs={'class': 'box_ty3'})

            title = soupData.findAll('span', attrs={'class': 'txt_recruit'})
            title = title[0].get_text()
            n += 1
            print("index : ", page_idx, "/", n, "번째 : ", title)
            answer_Q = []
            answer_A = []

            bEnd = True
            for an in answers:
                bEnd = False
                texts = an.get_text().strip().split('\n')
                for i in range(len(texts)):
                    texts[i] = texts[i].strip().replace('  ', ' ')
                    index = texts[i].find('  ')
                    if index != -1:
                        texts[i] = texts[i][:index]
                answer_Q.append(texts[0])
                texts.remove('접기')
                answer_A.append(" ".join(texts[1:]))

            if (bEnd == True):
                print(result[0])  # 확인용으로 출력
                print("== 데이터 수 : %d" % len(result))
                return

            answer_All = " ".join(answer_A)
            result.append([title] + [answer_All])
        except:
            print("index : ", page_idx, ' / Not Exist Page!')
        # if n == 7233:
        #     return
        # elif page_idx == 36000:
        #     return

def resume_crawler():
    result = []
    print('RESUME ADDRESS CRAWLING START')
    getResumeAddress(result)
    resume_table = pd.DataFrame(result, columns=('title', 'answer'))
    print(result)
    resume_table.to_csv("./resume.csv", encoding="utf-8", mode='w', index=True)
    del result[:]
    print('FINISHED')

if __name__ == '__main__':
    resume_crawler()