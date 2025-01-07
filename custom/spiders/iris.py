from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "iris"
    def start_requests(self):
        urls = [
            "file://Scoreboard%20_%20IrisCTF%202025%20-%20CTF%20fun%20for%20hackers%20of%20all%20skill%20levels.html",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        #item = response.meta['item']
        df = pd.DataFrame()
        table = response.xpath('//div[@class = "scoreboard"]')
        points = [i.split(" ")[0] for i in table.xpath('//div[@class="scoreboard-score"]//text()').getall()]
        team = table.xpath('//div[@class="scoreboard"]//a/@href').getall()
        name = response.xpath('//div[@class="scoreboard"]//a//text()').getall()
        df['points'] = points
        df['name'] = name
        url = ""
        challenges = []
        for cnt,i in enumerate(team):
           self.log(f"{cnt}/{len(team)} teams processed")
           if int(points[cnt])==0:
            s = {'challenge_name': [],'challenge_category': [],'challenge_points': [],'solve_time': []}
            challenges.append(s)
            continue
           next_page = url+i
           request= yield scrapy.Request(next_page)
           s = self.parse_team(request)
           challenges.append(s)
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / f'{self.name}.csv',index=False)
    def parse_team(self,response):
        table= response.xpath('//tbody/tr')
        challenge_name = []
        challenge_category = []
        challenge_points = []
        solve_time = []
        for i in table:
            challenge_category.append(i.xpath('td[1]/a/text()').get())
            challenge_name.append(i.xpath('td[2]//text()').get())
            challenge_points.append(i.xpath('td[2]/text()').get()[2:-1])
            solve_time.append(i.xpath('td[3]//div/text()').get())
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s
