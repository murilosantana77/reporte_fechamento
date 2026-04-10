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
        print("Acessando o domínio principal do Google para preparar a sessão...")
        driver.get("https://google.com")
        time.sleep(2)

        print("Injetando cookies de sessão do GitHub Secrets...")
        cookies_str = os.environ.get("COOKIES_SESSAO")
        
        if cookies_str:
            cookies_list = json.loads(cookies_str)
            for cookie in cookies_list:
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                
                # Tenta adicionar o cookie. Ignora se o domínio for incompatível.
                try:
                    driver.add_cookie(cookie)
                except:
                    pass
                    
            print("✅ Tentativa de injeção de cookies finalizada.")
        else:
            print("⚠️ AVISO: O segredo COOKIES_SESSAO não foi encontrado ou está vazio!")

        # 2. ACESSAR O PAINEL DE DESENVOLVIMENTO
        print("Acessando o link do Google Apps Script...")
        url = "https://script.google.com/a/macros/shopee.com/s/AKfycby9ezG_TJrxTuCrEzXiIzs1Nc0ePz-TW-0JgfFXhrg/dev"
        driver.get(url)
        
        print("Aguardando 10 segundos para a página carregar...")
        time.sleep(10) 

        # 3. MERGULHAR NO IFRAME DO APPS SCRIPT
        print("Procurando o iframe do painel...")
        try:
            # Encontra o primeiro iframe da página e entra nele
            iframe_principal = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(iframe_principal)
            print("✅ Entrou no iframe principal.")
            
            # O Apps Script frequentemente coloca o conteúdo real em um segundo iframe interno
            time.sleep(2)
            iframes_internos = driver.find_elements(By.TAG_NAME, "iframe")
            if len(iframes_internos) > 0:
                driver.switch_to.frame(iframes_internos[0])
                print("✅ Entrou no iframe interno do Apps Script.")
        except Exception as e:
            print("⚠️ Não achou iframe, vai tentar na página principal mesmo.")
        
        # 4. TENTAR CLICAR EM "COPIAR"
        print("Procurando o botão 'Copiar'...")
        try:
            btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Copiar')]")))
            btn_copiar.click()
            print("✅ Botão 'Copiar' clicado com sucesso.")
        except:
            print("⚠️ Falha ao clicar no Copiar.")
            raise Exception("Botão Copiar não encontrado dentro do iframe.")

        print("Aguardando 10 segundos para a caixa do SeaTalk aparecer...")
        time.sleep(10)

        # 5. TENTAR CLICAR EM "SEATALK"
        print("Procurando o botão 'SeaTalk'...")
        try:
            btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SeaTalk')]")))
            btn_seatalk.click()
            print("✅ Botão 'SeaTalk' clicado com sucesso.")
        except:
            print("⚠️ Falha ao clicar no SeaTalk.")
            raise Exception("Botão SeaTalk não encontrado na tela.")

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
