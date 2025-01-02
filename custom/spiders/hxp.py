from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
from scrapy.shell import inspect_response
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "hxp"
    def start_requests(self):
        urls = [
            'file://Scoreboard%20_%20hxp%2038C3%20CTF.html',
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        challenge = response.xpath('//table/thead//a/text()').getall()
        name = []
        position = []
        points = []
        challenges = []
        for l1,i in enumerate(response.xpath('//table/tbody/tr')):
            position.append(i.xpath('td/text()').get())
            name.append(i.xpath('td[2]/a/text()').get())
            points.append(i.xpath('td[3]/text()').get())
            challenge_name = []
            for cnt,j in enumerate(i.xpath('td')[3:]):
                if j.xpath('text()').get():
                    challenge_name.append(challenge[cnt])
            s = {'challenge_name': challenge_name}
            challenges.append(s)
        df = pd.DataFrame()
        df['position'] = position
        df['points'] = points
        df['name'] = name
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / f'{self.name}.csv',index=False)