from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "mctf"
    def start_requests(self):
        urls = [
            "file:///D:/ctf/stat/custom/custom/spiders/Scoreboard%20%E2%80%94%20M%E2%98%86CTF.html",
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
        points = table.xpath('tbody//th/text()').getall()[2::3]
        team = []
        name = table.xpath('tbody//th/text()').getall()[1::3]
        tables = response.xpath("//div[@id='scoreboard']/div/table/tbody/tr")
        df['points'] = points
        df['name'] = name
        url = ""
        challenges = []
        cnt=0
       # for i in team:
       #     self.log(f"{cnt}/{len(team)} teams processed")
       #     next_page = url+i
       #     request= yield scrapy.Request(next_page)
       #     s = self.parse_team(request)
       #     challenges.append(s)
       #     cnt+=1
       # df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / 'mctf.csv',index=False)
    def parse_team(self,response):
        table = response.css('tbody')[1]
        challenge_name = [i.strip() for i in table.css('tr a::text').getall()]
        challenge_category =table.css('tr td.d-none.d-md-block.d-lg-block::text').getall()
        challenge_points = table.css('tr td:nth-child(3)::text').getall()
        solve_time = table.css('td.solve-time span::attr(data-time)').getall()
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s