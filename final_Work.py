# Bibliotekos kurias naudojau:
from PyQt6.QtWidgets import QApplication, QMainWindow
from final_project import Ui_MainWindow
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import csv


class MainWindow(QMainWindow):
    def __init__(self):
    
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.ok.clicked.connect(self.collect_inputs)

    def collect_inputs(self):
        
        url = self.ui.weburl.text()

        if "https://elenta.lt/" in url:         
            options = Options()
            options.add_argument('--incognito')
            options.add_argument('--headless')
            driver = webdriver.Chrome(options)
            driver.get(url)     
            
            total_amount = 0
            with open('data.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'Price'])
                source = driver.page_source
                html = BeautifulSoup(source, "html.parser")

                category = html.select_one("span[itemprop='itemListElement'] > span[itemprop='name']")
                category = category.text.strip().replace("»", "")
                

                number = html.select_one(".counter")
                number = number.text.strip()
                

                while True:
                    agree_button = driver.find_elements(By.CSS_SELECTOR, '.fc-button-label')
                    if agree_button:
                        agree_button[0].click()

                    
                    for box in html.select(".units-list li"):
                        if box:
                            title = box.select_one(".ad-hyperlink")
                            title = title.text.strip() if title else "Nenurodyta"

                            price = box.select_one(".price-box")
                            price = price.text.strip() if price else "0"

                            writer.writerow([title, price])
 
                            price = float(price.replace("€", "").replace(",", "").replace(" ","").strip())
                            total_amount += int(price)
                    next_button = driver.find_elements(By.CSS_SELECTOR, 'li.pagerNextPage')
                    if next_button:
                        next_button[0].click()
                        source = driver.page_source
                        html = BeautifulSoup(source, "html.parser")     
                        sleep(1)
                    else:
                        break      
                        
            driver.quit()
            self.ui.isvestis.setText(f"Kategorijoje: {category}\nYra {number} skelbimai \nBendra kainų suma yra {str(total_amount)}€")

        else:
            self.ui.isvestis.setText(f"{url} ivestas netinkamas tinklalapis") 
 

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("Final Work")
    window.show()
    app.exec()


    