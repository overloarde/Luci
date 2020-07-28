import bs4
import requests

fixed_url = "https://www.lyricsmode.com"
url_l = 'https://www.lyricsmode.com/search.php?search='

def u_maker(song):

    for word in song.split(' '):
        global url_l
        url_l = url_l + word + '%20'


    print(url_l)
    search = requests.get(url_l)

    dumped = bs4.BeautifulSoup(search.text , 'html.parser')
    dumped = dumped.find("a" , {"class" : "lm-link lm-link--primary lm-link--highlight" })
    dumped = dumped['href']
    return dumped
def main_l(song):

    url = fixed_url + u_maker(song)

    R = requests.get(url)

    soup = bs4.BeautifulSoup(R.text, 'html.parser')

    soup = soup.find_all('div' , {"id" : "lyrics_text"})

    with open("Db/lyrics.txt" , 'w') as lyrics :
        for content in soup :
            if not content.text.isspace():
                lyrics.write("{}\n".format(content.text))
            else :
                pass

if __name__ == '__main__' :
    main_l(input("songs name sir : "))
