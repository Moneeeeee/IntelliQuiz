"""
File: 1_GetAllProblemSetLink.py
Description: 把所有数据集的原始json爬取并且保存到1_GetAllProblemSetLink.json文件中
Author: Monee
Created Date: 2024-07-23
Last Modified Date: 2024-07-23
"""

import os
import pickle
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

# 配置Edge选项
options = Options()
# options.add_argument('--headless')  # 无头模式，不打开浏览器，如果需要看到实际操作请去掉这一行

# 启动Edge浏览器
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# 定义Cookies文件路径
cookies_file = '../cookies.pkl'

# 清除Cookies文件
def clear_cookies(cookies_file):
    if os.path.exists(cookies_file):
        os.remove(cookies_file)

# 加载Cookies
def load_cookies(driver, cookies_file):
    if os.path.exists(cookies_file):
        with open(cookies_file, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)

# 保存Cookies
def save_cookies(driver, cookies_file):
    with open(cookies_file, 'wb') as cookiesfile:
        pickle.dump(driver.get_cookies(), cookiesfile)

# 登录函数
def login():
    driver.get('https://pintia.cn/auth/login')  # 替换为实际的登录页面URL
    time.sleep(2)  # 等待页面加载
    load_cookies(driver, cookies_file)  # 加载Cookies
    driver.refresh()
    time.sleep(2)
    try:
        driver.find_element(By.CSS_SELECTOR, 'div.pc-image img[alt="Avatar"]')  # 检查头像图片元素
        print("Already logged in!")  # 如果找到头像元素，说明已经登录
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, 'div.teacher_tayqy[title="助教"]')  # 检查特定的div元素
            print("Already logged in!")  # 如果找到特定div元素，说明已经登录
        except:
            print("Not logged in. Proceeding with login...")  # 如果没有找到上述元素，则进行登录
            username_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="邮箱地址或手机号"]')
            password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="密码"]')
            username_input.send_keys('caohai@sdu.edu.cn')  # 使用新账号替换邮箱地址
            password_input.send_keys('sduwh2024')  # 使用新账号替换密码
            password_input.send_keys(Keys.RETURN)
            print("请手动完成滑块验证，然后按回车键继续...")
            input()  # 等待用户完成滑块验证
            time.sleep(5)
            try:
                driver.find_element(By.CSS_SELECTOR, 'div.pc-image img[alt="Avatar"]')
                print("Login successful!")  # 检查是否登录成功
            except:
                try:
                    driver.find_element(By.CSS_SELECTOR, 'div.teacher_tayqy[title="助教"]')
                    print("Login successful!")  # 检查是否登录成功
                except:
                    print("Login failed!")  # 如果登录失败，退出程序
                    driver.quit()
                    exit(1)
            save_cookies(driver, cookies_file)  # 登录成功后保存Cookies

# 使用已登录的会话发送API请求
def fetch_data_with_cookies():
    # 提取浏览器中的Cookies
    cookies = driver.get_cookies()
    session = requests.Session()

    # 将Cookies添加到会话中
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # 设置API端点
    api_url = 'https://pintia.cn/api/problem-sets/admin'

    # 获取所有数据
    all_problem_sets = []
    page = 0
    limit = 100  # 设置每页的数量
    while True:
        params = {
            'sort_by': '{"type":"UPDATE_AT","asc":false}',
            'page': page,
            'limit': limit,
            'filter': '{"ownerId":"0"}'
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        response = session.get(api_url, params=params, headers=headers)

        # 检查响应状态码
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            print(f"Response content: {response.text}")
            break

        # 打印响应内容以进行调试
        print(f"Response content for page {page}: {response.text}")

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response.text}")
            break

        problem_sets = data.get('problemSets', [])

        if not problem_sets:
            break  # 如果当前页没有数据，停止循环

        all_problem_sets.extend(problem_sets)
        print(f"Fetched page {page + 1}, {len(problem_sets)} problem sets")
        page += 1

    # 保存数据到JSON文件
    with open('1_AllProblemSetInfo.json', 'w', encoding='utf-8') as f:
        json.dump(all_problem_sets, f, ensure_ascii=False, indent=4)

    print(f"Total {len(all_problem_sets)} problem sets fetched and saved.")


if __name__ == "__main__":
    clear_cookies(cookies_file)  # 清除旧的Cookies文件
    login()  # 调用登录函数
    fetch_data_with_cookies()  # 使用已登录的会话发送API请求
    driver.quit()  # 关闭浏览器
