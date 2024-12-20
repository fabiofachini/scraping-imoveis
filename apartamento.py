from functions import criar_drive, scroll_para_cima_e_para_baixo, scraping, trocar_pagina, exportar_csv

if __name__ == "__main__":
    driver = criar_drive()
    data_list = []

    categoria = 'apartamento'
    url = "https://www.zapimoveis.com.br/venda/apartamentos/sc+florianopolis++cacupe/"
    
    driver.get(url)

    while True:
        try:
            scroll_para_cima_e_para_baixo(driver)
            scraping(driver, categoria, data_list)
            trocar_pagina(driver)

        except Exception as e:
            print("Erro ou fim das páginas: ", e)
            break

    driver.quit()
    exportar_csv(data_list, categoria)
