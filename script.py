from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

def main():
    # Configurações para rodar no GitHub Actions (Headless)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080') # Resolução grande para garantir que os botões apareçam
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20) # Espera máxima de 20 segundos para carregar elementos
    
    try:
        print("Acessando o link do Google Apps Script...")
        url = "https://script.google.com/a/macros/shopee.com/s/AKfycby9ezG_TJrxTuCrEzXiIzs1Nc0ePz-TW-0JgfFXhrg/dev"
        driver.get(url)
        
        # NOTA: Se houver redirecionamento para login do Google, o script precisaria tratar isso aqui.
        time.sleep(5) # Aguarda a página inicial carregar
        
        # 1. TENTAR CLICAR EM "COPIAR"
        print("Procurando o botão 'Copiar'...")
        try:
            # Tenta primeiro pelo XPath
            btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[1]")))
            btn_copiar.click()
            print("✅ Botão 'Copiar' clicado via XPath.")
        except:
            print("⚠️ XPath do botão 'Copiar' falhou. Tentando localizar pela escrita...")
            # Fallback procurando por um botão que contenha a palavra Copiar
            btn_copiar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Copiar')]")))
            btn_copiar.click()
            print("✅ Botão 'Copiar' clicado via texto.")

        # Aguardar 10 segundos conforme solicitado
        print("Aguardando 10 segundos para a caixa do SeaTalk aparecer...")
        time.sleep(10)

        # 2. TENTAR CLICAR EM "SEATALK"
        print("Procurando o botão 'SeaTalk'...")
        try:
            # Tenta primeiro pelo XPath
            btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/div/div[1]/div[1]/div[5]/div[2]/div[3]/button[2]")))
            btn_seatalk.click()
            print("✅ Botão 'SeaTalk' clicado via XPath.")
        except:
            print("⚠️ XPath do botão 'SeaTalk' falhou. Tentando localizar pela escrita...")
            # Fallback procurando por um botão que contenha a palavra SeaTalk
            btn_seatalk = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SeaTalk')]")))
            btn_seatalk.click()
            print("✅ Botão 'SeaTalk' clicado via texto.")

        # Aguardar 5 segundos para a mensagem ser enviada e para o print
        print("Aguardando 5 segundos para envio da mensagem...")
        time.sleep(5)
        
        # Tirar print de confirmação
        driver.save_screenshot("sucesso_print.png")
        print("📸 Print final salvo com sucesso.")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")
        # Tira um print do erro para ajudar a debugar lá no GitHub
        driver.save_screenshot("erro_print.png")
        sys.exit(1) # Força o erro no GitHub Actions para ele ficar vermelho (failed)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
