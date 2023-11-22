# 引入相关模块
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import random
import time
import pyautogui
import numpy as np
# 方法：题干 —> 选项


def choose_answer():
    score = min(max(int(np.random.normal(75, 15)), 0), 100)

    # 根据分数确定倾向选择的选项
    if score <= 40:
        return 3  # 40分的选项
    elif score <= 60:
        return 2  # 60分的选项
    elif score <= 80:
        return 1  # 80分的选项
    elif score <= 100:
        return 0  # 100分的选项


# 滚动方法,scroPx为滚动距离
def scrop(driver, scroPx):
    # 滚动脚本
    js = "var q=document.documentElement.scrollTop=" + str(scroPx)
    # 脚本执行
    driver.execute_script(js)
    # 延时
    time.sleep(1)


# 单选题
def single(driver):
    # 页面中有7个单选题
    for j in range(2, 9):
        # 每个单选题所在的位置
        # sinPro = driver.find_elements(By.XPATH, f'//*[@id="div{j}"]')
        sinPro = driver.find_elements(By.CSS_SELECTOR, f'#div{j} > div.ui-controlgroup.column1')
        # 每个单选题的答案进行遍历
        for answer in sinPro:
            # 对应每个单选题的选项组合
            ansItem = answer.find_elements(By.CSS_SELECTOR, '.ui-radio')
            index = choose_answer()
            # 随机点击选项
            ansItem[index].click()
            # 答题时间间隔
            time.sleep(random.randint(0, 1))


# 滑动题
def slide(driver):
    sli_ele = driver.find_element(By.XPATH, '//*[@id="jsrs_q1"]/div[2]')

    action = ActionChains(driver)
    action.click_and_hold(sli_ele)
    score = min(max(int(np.random.normal(80, 10)), 0), 100)

    action.move_by_offset(score*6.14, 0)
    action.release()
    action.perform()


# 脚本执行方法
def launch(nums):
    for i in range(0, nums):
        # 初始配置，问卷星地址
        url_survey = 'https://www.wjx.cn/vm/ONwmm6w.aspx'
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=option)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        driver.get(url_survey)

        # 调用单选题方法
        slide(driver)
        time.sleep(random.randint(0, 1))
        single(driver)
        time.sleep(random.randint(0, 1))

        # 调用滚动屏幕方法
        scrop(driver, 600)
        # 提交按钮
        driver.find_element(By.CSS_SELECTOR, '#ctlNext').click()  # 找到提交的css并点击
        time.sleep(4)
        print('已经提交了{}次问卷'.format(int(i) + int(1)))
        time.sleep(6)
        driver.quit()  # 停止


if __name__ == "__main__":
    # 填写问卷次数
    launch(150)
