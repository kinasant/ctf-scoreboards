from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
from time import sleep
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "uoftctf"
    def start_requests(self):
        urls = [
            "https://play.uoftctf.org/scoreboard",
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
        tables = response.xpath('//table')[1].xpath('tbody/tr')
        for table in tables:
            y =  table.xpath("td[2]/text()").get()
            points.append(y)
            name.append(table.xpath("td[1]//a/text()").get().strip())
            team.append(table.xpath("td[1]//a/@href").get())
        df['points'] = points
        df['name'] = name
        url = "https://play.uoftctf.org/"
        challenges = []
        cnt=0
        while cnt!=len(team):
         try:
            self.log(f"{cnt+1}/{len(team)} teams processed")
            next_page = url+team[cnt]
            request= yield scrapy.Request(next_page)
            s = self.parse_team(request)
            challenges.append(s)
            cnt+=1
         except:
            sleep(2)
            continue
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / f'{self.name}.csv',index=False)
    def parse_team(self,response):
        table = response.css('tbody')[1]
        challenge_name = [i.strip() for i in table.css('tr a::text').getall()]
        challenge_category =table.css('tr td.d-none.d-md-block.d-lg-block::text').getall()
        challenge_points = table.css('tr td:nth-child(3)::text').getall()
        solve_time = table.css('td.solve-time span::attr(data-time)').getall()
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s