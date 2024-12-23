from functions import criar_drive, scroll_para_cima_e_para_baixo, scraping, trocar_pagina, exportar_csv, aceitar_cookie
import time

if __name__ == "__main__":
    driver = criar_drive()
    data_list = []

    categoria = 'venda'
    tipo = 'terreno'
    cidade = 'florianopolis'
    url = "https://www.zapimoveis.com.br/venda/terrenos-lotes-condominios/sc+florianopolis/?transacao=venda&onde=,Santa%20Catarina,Florian%C3%B3polis,,,,,city,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis,-27.594804,-48.556929,&tipos=lote-terreno_residencial,granja_residencial&itl_id=1000072&itl_name=zap_-_botao-cta_buscar_to_zap_resultado-pesquisa&origem=busca-recente"
    
    driver.get(url)
    time.sleep(5)
    aceitar_cookie(driver)
    
    while True:
        try:
            scroll_para_cima_e_para_baixo(driver)
            scraping(driver, categoria, tipo, data_list)
            trocar_pagina(driver)

        except Exception as e:
            print("Erro ou fim das páginas: ", e)
            break

    driver.quit()
    
    exportar_csv(data_list, categoria, tipo, cidade)
