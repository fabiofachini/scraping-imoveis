from functions import criar_drive, scroll_para_cima_e_para_baixo, scraping, trocar_pagina, exportar_csv, aceitar_cookie, verificar_botao_proxima_pagina
import time
from datetime import datetime

if __name__ == "__main__":
        # Capturar o horário de início
    start_time = datetime.now()
    print(f"Início da execução: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    driver = criar_drive()
    data_list = []

    categoria = 'aluguel'
    tipo = 'apartamento'
    cidade = 'florianopolis'
    caracteristica = 'tudo'
    url = "https://www.zapimoveis.com.br/aluguel/apartamentos/sc+florianopolis/?__ab=exp-aa-test:control,propposv3:control,rentsale:test,pos-zap:new,zapproppos:a&transacao=aluguel&onde=,Santa%20Catarina,Florian%C3%B3polis,,,,,city,BR%3ESanta%20Catarina%3ENULL%3EFlorianopolis,-27.594804,-48.556929,&tipos=apartamento_residencial,studio_residencial,kitnet_residencial,cobertura_residencial,flat_residencial,loft_residencial&pagina=1"
    
    driver.get(url)
    time.sleep(5)
    aceitar_cookie(driver)

    while True:
        try:
            for attempt in range(5):
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
    
    exportar_csv(data_list, categoria, tipo, cidade, caracteristica)

    # Capturar o horário de término
    end_time = datetime.now()
    print(f"Término da execução: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Exibir a duração total
    duration = end_time - start_time
    print(f"Duração total: {duration}")