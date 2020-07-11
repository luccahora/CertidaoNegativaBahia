from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
global str

options = Options()
options.add_experimental_option("prefs", {
"download.default_directory": r"C:\certidaoNegativaEstadual", #Por o diretorio em que o pdf vai ser baixado.
"download.prompt_for_download": False,
"download.directory_upgrade": True,
"safebrowsing.enabled": True,
"pdfjs.disabled": True,
"plugins.plugins_list": [{"enabled":False,"name":"Chrome PDF Viewer"}],
"plugins.always_open_pdf_externally": True,
})

options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=options)

def ler_csv():
    Resultado = [] 
    with open('empresas.csv','r',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=";",lineterminator="\n")
        for row in reader:
            Resultado.append(row)  
    return Resultado

def login(cnpj_empresa):
    try:
        driver.get("https://sistemas.sefaz.ba.gov.br/sistemas/sigat/Default.Aspx?Modulo=CREDITO&Tela=DocEmissaoCertidaoInternet&limparSessao=1&sts_link_externo=2")
        campo_cnpj = driver.find_element_by_xpath('//*[@id="_ctl0__ctl1_num_cnpj"]')
        campo_cnpj = campo_cnpj.send_keys(cnpj_empresa)
        botao_login = driver.find_element_by_xpath('//*[@id="_ctl0__ctl1_btn_Imprimir"]').click()
    except: 
        login(cnpj_empresa)    

def download_pdf():
    pagina_download = driver.window_handles[1]
    driver.switch_to_window(pagina_download)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="_ctl0__ctl0_crv_relatorio"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[1]/a[2]/img').click()
    driver.find_element_by_name("button").click()

def renomear_pdf(razao_empresa):    
    time.sleep(5)
    nome_antigo = os.path.join(r"C:\certidaoNegativaEstadual", "Untitled.pdf") #Tem que ser o mesmo diretorio da linha 12.
    nome_novo = os.path.join(r"C:\certidaoNegativaEstadual",str(str(razao_empresa)+".pdf")) #Tem que ser o mesmo diretorio da linha 12.
    os.rename(nome_antigo, nome_novo)
    return nome_novo

lista_empresas = ler_csv()

for i in lista_empresas:
    login(i['cnpj'])  
    download_pdf()
    renomear_pdf(i['razao'])
