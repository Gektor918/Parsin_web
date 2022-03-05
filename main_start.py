from bs4 import BeautifulSoup as be4
import requests as rq
import sqlite3 as sql
from telegraph import Telegraph


def _soup(url):
    try:
        ask = rq.get(url)
        ask.encoding = 'windows-1251'
        soup = be4(ask.text, 'lxml')
        return soup
    except Exception as e:
        return {'error':e}
    return 'fin'

def find_all_snippets(soup,tag,**kwargs):
    rezult = soup.find_all(tag,**kwargs)
    return rezult

def parse_article(link_list):
    my_dict  = {
    'января':'01',
    'февраля':'02',
    'марта':'03',
    'апреля':'04',
    'мая':'05',
    'июня':'06',
    'июля':'07',
    'августа':'08',
    'сентября':'09',
    'октября':'10',
    'ноября':'11',
    'декабря':'12'
}
    fin_date = ''
    final = []
    new = ''
    for link in link_list:
        link_soup = _soup(link)
        date,name,txt = link_soup.find('div',{'class':'date'}),\
                link_soup.find('p',{'class':'name'}),\
                link_soup.find_all('p',limit=2)[1]
        date = date.text.strip()
        date_split = date.split()
        for i in date_split:
            if i in my_dict:
                new = i.replace(i,my_dict[i])
        fin_date = date_split[2]+'-'+new+'-'+date_split[0]+' '+date_split[3]
        final+=[(fin_date,name.text.strip(),txt.text.strip())]
    return final

if __name__ == '__main__':
    target = 'https://www.astronews.ru/'
    soup = _soup(target)
    all_links = find_all_snippets(soup,'a', **{'class':'name'})
    clear_links = [target + link['href'] for link in all_links if 'news' in link['href']]

new_unic_links = []
for i in clear_links:
    if not i in new_unic_links:
        new_unic_links+=[i]

final = parse_article(new_unic_links)

def parse_img(new_unic_links):
    final = []
    for i in new_unic_links:
        link_soup = _soup(i)
        img = link_soup.find('div',{'class':'news-page'}).find('a').find('img')['src']
        final+=[(img)]
        one_img = final[0]
        img = 'https://www.astronews.ru'+ one_img
    return img
img_link_one = parse_img(new_unic_links)


db_name = 'articles.db'
DB = sql.connect(db_name)
cur = DB.cursor()

def update_base(final):
    new = []
    for i in final:
        cur.execute('select * from articles order by date DESC')
        if i[0] == cur.fetchall()[0][0]:
            break
        else:
            new += [(i)]
    if not new:
        return 'none'
    else:
       for i in new:    
            cur.execute("""
insert into articles (date, header, content) values (?,?,?)
""", i)
    DB.commit()
    return 'update'
update_base(final)

cur.execute('select * from articles order by date DESC')
text_cont = cur.fetchall()[0][2]

cur.execute('select * from articles order by date DESC')
title_cont = cur.fetchall()[0][1]

mass_create = [
    {
  "tag":"img",
  "attrs":{"src":img_link_one},
  },
  {
    "tag":"h3",
    "children":[title_cont]
  },
  {
    "tag":"p",
    "children":[text_cont]
  }
]

telegraph = Telegraph("e651a827ca035267aba3a290cc887a36a3abb712101e7b702abb8ec3cdd2")

response = telegraph.create_page(
    title = 'Space/News', 
    author_name = 'Astronews',
    author_url = 'https://www.astronews.ru/',
    content = mass_create
)
return_link = 'https://telegra.ph/{}'.format(response['path'])
DB.close()

def send_telegram(return_link):
    url = "https://api.telegram.org/bot5232924111:AAFAgpx54Sesr6NIpxoyyLz_Y4kBL23PO5A/sendMessage"
    channel_id = -1001660671340
    try:
        r = rq.post(url, data={
            "chat_id": channel_id,
            "text": return_link,
            })
    except Exception as e:
        return {'error': e}
send_telegram(return_link)
