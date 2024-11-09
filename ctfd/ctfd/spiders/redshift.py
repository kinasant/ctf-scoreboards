from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "redshift"
    def start_requests(self):
        urls = [
            "https://quals.o1d-bu7-go1d.ru/scoreboard",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        #item = response.meta['item']
        df = pd.DataFrame()
        points = response.xpath('//div[@id = "scoreboard"]//table/tbody/tr/td[2]/text()').getall()
        team = response.xpath('//div[@id = "scoreboard"]//table/tbody/tr/td/a/@href').getall()
        name = [i.strip() for i in response.xpath('//div[@id = "scoreboard"]//table/tbody/tr/td/a/text()').getall()]
        df['points'] = points
        df['name'] = name
        url = "https://quals.o1d-bu7-go1d.ru"
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
        df.to_csv(Path(__file__).parent / 'redshift.csv',index=False)
    def parse_team(self,response):
        table = response.xpath('//table')[1]
        challenge_name = [i.strip() for i in table.xpath('tbody//a/text()').getall()]
        challenge_category =table.xpath('tbody/tr/td[2]/text()').getall()
        challenge_points = table.xpath('tbody/tr/td[3]/text()').getall()
        solve_time = table.css('td.solve-time span::attr(data-time)').getall()
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s