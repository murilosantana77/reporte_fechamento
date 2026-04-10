from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import json
import os

def main():
    options = webdriver.ChromeOptions()
    
    # =====================================================================
    # AS MUDANÇAS ESTÃO AQUI: Configurações anti-bloqueio e novo motor Headless
    # =====================================================================
    options.add_argument('--headless=new') # Usa o novo motor de renderização (idêntico ao Chrome real)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled') # Esconde que é o Selenium
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36') # Finge ser um PC normal
    
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
        
        print("Aguardando 40 segundos para a página carregar...")
        time.sleep(40) 

        # 3. MERGULHAR NO IFRAME DO APPS SCRIPT
        print("Procurando o iframe do painel...")
        try:
            iframe_principal = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(iframe_principal)
            print("✅ Entrou no iframe principal.")
            
            time.sleep(2)
            iframes_internos = driver.find_elements(By.TAG_NAME, "iframe")
            if len(iframes_internos) > 0:
                driver.switch_to.frame(iframes_internos[0])
                print("✅ Entrou no iframe interno do Apps Script.")
        except Exception as e:
            print("⚠️ Não achou iframe, vai tentar na página principal mesmo.")
        
        # Mantemos o tempo alto para dar tempo do Apps Script rodar tudo no novo motor
        print("Aguardando 35 segundos para o dashboard puxar os KPIs da planilha e desenhar os gráficos...")
        time.sleep(35) 

        # 4. TENTAR CLICAR EM "COPIAR"
        print("Procurando o botão 'Copiar' pelo XPath exato...")
        try:
            xpath_copiar = "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[1]"
            btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_copiar)))
            
            try:
                btn_copiar.click()
                print("✅ Botão 'Copiar' clicado via Selenium.")
            except:
                driver.execute_script("arguments[0].click();", btn_copiar)
                print("✅ Botão 'Copiar' clicado via JavaScript.")
                
        except Exception as e:
            print("⚠️ Falha ao achar o Copiar.")
            raise Exception(f"Botão Copiar não encontrado no XPath: {e}")

        print("Aguardando 10 segundos para a caixa do SeaTalk aparecer...")
        time.sleep(10)

        # 5. TENTAR CLICAR EM "SEATALK"
        print("Procurando o botão 'SeaTalk' pelo XPath exato...")
        try:
            xpath_seatalk = "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[2]"
            btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_seatalk)))
            
            try:
                btn_seatalk.click()
                print("✅ Botão 'SeaTalk' clicado via Selenium.")
            except:
                driver.execute_script("arguments[0].click();", btn_seatalk)
                print("✅ Botão 'SeaTalk' clicado via JavaScript.")
                
        except Exception as e:
            print("⚠️ Falha ao achar o SeaTalk.")
            raise Exception(f"Botão SeaTalk não encontrado no XPath: {e}")

        print("Aguardando 5 segundos para envio da mensagem...")
        time.sleep(5)
        
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
