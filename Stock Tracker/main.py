from utils import stock_price_assessment


def retrieve_articles(article_list: list):
    if article_list:
        print('Articles found:')
        if len(article_list) > 10:
            articles = article_list[:10]
        read_article = True
        while read_article:
            for art_no in range(len(articles)):
                print(f'{art_no + 1}')
                art = articles[art_no]
                print(f'Source: {art["source"]["name"]}')
                print(f'Title: {art["title"]}')
                print(f'Author: {art["author"]}')
                print('\n')
            index = input('Pick any article from below [1-10] or press "q" to quit\n')
            if index == 'q':
                read_article = False
            elif int(index) > 10 or int(index) < 1:
                print('Incorrect choice')
                other = input('See another article? (Y/N)')
                if other.lower() == 'n':
                    read_article = False
                continue
            else:
                referred_article = articles[int(index) - 1]
                # print(referred_article)
                print(referred_article['title'])
                print(referred_article['description'])
                other = input('See another article? (Y/N)')
                if other.lower() == 'n':
                    read_article = False
        print('Thanks for using our app!')


articles = stock_price_assessment('NVDA', 7, 0.01)
retrieve_articles(articles)
