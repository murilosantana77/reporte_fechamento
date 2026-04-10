from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json
import os

def main():
    # Configurações para rodar no GitHub Actions (Headless)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080') 
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20) 
    
    try:
        # 1. ACESSAR DOMÍNIO RAIZ E INJETAR COOKIES
        print("Acessando o domínio raiz para preparar a sessão...")
        driver.get("https://script.google.com")
        time.sleep(2)

        print("Injetando cookies de sessão do GitHub Secrets...")
        cookies_str = os.environ.get("COOKIES_SESSAO")
        
        if cookies_str:
            cookies_list = json.loads(cookies_str)
            for cookie in cookies_list:
                # O Selenium às vezes recusa cookies com o atributo 'sameSite', então removemos
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                driver.add_cookie(cookie)
            print("✅ Cookies injetados com sucesso.")
        else:
            print("⚠️ AVISO: O segredo COOKIES_SESSAO não foi encontrado ou está vazio!")

        # 2. ACESSAR O PAINEL DE DESENVOLVIMENTO
        print("Acessando o link do Google Apps Script...")
        url = "https://script.google.com/a/macros/shopee.com/s/AKfycby9ezG_TJrxTuCrEzXiIzs1Nc0ePz-TW-0JgfFXhrg/dev"
        driver.get(url)
        
        # Aguarda um tempo maior aqui para garantir que a página logada carregue totalmente
        time.sleep(10) 
        
        # 3. TENTAR CLICAR EM "COPIAR"
        print("Procurando o botão 'Copiar'...")
        try:
            btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[1]")))
            btn_copiar.click()
            print("✅ Botão 'Copiar' clicado via XPath.")
        except:
            print("⚠️ XPath do botão 'Copiar' falhou. Tentando localizar pela escrita...")
            btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Copiar')]")))
            btn_copiar.click()
            print("✅ Botão 'Copiar' clicado via texto.")

        print("Aguardando 10 segundos para a caixa do SeaTalk aparecer...")
        time.sleep(10)

        # 4. TENTAR CLICAR EM "SEATALK"
        print("Procurando o botão 'SeaTalk'...")
        try:
            btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[2]")))
            btn_seatalk.click()
            print("✅ Botão 'SeaTalk' clicado via XPath.")
        except:
            print("⚠️ XPath do botão 'SeaTalk' falhou. Tentando localizar pela escrita...")
            btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SeaTalk')]")))
            btn_seatalk.click()
            print("✅ Botão 'SeaTalk' clicado via texto.")

        print("Aguardando 5 segundos para envio da mensagem...")
        time.sleep(5)
        
        # Tirar print de confirmação
        driver.save_screenshot("sucesso_print.png")
        print("📸 Print final salvo com sucesso.")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")
        driver.save_screenshot("erro_print.png")
        sys.exit(1) 
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
