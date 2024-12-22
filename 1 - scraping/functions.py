import random
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import os

def escolher_agente_aleatoriamente():
    # Lista de User-Agents para rotação
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

def criar_drive():
    chrome_options = Options()
    user_agent = escolher_agente_aleatoriamente()
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scroll_para_cima_e_para_baixo(driver):
    scroll_tempo_pausa = 0.7

    # Rolar até o topo
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(scroll_tempo_pausa)

    # Rolar até o final
    posicao_atual = 0
    posicao_nova = None
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(scroll_tempo_pausa)
        posicao_nova = driver.execute_script("return window.pageYOffset")
        if posicao_nova == posicao_atual:
            print("Scroll chegou ao final da página.")
            break
        posicao_atual = posicao_nova

def scraping(driver, categoria, tipo, data_list):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    imoveis = soup.select('div.ListingCard_result-card__Pumtx')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for imovel in imoveis:
        valor = imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-heading-small.l-text--weight-bold.undefined')
        if not valor:
            valor = imovel.select_one('p.l-text.l-u-color-feedback-success-110.l-text--variant-heading-small.l-text--weight-bold.undefined')

        data = {
            'titulo': imovel.select_one('h2.l-text.l-u-color-neutral-28.l-text--variant-heading-small.l-text--weight-medium.truncate').get_text(strip=True) if imovel.select_one('h2.l-text.l-u-color-neutral-28.l-text--variant-heading-small.l-text--weight-medium.truncate') else None,
            'valor': valor.get_text(strip=True) if valor else None,
            'metragem': imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[itemprop="floorSize"]').get_text(strip=True) if imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[itemprop="floorSize"]') else None,
            'quartos': imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[itemprop="numberOfRooms"]').get_text(strip=True) if imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[itemprop="numberOfRooms"]') else None,
            'banheiros': imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[itemprop="numberOfBathroomsTotal"]').get_text(strip=True) if imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[itemprop="numberOfBathroomsTotal"]') else None,
            'vagas': imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]').get_text(strip=True) if imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.undefined[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]') else None,
            'endereco': imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.truncate[data-cy="rp-cardProperty-street-txt"]').get_text(strip=True) if imovel.select_one('p.l-text.l-u-color-neutral-28.l-text--variant-body-small.l-text--weight-regular.truncate[data-cy="rp-cardProperty-street-txt"]') else None,
            'link': imovel.select_one('a.ListingCard_result-card__Pumtx')['href'] if imovel.select_one('a.ListingCard_result-card__Pumtx') else None,
            'categoria': categoria,
            'tipo': tipo,
            'timestamp': timestamp
        }
        data_list.append(data)
    print("Dados dos imóveis capturados")

def trocar_pagina(driver):
    botao_proxima = driver.find_element(By.XPATH, "//*[@id='__next']/main/section/div/form/div[2]/div[4]/div[1]/div/section/nav/button[2]")
    botao_proxima.click()
    print("Cliquei na próxima página!")
    time.sleep(5)

def exportar_csv(data_list, categoria, tipo, cidade):
    pasta = "2 - csv"
    
    csv_file = os.path.join(pasta, f"{categoria}_{tipo}_{cidade}.csv")
    
    # Criação do arquivo CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['titulo', 'valor', 'metragem', 'quartos', 'banheiros', 'vagas', 'endereco', 'link', 'categoria','tipo', 'timestamp'])
        writer.writeheader()
        writer.writerows(data_list)
    
    print(f"Dados salvos no arquivo {csv_file}")

def aceitar_cookie(driver):
    """
    Função para clicar no botão de aceitar cookies.
    :param driver: Instância do Selenium WebDriver
    """
    try:
        botao_aceitar = driver.find_element(By.XPATH, "//*[@id='adopt-accept-all-button']")
        botao_aceitar.click()
        print("Cliquei no botão de aceitar cookies!")
        time.sleep(5)
    except Exception as e:
        print(f"Erro ao clicar no botão de aceitar cookies: {e}")