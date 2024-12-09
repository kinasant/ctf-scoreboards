from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "lakectf"
    def start_requests(self):
        urls = [
            "file://LakeCTF%20%2724-%2725%20Quals.html",
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
        tables = response.xpath("//div[@id='scoreboard']/div/table/tbody/tr")
        for table in tables:
            y =  table.xpath("td[2]/text()").get()
            points.append(y)
            name.append(table.xpath("td[1]//a/text()").get().strip())
            team.append(table.xpath("td[1]//a/@href").get())
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
        df.to_csv(Path(__file__).parent / 'lakectf.csv',index=False)
    def parse_team(self,response):
        table = response.css('tbody')[0]``
        challenge_name = [i.strip() for i in table.css('tr a::text').getall()]
        challenge_category =table.css('tr td.d-none.d-md-block.d-lg-block::text').getall()
        challenge_points = table.css('tr td:nth-child(3)::text').getall()
        solve_time = table.css('td.solve-time span::attr(data-time)').getall()
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s