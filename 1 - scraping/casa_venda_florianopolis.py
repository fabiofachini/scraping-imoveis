from functions import criar_drive, scroll_para_cima_e_para_baixo, scraping, trocar_pagina, exportar_csv, aceitar_cookie, verificar_botao_proxima_pagina
import time

if __name__ == "__main__":
    driver = criar_drive()
    data_list = []

    categoria = 'venda'
    tipo = 'casa'
    cidade = 'florianopolis'
    url = "https://www.zapimoveis.com.br/venda/casas/sc+florianopolis/?transacao=venda&onde=,Santa%20Catarina,Florian%C3%B3polis,,,,,city,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis,-27.594804,-48.556929,&tipos=casa_residencial,sobrado_residencial,condominio_residencial,casa-vila_residencial&itl_id=1000072&itl_name=zap_-_botao-cta_buscar_to_zap_resultado-pesquisa&origem=busca-recente"
    
    driver.get(url)
    time.sleep(5)
    aceitar_cookie(driver)
    
    while True:
        try:
            # Realiza até 3 tentativas de scroll
            for attempt in range(3):
                scroll_para_cima_e_para_baixo(driver)
                
                if verificar_botao_proxima_pagina(driver):
                    break  # Sai do loop se o botão for encontrado
                
                if attempt < 2:
                    print(f"Tentativa {attempt + 1} de encontrar o botão de próxima página falhou. Tentando novamente...")
                else:
                    print("Todas as tentativas de scroll falharam. Prosseguindo para scraping...")
            
            # Realiza o scraping dos dados
            scraping(driver, categoria, tipo, data_list)
            
            # Troca para a próxima página
            trocar_pagina(driver)

        except Exception as e:
            print("Erro ou fim das páginas: ", e)
            break

    driver.quit()
    
    exportar_csv(data_list, categoria, tipo, cidade)