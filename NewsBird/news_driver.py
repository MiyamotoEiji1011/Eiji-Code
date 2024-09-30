from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    service = Service('.\chromedriver.exe')  # ここに手動でダウンロードしたChromeDriverのパスを指定
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def yahoo():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://news.yahoo.co.jp/search?p=%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88&ei=utf-8&categories=it'
        driver.get(url)

        # URL開くまで待機pip install webdriver-manager


        time.sleep(5)

        # 最新記事のURLを取得
        latest_news_element = driver.find_element(By.CLASS_NAME, 'newsFeed_item_link')
        latest_news_url = latest_news_element.get_attribute('href')
        
        return latest_news_url

    finally:
        # ブラウザを終了
        driver.quit()

def techable():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://techable.jp/'
        driver.get(url)

        # URL開くまで待機
        time.sleep(5)

        # 最新記事のURLを取得
        latest_news_element = driver.find_element(By.CLASS_NAME, 'te-articles__list__item__hit')
        latest_news_url = latest_news_element.get_attribute('href')
        
        return latest_news_url

    finally:
        # ブラウザを終了
        driver.quit()

def itemedia():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://www.itmedia.co.jp/aiplus/subtop/news/index.html'
        driver.get(url)

        # URL開くまで待機
        time.sleep(5)

        # 最新記事のURLを取得
        col_box_icon_set = driver.find_element(By.CLASS_NAME, 'dispatch-0')
        latest_news_element = col_box_icon_set.find_element(By.TAG_NAME, 'a')
        latest_news_url = latest_news_element.get_attribute('href')
        
        return latest_news_url

    finally:
        # ブラウザを終了
        driver.quit()

def gizmodo():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://www.gizmodo.jp/articles/'
        driver.get(url)

        # URL開くまで待機
        time.sleep(5)

        # 最新記事のURLを取得
        col_box_icon_set = driver.find_element(By.CLASS_NAME, 'p-archive-cardPost')
        latest_news_element = col_box_icon_set.find_element(By.TAG_NAME, 'a')
        latest_news_url = latest_news_element.get_attribute('href')
        
        return latest_news_url

    finally:
        # ブラウザを終了
        driver.quit()

def gigazine():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://gigazine.net/news/C37/' #カテゴライズされたURL
        driver.get(url)

        # URL開くまで待機
        time.sleep(5)

        # 最新記事のURLを取得
        col_box_icon_set = driver.find_element(By.CLASS_NAME, 'thumb')
        latest_news_element = col_box_icon_set.find_element(By.TAG_NAME, 'a')
        latest_news_url = latest_news_element.get_attribute('href')
        
        return latest_news_url

    finally:
        # ブラウザを終了
        driver.quit()

def axismag():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://www.axismag.jp/'
        driver.get(url)

        # 明示的な待機を使用して、ページが完全に読み込まれるまで待機
        wait = WebDriverWait(driver, 10)
        latest_news_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#post_lists a.ov_color')))

        # 最新記事のURLを取得
        latest_news_url = latest_news_element.get_attribute('href')

        return latest_news_url

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        # ブラウザを終了
        driver.quit()

def mynaviz():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://news.mynavi.jp/techplus/technology/'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        latest_news_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.c-gridList_nodelink.gtm')))
        latest_news_url = latest_news_element.get_attribute('href')

        return latest_news_url

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        # ブラウザを終了
        driver.quit()

def wired():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://wired.jp/'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        latest_news_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.SummaryItemHedLink-civMjp.hAREyO.summary-item-tracking__hed-link.summary-item__hed-link')))
        latest_news_url = latest_news_element.get_attribute('href')

        return latest_news_url

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        # ブラウザを終了
        driver.quit()

def thebridge():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://thebridge.jp/'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        div_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'entry-summery')))
        latest_news_element = div_element.find_element(By.TAG_NAME, 'a')
        latest_news_url = latest_news_element.get_attribute('href')

        return latest_news_url

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        # ブラウザを終了
        driver.quit()

def cne():
    driver = initialize_driver()
    try:
        # 指定URLを開く
        url = 'https://japan.cnet.com/'
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        div_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-main')))
        latest_news_element = div_element.find_element(By.TAG_NAME, 'a')
        latest_news_url = latest_news_element.get_attribute('href')

        return latest_news_url

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

    finally:
        # ブラウザを終了
        driver.quit()


if __name__ == "__main__":
    #print(itemedia())
    #print(gizmodo())
    #print(gigazine())
    #print(mynaviz())
    
    
    print("END")
