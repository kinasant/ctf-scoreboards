from pathlib import Path
import pandas as pd
import scrapy
from inline_requests import inline_requests
#response.xpath("//div[@id='scoreboard']/div/table/tbody/tr[1]")
class TeamSpider(scrapy.Spider): 
    name = "sunshine"
    def __init__(self):
        self.headers = {'accept':'application/json','accept-encoding':'gzip, deflate, br, zstd','accept-language':'en-US,en;q=0.9','content-type':'application/json','cookie':'session=82155b2a-a0db-4bcd-bba0-785b54c0fece.rAtRrrRl1ro3hjRCClBjq6NjISI; cf_clearance=J6txjpNOhi.I1JxABfxNTln6Rv2dNDUxzt7y4Fi8x3M-1730688182-1.2.1.1-.QmkNylhVi1lzXghRnJRslecS9wmy.mrBUSfX_8Cgxvke.QSqiFIE1rJODGKtUXm7iVRrnHHi5sg_Dm14GjXKPt62VmDFy.WN5gW1zeL_egMK2PAhKQeG3Z4iSWe_SsTePoL3QhB9FACOFK7fWT2fSrbT3zTKYIghlatI9q8Wb.Eke7Y.tExuzfxWNvPwlgnhe6fdWA5reYX74Qzd19ATAMTAW7Atw_Xm2U_MXrrV87c2sKtY4q5qj1qA_ARNpf8X1d0RkWtHQs9yktK5SMzCrMaIZ.6_K_w_UoAHlHoy0rRHtlUKC77TdiHgJJNp861NA6CakkTXi80i0HI88VRYsoh4EAhNmZMXdVfzo6gjdxBY9n1HefuB7UyaELGwtFdsmr9CdXlzmdmHARNaPEgAMf14syoMuZrYqGuEEeljsbGa_Iq2euLwaCw8TzBotK2','csrf-token':'9407fa4e3ab19ba353bf0035147a904f1b0d9ed2af49b03782116b557c62a94e','priority':'u=1, i','referer':'https://2024.sunshinectf.org/scoreboard','sec-ch-ua-arch':"x86",'sec-ch-ua-bitness':"64",'sec-ch-ua-full-version':"130.0.2849.68",'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'}
    def start_requests(self):
        urls = [
            "file:///D:/ctf/stat/ctfd/ctfd/spiders/SunshineCTF%202024.html",
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,headers=self.headers)
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
            if int(y)<=1:
                break
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
            request= yield scrapy.Request(next_page,headers=self.headers)
            s = self.parse_team(request)
            challenges.append(s)
            cnt+=1
        df["challenge"] = challenges
        df.to_csv(Path(__file__).parent / 'sunshine.csv',index=False)
    def parse_team(self,response):
        table = response.css('tbody')[1]
        challenge_name = [i.strip() for i in table.css('tr a::text').getall()]
        challenge_category =table.css('tr td.d-none.d-md-block.d-lg-block::text').getall()
        challenge_points = table.css('tr td:nth-child(3)::text').getall()
        solve_time = table.css('td.solve-time span::attr(data-time)').getall()
        s = {'challenge_name': challenge_name,'challenge_category': challenge_category,'challenge_points': challenge_points,'solve_time': solve_time}
        return s