from helium import *
from bs4 import BeautifulSoup
import pandas as pd
driver = start_chrome()
go_to('https://platform.ctf.hkcert.org/scoreboard')
t=[]
c=[]
df = pd.DataFrame()
for i in range(120):
    teams = [i.text for i in soup.find_all('span')]
    ans = []
    for cnt,j in enumerate(teams):
        if 'Page' in j:
            ans=teams[cnt-10:cnt]
            break
    for i in ans:
        p = parse_team(i)
        c.append(p)
        t.append(i)
    click(next)

def parse_team(i):
    click(i)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    s = [i.text for i in soup.find_all('span')]
    data = s[s.index('Price')+1:s.index('Events')]
    score = data[-1]
    data = data[:-4]
    challs = data[::2]
    points = data[1::2]
    driver.execute_script("window.history.go(-1)")
    s1 = {"challenge_name":challs,"challenge_points":points,"challenge_score":score}
    return s1

