import urllib2
from bs4 import BeautifulSoup
import json
import csv
import sys



# and other libraries


class IMDb_crawler():
    def crawl (self, limit=100, min_rating=5):
        print "how many movies u wanna crawl: "
        limit = input()
        print "crawling...."
        genres = (
            "action",
            "comedy",
            "mystery",
            "sci_fi",
            "adventure",
            "fantasy",
            "horror",
            "animation",
            "drama",
            "thriller")
        iteration = 0
        count = 0
        movie_data = {}
        while count < limit:
            for genre in genres:
                print count
                if count > limit:
                    break
                c = self.get_webpage(genre, iteration)
                if c is None:
                    continue
                # change to c.read() later on
                soup = BeautifulSoup(c.read())
                self.get_movie_data(soup, min_rating, movie_data)
                print movie_data

                count += 50
                iteration += 1
                with open("movie.json", "w") as movie_file:
                    json.dump(movie_data, movie_file)
                    print "written to json"
        self.json_to_csv()

    def get_webpage (self, genre, iteration):
        try:
            self.url = "http://www.imdb.com/search/title?at=0&genres=" + genre + \
                       "&sort=moviemeter,asc&start=" + str(iteration * 50 + 1) + "&title_type=feature"
            c = urllib2.urlopen(self.url)
            return c
        except Exception, e:
            print "error is ", e
            print "could not open url", self.url
            return None

    def get_movie_data (self, soup, min_rating, movie_data):
        movies_contents = soup.find_all("div", class_="lister-item mode-advanced")
        for movie_content in movies_contents:
            # print "************"
            name = self.get_movie_name(movie_content)
            # print name
            year = self.get_movie_year(movie_content)
            # print year
            # pdb.set_trace()
            movie_id = self.get_movie_id(movie_content)
            # print movie_id
            movies_url = self.get_movie_url(movie_content)
            # print movies_url
            rating = self.get_movie_rating(movie_content)
            # print rating
            # users = self.get_movie_users(td)
            summary = self.get_movie_summary(movie_content)
            # print summary
            genre = self.get_movie_genre(movie_content)
            # print genre
            movie_data[movie_id] ={
                'title': name,
                'year': year,
                'movie_id': movie_id,
                'rating': rating,
                'users': "users",
                'summary': summary,
                'genre': genre}
            # movie_data.append({'title':name,'year':year,'movie_id':movie_id,'rating':rating,'users':"users",'summary':summary,'genre':genre})

    def get_movie_name (self, movie_content):
        try:
            return movie_content.find(
                "h3", "lister-item-header").a.getText()
        except BaseException:
            print "check movie name tag in this url", self.url

    def get_movie_rating (self, movie_content):
        try:
            return movie_content.find(
                "div", "inline-block ratings-imdb-rating").get("data-value")
        except BaseException:
            print "error: rating"

    def get_movie_users (self, text):
        div = text.div.div
        if div.has_key('title') and div['title'].split()[
            0] == 'Users':
            value = div['title']
            temp = value.split()[4].split(
                '(')[1].split(',')
            return ''.join(temp)
        else:
            return 0

    def get_movie_year (self, movie_content):
        try:
            year = movie_content.find("h3", "lister-item-header").find(
                "span", "lister-item-year text-muted unbold").getText()
            for ch in [
                '(', ')', '{', '}', '[', ']']:
                year.replace(ch, " ")
                return year.strip()
        except BaseException:
            print "check movie year tag in this url", self.url

    def get_movie_id (
            self, movie_content):
        try:
            return movie_content.find(
                "h3", "lister-item-header").a.get("href")[7:-16]
        except BaseException:
            print "check movie id tage in this url", self.url

    def get_movie_url (
            self, movie_content):
        try:
            return movie_content.find(
                "h3", "lister-item-header").a.get("href").strip()
        except BaseException:
            print "check movie id tage in this url", self.url

    def get_movie_genre (
            self, movie_content):
        try:
            return movie_content.find_all(
                "p", "text-muted")[0].find("span", "genre").getText().strip()
        except BaseException:
            print "error genre"

    def get_movie_summary (
            self, movie_content):
        try:
            return movie_content.find_all(
                "p", "text-muted")[1].getText().strip()
        except BaseException:
            print "error:summary"

    def json_to_csv(self):
        try:
            print "in json conversion"
            file = open('movie.json',"r")
            data = json.load(file)
            file.close()
            file = csv.writer(open('movie.csv',"w"))
            file.writerow(["movie_id","users","title","summary","year","genre"])
            for line in data:
                print line
                print data[line]["rating"]
                file.writerow([data[line]["movie_id"],
                data[line]["users"], data[line]["title"], data[line]["summary"], data[line]["year"], data[line]["genre"]])
        except Exception as e:
            print "error ", e;




reload(sys)
sys.setdefaultencoding('utf-8')
crawler = IMDb_crawler()
crawler.crawl()

