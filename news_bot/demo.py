from newspaper import Article

url = 'https://www.axismag.jp/posts/2024/08/597435.html'
article = Article(url)

article.download()
article.parse()

print(article.title)
print(article.text)
