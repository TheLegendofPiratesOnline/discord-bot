"""
A classe BotLocalizerPortuguese é utilizada para fornecer respostas
em canais Discord onde se fala português.

Todas as strings nesta classe estarão apenas em português(Portugal).
"""

APP_DESCRIPTION = "Bot Discord criado pela TLOPO. <3 \n https://github.com/TheLegendofPiratesOnline/discord-bot"

OUT_OF_DATE = "Este bot está desatualizado. Por favor, visita https://github.com/TheLegendofPiratesOnline/discord-bot para atualizá-lo."

FLEET_ITEM_INFO = '''- Tipo: %s
- Estado: %s
- Navios Restantes: %s
'''

INVASION_ITEM_INFO = '''- Estado: %s
- Fase: %s
- Número de Jogadores: %s
'''

SYSTEM_STATUS_INFO = '''%s
Falhas Reportadas: %s
'''

OVER_ALL_STATUS = '''Estado Geral: **%s**
'''

EMBED_TITLES = [
    'Comandos',  # 0
    'Sobre',  # 1
    'Populações dos Oceanos',  # 2
    'Frotas Ativas',  # 3
    'Sem frotas ativas',  # 4
    'Invasões Ativas',  # 5
    'Sem invasões ativas',  # 6
    'Avisos do Servidor',  # 7
    'Estado do Servidor',  # 8
    'Estado do Servidor Indisponível',  # 9
    'Avisos do Servidor Indisponíveis',  # 10
    'The Legend of Pirates Online está atualmente fechado para uma atualização'  # 11
]

FIELD_NAMES = [
    'Autores',  # 0
    'Total',  # 1
    'Servidores Web',  # 2
    'Agentes Cliente',  # 3
    'Oceanos',  # 4
    'Funções do Servidor de Jogo'  # 5
]

STATUS_MESSAGES = [
    'Sem descrição disponível',  # 0
    'Nenhum autor encontrado.',  # 1
    'Nenhuma frota ativa',  # 2
    'Nenhuma invasão ativa',  # 3
    'Sem avisos conhecidos.',  # 4
    'Dados da população oceânica indisponíveis',  # 5
    'Dados de frota indisponíveis',  # 6
    'Dados de invasão indisponíveis',  # 7
    'Visita https://tlopo.com/ para mais informações.',  # 8
    'O estado de prod-gs-1.tlopo.com está a ser detetado incorretamente.\nEste é um problema com a API da TLOPO.',  # 9
    'Desconhecido',  # 10
    'Sem dados disponíveis',  # 11
    'Adiciona-me ao teu servidor!'  # 12
]

MISC = [
    'Mensagem',  # 0
]

STATUS_ALIVE_SRV = 1         
STATUS_MESSAGE_SRV = 2       
STATUS_UPDATE_SRV = 4        
STATUS_ERROR_SRV = 8         
STATUS_FATAL_SRV = 16        
STATUS_UNKNOWN_SRV = 32      

SRV_CODE_TO_STATUS = {
    STATUS_ALIVE_SRV:   "VIVO",
    STATUS_MESSAGE_SRV: "MENSAGEM",
    STATUS_UPDATE_SRV:  "ATUALIZAÇÃO",
    STATUS_ERROR_SRV:   "ERRO",
    STATUS_FATAL_SRV:   "FATAL",
    STATUS_UNKNOWN_SRV: "DESCONHECIDO"
}

# Códigos de estado globais
STATUS_ALIVE_GLOB = 1        
STATUS_MESSAGE_GLOB = 2      
STATUS_UPDATE_GLOB = 3       
STATUS_ERROR_GLOB = 4        
STATUS_FATAL_GLOB = 5        
STATUS_UNKNOWN_GLOB = 6      

GLOB_CODE_TO_STATUS = {
    STATUS_ALIVE_GLOB:   "VIVO",
    STATUS_MESSAGE_GLOB: "MENSAGEM",
    STATUS_UPDATE_GLOB:  "ATUALIZAÇÃO",
    STATUS_ERROR_GLOB:   "ERRO",
    STATUS_FATAL_GLOB:   "FATAL",
    STATUS_UNKNOWN_GLOB: "DESCONHECIDO"
}