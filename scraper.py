import lxml.html as html
import requests
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_NEWS = '//text-fill/a[not(@class="los-mejores-colegios-de-2020-especialesSect")]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]//text-fill/span/text()'
XPATH_ABSTRACT = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p/text()'


def parse_new(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            new_content = response.content.decode('utf-8')
            parsed_new = html.fromstring(new_content)

            try:
                title = parsed_new.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                abstract = parsed_new.xpath(XPATH_ABSTRACT)[0]
                body = parsed_new.xpath(XPATH_BODY)
            except IndexError as ie:
                return 0
            except Exception as e:
                print(e)
                return 0

            with open(f'{today}/{title}.txt', "w", encoding='utf-8') as f:
                f.write(title+"\n\n")
                f.write(abstract+"\n\n")
                for p in body:
                    f.write(p+"\n")
            return 1
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        return 0
    except Exception as e:
        print("Sth bad happened: " + e)
        return 0


def parse_home():
    try:
        # make a request to the url
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            # response.content brings the html content of the response
            # .decode for python to understand all especial characters
            home = response.content.decode('utf-8')
            # transform to a html we can use xpath
            parsed = html.fromstring(home)
            # extract the info that the xpath tells
            links_to_news = parsed.xpath(XPATH_LINK_TO_NEWS)
            # print(links_to_news)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            ok_news_counter = 0
            print("Processing news...")
            for link in links_to_news:
                ok_news_counter += parse_new(link, today)
            print(f'The number of ok news are: {ok_news_counter} out of {len(links_to_news)} news')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print("Sth bad happened: " + e)


def main():
    parse_home()


if __name__ == '__main__':
    main()
