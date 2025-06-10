import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def send_email(text):
    sender_email = "pmart4261@gmail.com"
    sender_password = "eiov bchh scrb zdhz"  # Gmail 应用专用密码

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = "yyp.0526@outlook.com"
    msg['Subject'] = Header("Popmart mmmmmmmm 补货啦，快去抢购！/n https://www.popmart.com/au/products/1990/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box", "utf-8")
    msg.attach(MIMEText(text, "plain", "utf-8"))

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, ["yyp.0526@outlook.com"], msg.as_string())
        print("✅ 邮件发送成功")
    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")

# 商品页面 URL
PRODUCT_URL = "https://www.popmart.com/au/products/1990/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box"
REFRESH_INTERVAL = 10  # 刷新间隔秒数

# 设置 Chrome 浏览器选项
options = uc.ChromeOptions()
#options.add_argument('--headless')  # 如需无头可以取消注释
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 使用 undetected-chromedriver 初始化 driver
driver = uc.Chrome(options=options)

# 控制变量
max_iterations = 40
count = 0
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)


try:
    while True:
        got_stock = False 
        if count % max_iterations == 0 and count != 0:
            print("🔁 达到刷新上限，重启浏览器中...")
            driver.quit()
            # 设置 Chrome 浏览器选项
            options = uc.ChromeOptions()
            #options.add_argument('--headless')  # 如需无头可以取消注释
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            # 使用 undetected-chromedriver 初始化 driver
            driver = uc.Chrome(options=options)

        driver.get(PRODUCT_URL)
        print(f"🔄 第 {count + 1} 次刷新页面中...")

        time.sleep(2)
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.policy_acceptBtn__ZNU71"))
            )
            print("found the button")
            driver.execute_script("arguments[0].click();", accept_button)
        except:
            pass
               
        try:
            print("box")
           

            box = wait.until(EC.element_to_be_clickable((
                By.XPATH,  "//div[text()='Whole Set']")))
            box.click()


            print(box)
            buy_button = driver.find_element(By.XPATH, "//div[text()='BUY NOW']")
            if buy_button.is_displayed():
                send_email("popmart s3 一盒 一盒 一盒 有货了！！！")
                buy_button.click()
                time.sleep(3)
                print("🧩 检测到【一盒】并购买")
                got_stock = True
        except Exception as e:
            #print(e)
            print(f" box 暂时无货")

        logined_in = False

        if got_stock:
            
            try:

                try:
                    # 尝试找到 "CHECKOUT AS MEMBER" 按钮，并等待它可点击
                    span = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='CHECKOUT AS MEMBER']")))
                    # 如果找到了并且可点击，点击它
                    span.click()
                    print("点击了 'CHECKOUT AS MEMBER' 按钮")
                except Exception as e:
                    # 如果找不到或无法点击，跳过并不做处理
                    print("没有找到 'CHECKOUT AS MEMBER' 按钮，跳过点击操作")

                email_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="email"]')))
                email_input.clear()
                actions.move_to_element(email_input).click().send_keys("yyp.0526@outlook.com").perform()

                continue_btn = wait.until(EC.element_to_be_clickable((
                    By.XPATH, '//button[contains(@class, "index_loginButton__") and text()="CONTINUE"]')))
                continue_btn.click()

                password_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="password"]')))
                password_input.clear()
                actions.move_to_element(password_input).click().send_keys("Skydo0526?").perform()

                time.sleep(0.5)
                signin_btn = driver.find_element(By.XPATH, '//button[contains(@class, "index_loginButton__") and text()="SIGN IN"]')
                driver.execute_script("arguments[0].click();", signin_btn)

                print("登陆成功")
                logined_in = True
                
            except Exception as e:
                print(f"❌ 登录失败: {e}")
                    
        
        if logined_in:
            

            try:
                max_attempts = 100  # 最大尝试次数
                attempt = 0  # 当前尝试次数
              
                while attempt < max_attempts:
                    try:
                        button = wait.until(EC.element_to_be_clickable((
                            By.XPATH, "//button[contains(text(), 'PROCEED TO PAY')]"
                        )))
                        button.click()
                        break
                    except Exception as e:
                        print(f"尝试 {attempt + 1}/{max_attempts} 失败: {e}")
                        time.sleep(2)  # 等待2秒后再重试
                        attempt += 1  # 尝试次数加1
                
                # while attempt < max_attempts:
                #     try:
                #         payment_option = wait.until(EC.element_to_be_clickable((
                #             By.XPATH, "//span[@class='index_radio__UGOaV']"
                #         )))
                #         payment_option.click()
                #         break
                #     except Exception as e:
                #         print(f" 换成creditcatd 尝试 {attempt + 1}/{max_attempts} 失败: {e}")
                #         time.sleep(2)  # 等待2秒后再重试
                #         attempt += 1  # 尝试次数加1



                # payment_option = wait.until(EC.element_to_be_clickable((
                #     By.XPATH, "//div[contains(@class, 'index_optionItemActive') and contains(., 'CreditCard')]"
                # )))
                # payment_option.click()

                # card_number_input = wait.until(EC.visibility_of_element_located((
                #     By.CSS_SELECTOR, "input[aria-label='Card number']"
                # )))

                # # Input the card number
                # card_number = "1234 5678 9012 3456"
                # actions.move_to_element(card_number_input).click().send_keys(card_number).perform()


                # expiry_date_input = wait.until(EC.visibility_of_element_located((
                #     By.CSS_SELECTOR, "input[aria-label='Expiry date']"
                # )))

                # # Input the expiry date (MM/YY)
                # expiry_date = "12/25"
                # actions.move_to_element(expiry_date_input).click().send_keys(expiry_date).perform()

                # security_code_input = wait.until(EC.visibility_of_element_located((
                #     By.CSS_SELECTOR, "input[aria-label='Security code']"
                # )))

                # security_code = "123"
                
                # actions.move_to_element(security_code_input).click().send_keys(security_code).perform()

                # holder_name_input = wait.until(EC.visibility_of_element_located((
                #     By.NAME, "holderName"
                # )))

                # holder_name = "him yang"
                # actions.move_to_element(holder_name_input).click().send_keys(holder_name).perform()

                # pay_button = wait.until(EC.element_to_be_clickable((
                #     By.CLASS_NAME, "adyen-checkout__button--pay"
                # )))

                # # Click the button
                # pay_button.click()
                # time.sleep(40)

            except Exception as e:
                print(f"❌ 支付失败: {e}")
                time.sleep(40)
                break
        
        
        time.sleep(REFRESH_INTERVAL)
        count += 1

finally:
    print("ok")
    #driver.quit()
