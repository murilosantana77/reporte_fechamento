from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json
import os

os.environ['TZ'] = 'America/Sao_Paulo'
try:
    time.tzset() # Aplica o fuso horário no ambiente Linux/Vercel
except AttributeError:
    pass # Ignora se rodar localmente no Windows (que não suporta tzset)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 60) 
    
    try:
        # 1. PREPARAR SESSÃO
        print("Preparando sessão com cookies...")
        driver.get("https://google.com")
        cookies_str = os.environ.get("COOKIES_SESSAO")
        if cookies_str:
            cookies_list = json.loads(cookies_str)
            for cookie in cookies_list:
                if 'sameSite' in cookie: del cookie['sameSite']
                try: driver.add_cookie(cookie)
                except: pass

        # 2. ACESSAR DASHBOARD
        print("Acessando o dashboard do SOC SP5...")
        url = "https://script.google.com/a/macros/shopee.com/s/AKfycby9ezG_TJrxTuCrEzXiIzs1Nc0ePz-TW-0JgfFXhrg/dev"
        driver.get(url)
        
        # 3. ENTRAR NOS IFRAMES
        print("Navegando pelos iframes...")
        iframe_principal = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe_principal)
        time.sleep(2)
        iframes_internos = driver.find_elements(By.TAG_NAME, "iframe")
        if len(iframes_internos) > 0:
            driver.switch_to.frame(iframes_internos[0])

        # 4. ESPERA DINÂMICA PELOS DADOS
        print("Aguardando carregamento dos dados (Data de hoje)...")
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Aguardando dados')]")))
            print("✅ Dashboard carregado com sucesso!")
        except:
            print("⚠️ Aviso: O dashboard demorou para carregar, tentando prosseguir...")

        # Pausa extra para renderização visual
        time.sleep(10)

        # 5. CLICAR COPIAR
        print("Clicando no botão 'Copiar'...")
        xpath_copiar = "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[1]"
        btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_copiar)))
        driver.execute_script("arguments[0].click();", btn_copiar)

        time.sleep(10)

        # 6. CLICAR SEATALK
        print("Clicando no botão 'SeaTalk'...")
        xpath_seatalk = "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[2]"
        btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_seatalk)))
        driver.execute_script("arguments[0].click();", btn_seatalk)

        time.sleep(5)
        driver.save_screenshot("sucesso_print.png")
        print("📸 Processo finalizado com print de sucesso.")

    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        driver.save_screenshot("erro_print.png")
        sys.exit(1) 
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
