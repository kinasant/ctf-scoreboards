from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "usc"
    def start_requests(self):
        urls = [
            "file:USC%20CTF%20Fall%202024.html",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        #item = response.meta['item']
        df = pd.DataFrame()
        points = response.xpath('//table/tbody/tr/td[2]/text()').getall()
        team = response.xpath('//table/tbody/tr/td/a/@href').getall()
        name = response.xpath('//table/tbody/tr/td/a/text()').getall()
        eligibility = response.xpath('//table/tbody/tr/td/span/text()').getall()
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
        df['name'] = name
        df['points'] = points
        df["challenge"] = challenges
        df['elibigility'] = eligibility
        df.to_csv(Path(__file__).parent / 'usc.csv',index=False)
    def parse_team(self,response):
        challenge_name = [i.strip() for i in response.xpath('//table/tbody/tr/td/a/text()').getall()]
        challenge_category = [i.strip() for i in response.xpath('//table/tbody/tr/td[2]/text()').getall()]
        challenge_points = [i.strip() for i in response.xpath('//table/tbody/tr/td[3]/text()').getall()]
        solve_time = response.xpath('//table/tbody/tr/td[4]/span/@data-time').getall()
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s