from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
import json
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "alpacahack"
    def start_requests(self):
        urls = [
            "file:Scoreboard%20-%20AlpacaHack%20Round%206%20%28Pwn%29.html",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        #item = response.meta['item']
        df = pd.DataFrame()
        points = []
        team = [i for i in response.xpath('//a/@href').getall()[:-3] if 'users' in i]
        t = response.xpath('//p/text()').getall()[9:]
        name = []
        for cnt,i in enumerate(t):    
          if i == 'pts':
              name.append(t[cnt-2]) 
              points.append(t[cnt-1])
        df['points'] = points
        df['name'] = name
        url = ""
        challenges = []
        cnt=0
        for i in team:
            self.log(f"{cnt}/{len(team)} teams processed")
            next_page = url+i
            request= yield scrapy.Request(next_page)
            s = self.parse_team(request)
            challenges.append(s)
            cnt+=1
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / 'alpacahack.csv',index=False)
    def parse_team(self,response):
        s = response.xpath('//script[2]/text()').get()
        y = s[s.index('=')+1:-1]
        data = json.loads(y)
        submissions = data['state']['loaderData']['routes/_root.users_.$userName']['submissions']
        challenges = []
        for submission in submissions:
            challenge = submission['challenge']
            challenge_info = {
            'name': challenge['name'],
            'solves': challenge['solves'],
            'category': challenge['categories'][0]['name']  
            }
            if challenge_info['category'] == 'Pwn':
                challenges.append(challenge_info)
        return challenges