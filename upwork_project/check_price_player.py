from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.options import Options

import telegram_alarm


class PriceChecker:

    def __init__(self):
        # hide process execution
        options = Options()
        options.add_argument("--headless")

        self.browser = webdriver.Chrome("chromedriver.exe", options=options)

    # checking by xpath if element exist
    def xpath_existing(self, xpath):
        browser = self.browser
        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # closing tab and quiting the browser
    def exit(self):
        self.browser.close()
        self.browser.quit()

    # getting info from the site
    def parse_info(self, web_page, delay, alert_percent):
        browser = self.browser
        browser.maximize_window()

        # open necessary num of tabs
        for num_tabs in range(len(web_page) - 1):
            browser.execute_script("window.open('');")
            browser.switch_to.window(browser.window_handles[0])

        # open players' pages in each tab
        for switch_to_open in range(len(web_page)):
            browser.switch_to.window(browser.window_handles[switch_to_open])
            browser.get(web_page[switch_to_open])

        # close pop-up
        accept_all_pop_up = "/html/body/div[1]/div[1]/div[2]/span[1]/a"
        if self.xpath_existing(accept_all_pop_up):
            browser.find_element_by_xpath(accept_all_pop_up).click()
        else:
            pass

        # get name and price
        price_football_player = {f"{price}" + web_page[price].split("/")[-2].translate({45: " "}).title(): 0 for
                                 price
                                 in range(len(web_page))}
        infinite_loop = True

        while infinite_loop:
            for switcher in range(len(web_page)):
                browser.switch_to.window(browser.window_handles[switcher])

                # reload page and delay
                browser.refresh()
                time.sleep(1)

                price = "/html/body/main/div[4]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]"
                if self.xpath_existing(price):
                    str_price = browser.find_element_by_xpath(price).text
                    player_name = list(price_football_player.keys())[switcher]
                    player_price_short = list(price_football_player.values())[switcher]

                    # use translate() method to exclude coma
                    exclude_come_to_none = {44: None}
                    int_price = int(str_price.translate(exclude_come_to_none))

                    # definer percent difference between last price and new one
                    try:
                        percent = (int_price - player_price_short) / player_price_short * 100
                        if percent < -alert_percent:
                            print(f"Price dropped by {format(percent, '.2f')}% !")

                            # load telegram bot to sending alert about price
                            telegram_alarm.alert_message(player_name[1:], int_price, percent, web_page[switcher])

                        if percent > alert_percent:
                            print(f"Price increased by {format(percent, '.2f')}% !")

                            # load telegram bot to sending alert about price
                            telegram_alarm.alert_message(player_name[1:], int_price, percent, web_page[switcher])

                        if percent == float(0):
                            print(f"\nNothing changed: {format(percent, '.2f')}% !")
                        if alert_percent > percent > 0:
                            print(f"Price increased by {format(percent, '.2f')}% !")
                        if -alert_percent < percent < 0:
                            print(f"Price dropped by {format(percent, '.2f')}% !")
                        else:
                            pass
                    except ZeroDivisionError:
                        print("\nFirst iteration...")

                    number_player = browser.find_element_by_xpath(
                        "/html/body/main/div[4]/div/div[2]/div/div[1]/div/div/div[5]").text

                    price_football_player[player_name] = int_price
                    print(f"{player_name[1:]} ({number_player}) : {price_football_player[player_name]:,}\n")

                    if switcher == len(web_page) - 1:
                        time.sleep(delay)
                    else:
                        continue
                else:
                    print("Have no such info!")


if __name__ == '__main__':
    test = PriceChecker()

    football_players = []
    apply = True
    while apply:
        print("\nTo APPLY, write \"apply\"\n")
        player_url = str(input("Write full url: "))
        if player_url.lower() == "apply":
            apply = False
        elif player_url in football_players:
            print("ALERT: This URL already exists!")
        else:
            football_players.append(player_url)

    delay_sec = int(input("Delay(sec): "))
    percent_alert = int(input("Percent(%): "))

    print("Program starts executing...")

    print(test.parse_info(football_players, delay_sec, percent_alert))
