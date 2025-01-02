from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "asis"
    def start_requests(self):
        urls = [
            "https://asisctf.com/scoreboard",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]/td[1]//a/@href").get()
#table.xpath(td[1]//a/@href").get()
    @inline_requests
    def parse(self, response):
        #item = response.meta['item']
        df = pd.DataFrame()
        challenge = response.xpath('//table/thead//template//div/text()').getall()
        name = response.xpath("//table/tbody//div/span/text()").getall()
        points =[i.strip() for i in response.xpath("//table/tbody//td[@style = 'padding-left: 10px']/text()").getall() if i.strip()]
        challenges = []
        challenge = response.xpath('//thead//template//div/text()').getall()
        l1 = response.xpath('//table/tbody//template/td')
        for i in range(len(name)):
            challenge_name = []
            for cnt,j in enumerate(l1[i*len(challenge):(i+1)*len(challenge)]):
                if j.xpath('span'):
                    challenge_name.append(challenge[cnt])
            s = {"challenge_name":challenge_name}
            challenges.append(s)
        df['name'] = name
        df['points'] = points
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / f'{self.name}.csv',index=False)