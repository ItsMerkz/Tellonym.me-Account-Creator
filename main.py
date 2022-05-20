import httpx, string, threading, json  
from captchatools import captcha_harvesters, exceptions
import random 
from colorama import Fore, init

config = json.load(open('./config.json', encoding='utf-8'))
    
def account(self):
    try:
        with open("proxies.txt", "r") as f:
            proxy = "http://" + random.choice(f.readlines()).strip()
        solver = captcha_harvesters(solving_site=1, api_key=config["apikey"], sitekey=f"3e48b1d1-44bf-4bc4-a597-e76af6f3a260", captcha_type="hcap", captcha_url="https://tellonym.me/")
        hcaptcha_answer = solver.get_token()
        with httpx.Client(headers={'authority': 'api.tellonym.me','accept': 'application/json','accept-language': 'en-GB,en;q=0.9,en-US;q=0.8','content-type': 'application/json;charset=utf-8','origin': 'https://tellonym.me','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','tellonym-client': 'web:0.62.1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'}, proxies=proxy) as client:
            resp = client.post("https://api.tellonym.me/accounts/register", json={'deviceName': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.6','deviceType': 'web','lang': 'en','hCaptcha': hcaptcha_answer,'email': ''.join(random.choice(string.ascii_uppercase) for i in range(8)) + "@gmail.com",'password': ''.join(random.choice(string.ascii_uppercase) for i in range(8)) + "@100!",'username': ''.join(random.choice(string.ascii_uppercase) for i in range(8)),'limit': 25,})
            accesstoken = resp.json()["accessToken"]
            if accesstoken == [""]:
                print("[!] Failed To Register")
            else:
                print(f"{Fore.RED}[+]{Fore.RESET} Successfully Registered {Fore.GREEN}{accesstoken}{Fore.RESET} ")
                with open("accounts.txt", "a") as f:
                    f.write(f"{accesstoken}\n")
                    f.close()
                print(f"{Fore.RED}[+]{Fore.RESET} Saved Accesstoken To File!")
    except Exception as err:
        print("Error: %s" % err)

def main():
    for i in range(int(config["threads"])): # amount on threads in here
        t = threading.Thread(target=account())
        t.start()

if __name__ == '__main__':
    print("Generating Accounts With:\n%s!" % int(config["threads"]))
    main()
