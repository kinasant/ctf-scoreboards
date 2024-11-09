from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "defcon"
    def start_requests(self):
        urls = [
            "https://quals.2024.nautilus.institute/scoreboard.html",
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
        team = []
        name = []
        tables = response.xpath('//table/tbody/tr')
        df['points'] = tables[0].xpath('//tt/text()').getall()
        df['name'] = tables[0].xpath('//a/text()').getall()[2:]
        team = tables[0].xpath('//a/@href').getall()[2:]
        df['Time of Last Solution'] = tables[0].xpath('//td[4]').getall()
        url = "https://quals.2024.nautilus.institute/"
        challenges = []
        cnt=0
        for i in team:
            self.log(f"{cnt}/{len(team)} teams processed")
            next_page = url+i
            request= yield scrapy.Request(next_page,dont_filter=True)
            s = self.parse_team(request)
            challenges.append(s)
            cnt+=1
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / 'defcon.csv',index=False)
    def parse_team(self,response):
        tables = response.xpath('//table[2]/tbody/tr')
        challenge_name = []
        category_and_points = []
        observed_time = []
        solved_time = []
        time_taken = []
        for table in tables:
            category_and_points.append(tables[1].xpath('td[1]/text()').get().strip().replace('\n',' '))
            challenge_name.append(table.xpath('td/a//text()').get().strip())
            observed_time.append(table.xpath('td[3]/text()').get())
            solved_time.append(table.xpath('td[4]/text()').get())
            time_taken.append(table.xpath('td[5]/text()').get())
        s = {'category & points': category_and_points,'challenge_name': challenge_name,'observed_time':observed_time,'solved_time':solved_time,'time_taken':time_taken}
        return s