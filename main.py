import httpx, string, secrets, threading, json  
from captchatools import captcha_harvesters, exceptions
from random import choice 
from colorama import Fore, init

config = json.load(open('./config.json', encoding='utf-8'))

class creator():
    def __init__(self):
        self.password = config['password']
        self.username = secrets.choice(string.ascii_letters) + secrets.choice(string.ascii_letters) + secrets.choice(string.ascii_letters)
        self.email = secrets.choice(string.ascii_letters) + secrets.choice(string.ascii_letters) + secrets.choice(string.ascii_letters) + secrets.choice(string.ascii_letters) + secrets.choice(string.ascii_letters) + "@gmail.com"
        self.captchakey = config['apikey']
    
    def account(self):
        self.proxy = ""
        with open("proxies.txt", "r") as f:
            proxy = "http://" + choice(f.readlines()).strip()
        solver = captcha_harvesters(solving_site=1, api_key=f"{self.captchakey}", sitekey=f"3e48b1d1-44bf-4bc4-a597-e76af6f3a260", captcha_type="hcap", captcha_url="https://tellonym.me/")
        self.recaptcha_answer = solver.get_token()
        with httpx.Client(headers={'authority': 'api.tellonym.me','accept': 'application/json','accept-language': 'en-GB,en;q=0.9,en-US;q=0.8','content-type': 'application/json;charset=utf-8','origin': 'https://tellonym.me','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','tellonym-client': 'web:0.62.1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'}, proxies=proxy) as client:
            resp = client.post("https://api.tellonym.me/accounts/register", json={'deviceName': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.6','deviceType': 'web','lang': 'en','hCaptcha': self.recaptcha_answer,'email': self.email,'password': self.password,'username': self.username,'limit': 25,})
            self.accesstoken = resp.json()["accessToken"]
            if self.accesstoken == [""]:
                print("[!] Failed To Register")
            else:
                print(f"{Fore.RED}[+]{Fore.RESET} Successfully Registered {Fore.GREEN}{self.accesstoken}{Fore.RESET} ")
                with open("accounts.txt", "a") as f:
                    f.write(f"{self.accesstoken}\n")
                    f.close()
                print(f"{Fore.RED}[+]{Fore.RESET} Saved Accesstoken To File!")

    def main(self):
        for i in range(5): # amount on threads in here
            t = threading.Thread(target=creator().account())
            t.start()

if __name__ == '__main__':
    creator().main()