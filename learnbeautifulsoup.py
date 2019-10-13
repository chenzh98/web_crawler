from bs4 import BeautifulSoup
import xlwt
import requests


def get_movie(url):
    try:
        response =  requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def parse_content(html, sheet):
    soup = BeautifulSoup(html, 'lxml')
    movie_list = soup.find(class_='grid_view').find_all('li')
    for movie in movie_list:
        movie_name = movie.find(class_='title').string
        movie_img = movie.find('a').find('img').get('src')
        movie_cast = movie.find(class_='bd').find('p').text
        movie_rank = movie.find('em').string
        movie_rating = movie.find(class_="rating_num").string
        try:
            movie_quote = movie.find(class_="inq").text
        except AttributeError:
            movie_quote = "无"
        n = int(movie_rank)
        sheet.write(n, 0, movie_rank)
        sheet.write(n, 1, movie_name)
        sheet.write(n, 2, movie_rating)
        sheet.write(n, 3, movie_cast)
        sheet.write(n, 4, movie_quote)
        sheet.write(n, 5, movie_img)
        print("爬取电影： " + movie_rank + " | " + movie_name + " | " + movie_rating + " | " + movie_cast)
    return sheet


def douban_top250():
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)
    sheet.write(0, 0, '排名')
    sheet.write(0, 1, '名称')
    sheet.write(0, 2, '评分')
    sheet.write(0, 3, '制作团队')
    sheet.write(0, 4, '经典影评')
    sheet.write(0, 5, '图片')
    for page in range(10):
        url = r"https://movie.douban.com/top250?start=" + str(page * 25) + "&filter="
        html = get_movie(url)
        sheet = parse_content(html, sheet)
    print("豆瓣评分前250部电影爬取完毕!!!")
    book.save(u'豆瓣电影评分TOP250.xls')


if __name__ == "__main__":
    douban_top250()