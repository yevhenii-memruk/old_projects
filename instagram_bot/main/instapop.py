import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from user_data import users_info
import time
import random
import os
import requests

from bs4 import BeautifulSoup as bs

"""Instagram Bot - InstaPOP.

Info:
This bot will help you keep your account more relevant and raise your activity to a high level

Features:
-Auto liking posts
-Auto subscription
-Auto liking posts by hashtag
-Make a list of all subscribers
-Download all media from instagram account
-Unsubscribe from profiles that do not follow you
-Automatic browsing of stories
"""


class InstaBot:
    def __init__(self, username, password, file_name):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")
        self.file_name = file_name

    # closing tab and quiting the browser
    def exit(self):
        self.browser.close()
        self.browser.quit()

    # checking by xpath if element exist
    def xpath_existing(self, xpath):
        browser = self.browser
        try:
            browser.find_element_by_xpath(xpath)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # signing into profile
    def sign_in(self):
        browser = self.browser
        try:
            browser.get("https://www.instagram.com/")
            browser.maximize_window()
            browser.implicitly_wait(10)
            # closing pop-up window
            browser.find_element_by_xpath("/html/body/div[3]/div/div/button[1]").click()
            time.sleep(1)

            name_tag = browser.find_element_by_name("username")
            name_tag.clear()
            for step_typing in self.username:
                time.sleep(random.uniform(0.1, 0.3))
                name_tag.send_keys(step_typing)

            password_tag = browser.find_element_by_name("password")
            password_tag.clear()
            for step_typing in self.password:
                time.sleep(random.uniform(0.1, 0.3))
                password_tag.send_keys(step_typing)

            time.sleep(1)
            password_tag.send_keys(Keys.ENTER)
            time.sleep(5)
        except Exception as ex:
            print(ex)
            self.exit()

    def open_profile(self, link):
        browser = self.browser
        try:
            browser.get(link)
        except NoSuchElementException:
            print("Sorry, this page isn't available.")

        time.sleep(random.randrange(2))

    # scrolling page and grab all url of posts into file
    def scrolling_get_urls(self):
        browser = self.browser
        all_post = []

        posts_num = int(
            browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
        # 12 posts loads each scrolling
        if posts_num < 12:
            loops_count = 1
        else:
            loops_count = int(posts_num / 12)

        try:
            for x in range(loops_count):
                time.sleep(random.randrange(1, 2))
                tag_a = browser.find_elements_by_tag_name("a")

                for href_a in tag_a:
                    href = href_a.get_attribute("href")
                    if "/p/" in href:
                        if href not in all_post:
                            all_post.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))
        except Exception as ex:
            print(ex)

        with open(f'{self.file_name}.txt', "w") as file_posts:
            for z in all_post:
                file_posts.write(z + "\n")

    # liking post by certain link
    def like_exactly_post(self, link_post):
        browser = self.browser

        time.sleep(3)
        browser.get(link_post)
        time.sleep(3)

        try:
            wrong_user_page = "/html/body/div[1]/section/main/div/h2"
            if self.xpath_existing(wrong_user_page):
                print("The post does not exist!")
            else:
                print("Post detected! Put our like!")

            like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
            if like:
                print("Like already put")
                self.exit()
            else:
                browser.find_element_by_xpath(
                    "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                time.sleep(random.randrange(2, 4))
                self.exit()
        except Exception as ex:
            print(ex)

    def like_by_hash(self, hashtag):
        global posts
        browser = self.browser

        try:
            browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            time.sleep(5)

            # !!! make number of scrolling manually change
            for x in range(1, 5):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

                refs = browser.find_elements_by_tag_name("a")

                posts = [i.get_attribute("href") for i in refs if "/p/" in i.get_attribute("href")]
                # for i in refs:
                #     href = i.get_attribute("href")
                #     if "/p/" in href:
                #        posts.append(href)

            for y in posts:
                browser.get(y)

                # check if like already exist
                like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
                if like:
                    print("Like already put")
                    continue
                elif posts[-1]:
                    self.exit()
                else:
                    browser.find_element_by_xpath(
                        "//*[@id=\"react-root\"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                    # make a delay due to Instagram restriction
                    time.sleep(random.randrange(80, 100))
        except Exception as ex:
            print(ex)

    def like_profile(self, url_profile):
        browser = self.browser

        time.sleep(random.randrange(1, 3))

        self.open_profile(url_profile)
        self.scrolling_get_urls()

        try:
            with open(f'{self.file_name}.txt', 'r') as file_reader:
                for like_post in file_reader:
                    time.sleep(1)
                    browser.get(like_post)
                    time.sleep(random.randrange(2))

                    wrong_user_page = "/html/body/div[1]/section/main/div/h2"
                    if self.xpath_existing(wrong_user_page):
                        print("The post does not exist!")
                    else:
                        print("Post detected! Put our like!")

                    like = browser.find_elements_by_css_selector("svg[fill = '#ed4956']")
                    if like:
                        print("Like already put")
                    else:
                        # make a delay due to Instagram restriction
                        time.sleep(random.randrange(80, 100))
                        browser.find_element_by_xpath(
                            "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                        time.sleep(random.randrange(2, 3))
        except Exception as ex:
            print(ex)

        self.exit()

    def download_media(self, url_profile):
        browser = self.browser
        file_name = url_profile.split("/")[-2]

        self.open_profile(url_profile)
        self.scrolling_get_urls()

        if os.path.exists(f'{file_name}'):
            print("Folder exist yet!")
        else:
            os.mkdir(f"{file_name}")

        # Clean folder with content
        for f in os.listdir(f"{file_name}"):
            os.remove(os.path.join(file_name, f))

        # OPTION 0
        # Download only images!
        # Make futures ( download video, download multiple post )
        with open(f"{self.file_name}.txt", "r") as file_reader:
            for like_post in file_reader:
                browser.get(like_post)

                try:
                    soup = bs(browser.page_source, 'lxml')

                    ''' Extract the url of the image from the source code'''
                    img = soup.find('img', class_='FFVAD')
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    if self.xpath_existing(video_src):
                        continue
                    img_url = img['src']

                    '''Download the image via the url using the requests library'''
                    r = requests.get(img_url)

                    with open(f"{file_name}" + "/" + "instagram" + str(time.time()) + ".png", 'wb') as f:
                        f.write(r.content)
                except Exception as ex:
                    print(ex)
        self.exit()

    # follow to exact profile
    def follow_exact_profile(self, url_profile):
        browser = self.browser
        follow_button = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button"

        self.open_profile(url_profile)
        if self.xpath_existing(follow_button):
            time.sleep(3)
            browser.find_element_by_xpath(follow_button).click()
        else:
            pass

        self.exit()

    # follow to all of user's followers
    def follow_engine(self, url_profile):
        num_scroll = 1
        browser = self.browser
        browser.get(url_profile)
        name_user = url_profile.split("/")[-2]

        time.sleep(2)

        # Create User folder
        if os.path.exists(f"{name_user}"):
            print("Folder already exist!")
        else:
            print("Create folder!")
            os.mkdir(name_user)

        num_followers = browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').get_attribute("title")
        if "," in num_followers:
            num_followers = int("".join(num_followers.split(",")))
        else:
            num_followers = int(num_followers)

        if num_followers <= 12:
            num_scroll = 1
        if num_followers > 12:
            num_scroll = int(num_followers / 12)

        browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()

        time.sleep(3)

        follower_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        follower_urls = []

        for scroll in range(num_scroll):
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follower_ul)
            time.sleep(2)

        all_divs = follower_ul.find_elements_by_tag_name("li")

        for link_follower in all_divs:
            link_follower = link_follower.find_element_by_tag_name("a").get_attribute("href")
            follower_urls.append(link_follower)

        with open(f"{name_user}/{name_user}.txt", "w") as file_urls:
            for iter_link in follower_urls:
                file_urls.write(iter_link + "\n")

        time.sleep(random.randrange(2, 3))

        with open(f"{name_user}/{name_user}.txt") as urls_reader:
            for user_url in urls_reader:
                try:
                    with open(f"{name_user}/{name_user}_following.txt") as check_list:
                        if user_url in check_list.readlines():
                            continue
                except Exception as ex:
                    print("File do not exist yet!")

                browser.get(user_url)

                follow_button = [
                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button",
                    "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button"]
                already_followed_button = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/span"
                our_profile = "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a"

                time.sleep(3)

                if self.xpath_existing(already_followed_button):
                    print("You have already subscribed to this user!")
                    continue
                if self.xpath_existing(follow_button[0]):
                    browser.find_element_by_xpath(follow_button[0]).click()
                    print("Following to " + user_url.split("/")[-2])
                if self.xpath_existing(our_profile):
                    print("It's me!")
                elif self.xpath_existing(follow_button[1]):
                    browser.find_element_by_xpath(follow_button[1]).click()
                    print("Following to " + user_url.split("/")[-2])

                # create a file to skip our following users
                with open(f"{name_user}/{name_user}_following.txt", "a") as following:
                    following.write(user_url)

                time.sleep(random.randrange(120, 180))

    # send message to certain account
    def send_direct_message(self, usernames="", message="", img_path=""):

        browser = self.browser

        direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

        if not self.xpath_existing(direct_message_button):
            print("Message button has not found!")
            self.exit()
        else:
            print("Send message..")
            browser.find_element_by_xpath(direct_message_button).click()
            time.sleep(random.randrange(2, 4))

        # close pop-up window
        if self.xpath_existing("/html/body/div[5]/div/div/div"):
            browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click()
        time.sleep(random.randrange(2, 4))

        browser.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # send message to several users
        for user in usernames:
            # enter the recipient's name
            to_input = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input")
            to_input.send_keys(user)
            time.sleep(random.randrange(2, 4))

            # choose recipient from list
            browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[2]/div[1]").find_element_by_tag_name(
                "button").click()
            time.sleep(random.randrange(2, 4))

        browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/div/button/div").click()
        time.sleep(random.randrange(2, 4))

        # sending text message
        if message:
            text_message_area = browser.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            text_message_area.send_keys(Keys.ENTER)
            print(f"Message for {usernames} sent succeed!")
            time.sleep(random.randrange(2, 4))

        # sending images
        if img_path:
            send_img_input = browser.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
            send_img_input.send_keys(img_path)
            print(f"Image for {usernames} sent succeed!")
            time.sleep(random.randrange(2, 4))

        self.exit()

    # unfollow method
    def unsubscribe_for_all_users(self, userpage):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        # if num followers more 999, delete comas
        if ',' in following_count:
            following_count = int(''.join(following_count.split(',')))
        else:
            following_count = int(following_count)

        time.sleep(random.randrange(2, 4))

        loops_count = int(following_count / 10) + 1
        print(f"Num reload page: {loops_count}")

        following_users_dict = {}

        for loop in range(1, loops_count + 1):

            count = 10
            browser.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.randrange(3, 6))

            # clil/open menu followers
            following_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

            following_button.click()
            time.sleep(random.randrange(3, 6))

            # take all li from lu, there are unfollow button and url to user
            following_div_block = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div")
            following_users = following_div_block.find_elements_by_tag_name("li")
            time.sleep(random.randrange(3, 6))

            for user in following_users:

                if not count:
                    break

                user_url = user.find_element_by_tag_name("a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                # add to dictionary pair values: name of user and url user
                following_users_dict[user_name] = user_url

                following_button = user.find_element_by_tag_name("button").click()
                time.sleep(random.randrange(3, 6))
                unfollow_button = browser.find_element_by_xpath(
                    "/html/body/div[6]/div/div/div/div[3]/button[1]").click()

                print(f"Iteration #{count} >>> Unfollow {user_name}")
                count -= 1

                # time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(2, 4))

        with open("following_users_dict.txt", "w", encoding="utf-8") as file:
            json.dump(following_users_dict, file)

        self.exit()

    # method unfollow unmutual users
    def smart_unsubscribe(self, username):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        followers_button = browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute("title")

        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        time.sleep(random.randrange(3, 6))

        # if num followers more 999, delete comas
        if ',' in followers_count or following_count:
            followers_count, following_count = int(''.join(followers_count.split(','))), int(
                ''.join(following_count.split(',')))
        else:
            followers_count, following_count = int(followers_count), int(following_count)

        followers_loops_count = int(followers_count / 12) + 1
        following_loops_count = int(following_count / 12) + 1

        # collect list followers
        followers_button.click()
        time.sleep(4)

        followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

        try:
            followers_urls = []
            print("Setup collection followers...")
            for i in range(1, followers_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Iteration #{i}")

            all_urls_div = followers_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                followers_urls.append(url)

            # save all followers to file
            with open(f"{username}_followers_list.txt", "a") as followers_file:
                for link in followers_urls:
                    followers_file.write(link + "\n")
        except Exception as ex:
            print(ex)
            self.exit()

        time.sleep(random.randrange(4, 6))
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        # collect list followings
        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_button.click()
        time.sleep(random.randrange(3, 5))

        following_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

        try:
            following_urls = []

            for i in range(1, following_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Iteration #{i}")

            all_urls_div = following_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                following_urls.append(url)

            # save followings to file
            with open(f"{username}_following_list.txt", "a") as following_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            """Compare two list, if users from following doesn't exist in follower list set it to separate list"""

            count = 0
            unfollow_list = []
            for user in following_urls:
                if user not in followers_urls:
                    count += 1
                    unfollow_list.append(user)
            print(f"Should unfollow from {count} users")

            # save all unmutual users to file
            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user + "\n")

            print("Unfollowing...")
            time.sleep(2)

            # enter to each user page and unfollow
            with open(f"{username}_unfollow_list.txt") as unfollow_file:
                unfollow_users_list = unfollow_file.readlines()
                unfollow_users_list = [row.strip() for row in unfollow_users_list]

            try:
                count = len(unfollow_users_list)
                for user_url in unfollow_users_list:
                    browser.get(user_url)
                    time.sleep(random.randrange(4, 6))

                    # button Unfollow
                    unfollow_button = browser.find_element_by_xpath(
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                    unfollow_button.click()

                    time.sleep(random.randrange(4, 6))

                    # confirmation
                    browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()

                    print(f"Unfollowed from {user_url}")
                    count -= 1

                    # time.sleep(random.randrange(120, 130))
                    time.sleep(random.randrange(4, 6))

            except Exception as ex:
                print(ex)
                self.exit()

        except Exception as ex:
            print(ex)
            self.exit()

        time.sleep(random.randrange(4, 6))
        self.exit()


# test = InstaBot(username, password, "test_list")

for user, user_data in users_info.items():
    username = user_data['login']
    password = user_data['password']
    test = InstaBot(username, password, "test_list")
    test.sign_in()
    test.smart_unsubscribe("alinaxody")
