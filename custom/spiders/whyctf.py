from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "whyctf"
    def start_requests(self):
        urls = [
            "https://ctf.why2025.org/scores",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        #item = response.meta['item']
        df = pd.DataFrame()
        table = response.xpath('//table')[2]
        rows =table.xpath('//tr')[1::224]
        name = rows[1].xpath('//td[2]//span/text()').getall()
        name = [i.strip() for i in name]
        points = [i for i in rows[1].xpath('//td[4]/text()').getall() if i.strip()]
        team =rows[1].xpath('//td[2]/a/@href').getall()
        df['name'] = name
        df['points'] = points
        url = "https://ctf.why2025.org/"
        challenges = []
        cnt=1
        for p,i in enumerate(team):
            self.log(f"{cnt}/{len(team)} teams processed")
            if int(points[p]) == 0:
                challenges.append({'challenge_name':'','challenge_category': '','challenge_points':'','solve_time': ''})
                cnt+=1
                continue
            next_page = url+i
            request= yield scrapy.Request(next_page)
            s = self.parse_team(request)
            challenges.append(s)
            cnt+=1
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / f'{self.name}.csv',index=False)
    def parse_team(self,response):
        rows  = response.xpath('//table//tr')
        challenge_category = [i.strip()[1:-1] for i in rows.xpath('td[1]/text()').getall()[1::2]]
        challenge_name = [i.strip() for i in rows.xpath('td[1]//a/text()').getall()]
        challenge_points = [i.strip() for i in rows.xpath('td[3]/text()').getall()]
        solve_time = [i.strip()[-20:-1] for i in rows.xpath('td[2]/text()').getall()]
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s