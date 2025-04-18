from pathlib import Path
import pandas as pd
import scrapy
from scrapy.http import FormRequest
from inline_requests import inline_requests
from scrapy.shell import inspect_response
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "swampctf"
    def start_requests(self):
        urls = [
            "file:\\SwampCTF 2025.html",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_file)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    def login(self,response):
        nonce =  response.xpath("//input[@id='nonce']/@value").get()
        yield FormRequest.from_response(response,formnumber=1,formdata={'name':'temp','password':"temp",'nonce':nonce},callback=self.parse,dont_filter=True)
    def parse_file(self, response):
        #item = response.meta['item']
        points = []
        team = []
        nickname = []
        self.log(response)
        tables = response.xpath("//div[@id='scoreboard']/div/table/tbody/tr")
        for table in tables:
            y =  table.xpath("td[2]/text()").get()
            #if int(y)<=50:
                #break
            points.append(y)
            nickname.append(table.xpath("td[1]//a/text()").get().strip())
            team.append(table.xpath("td[1]//a/@href").get())
        self.nickname = nickname
        self.team = team
        self.points = points
        yield scrapy.Request(url='https://ctf.swampctf.com/login?next=%2Fscoreboard%3F',callback = self.login)
    @inline_requests
    def parse(self, response):
        df = pd.DataFrame()
        url = ""
        challenges = []
        cnt = 1
        team = self.team
        for i in team:
            self.log(f"{cnt}/{len(team)} teams processed")
            next_page = url+i
            request= yield scrapy.Request(next_page)
            s = self.parse_team(request)
            challenges.append(s)
            cnt+=1 
        df['points'] = self.points
        df['name'] = self.nickname
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