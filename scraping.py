import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

# Lista de User-Agents para rotação
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
]

# Função para gerar um User-Agent aleatório
def get_random_user_agent():
    return random.choice(user_agents)

# Função para configurar o WebDriver com User-Agent aleatório
def create_driver():
    chrome_options = Options()
    user_agent = get_random_user_agent()  # Seleciona aleatoriamente um User-Agent
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scroll_to_top_and_bottom(driver):
    scroll_pause_time = 0.7  # Tempo de pausa entre scrolls

    # Primeiro, rolar até o topo
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(scroll_pause_time)

    # Rolar para o final da página
    current_position = 0
    new_position = None

    while True:
        # Rola para baixo
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(scroll_pause_time)

        # Verifica a posição atual do scroll
        new_position = driver.execute_script("return window.pageYOffset")

        # Se a posição não mudar, significa que chegamos ao final
        if new_position == current_position:
            print("Scroll chegou ao final da página.")
            break

        current_position = new_position


# Função para processar a página e extrair os dados
def process_page(driver, categoria):

    # Extrair o HTML da página carregada
    html = driver.page_source

    # Usar BeautifulSoup para processar o HTML extraído
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
            'timestamp': timestamp
        }
        data_list.append(data)

# Função para navegar pelas páginas
def navigate_pages(driver):
    # Verificando a presença do botão "Próxima Página" e clicando nele
    next_button = driver.find_element(By.XPATH, "//*[@id='__next']/main/section/div/form/div[2]/div[4]/div[1]/div/section/nav/button[2]")
    next_button.click()
    print("Cliquei na próxima página!")
    time.sleep(5)  # Esperar o carregamento da próxima página


# Salvar os dados em um arquivo CSV
def exportar_csv():
    csv_file = f"{categoria}.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['titulo', 'valor', 'metragem', 'quartos', 'banheiros', 'vagas', 'endereco', 'link', 'categoria', 'timestamp'])
        writer.writeheader()
        writer.writerows(data_list)

    print(f"Dados salvos no arquivo {csv_file}")


if __name__ == "__main__":
    driver = create_driver()

    data_list = []

    endereco = {'categoria': 'apartamento', 'url': "https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++cacupe/"}
    categoria = endereco['categoria']
    url = endereco['url']

    driver.get(url)

    while True:
        try:
            scroll_to_top_and_bottom(driver)
            process_page(driver, categoria)
            navigate_pages(driver)

        except Exception as e:
            print("Erro ou fim das páginas: ", e)
            break


    driver.quit()

    exportar_csv()

