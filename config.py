
#то что ниже обязательно заполнить своими данными
proxy_use = 0 #  0 - не использовать, 1 - прокси без ссылки , 2 - прокси со ссылкой для смены ip
proxy_login = 'pfd56464'
proxy_password = '9caa07'
proxy_address = 'noroxy.com'
proxy_port = '107'
proxy_changeIPlink = "httpcce3b204"


#то что ниже желательно настроить под себя
minimal_need_balance = 0.0001 # минимальный баланс на кошельке который должен быть чтобы начать  с ним работу


#укажите паузу в работе между кошельками, минимальную и максимальную. 
#При смене каждого кошелька будет выбрано случайное число. Значения указываются в секундах
timeoutMin = 120 #минимальная 
timeoutMax = 300 #максимальная
#задержки между операциями в рамках одного кошелька
timeoutTehMin = 10 #минимальная 
timeoutTehMax = 20 #максимальная

max_gas_price = 20 #максимальная цена газа в сети эфир при которой выполняются транзакции . если будет больше то скрипт будет ждать когда цена снизится


#то что ниже можно менять только если понимаешь что делаешь
proxies = { 'all': f'http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}',}
if proxy_use:
    request_kwargs = {"proxies":proxies, "timeout": 1200}
else:
    request_kwargs = {"timeout": 120}

slippage = 1    # % 
gas_kef=1.1 #коэфициент допустимого расхода газа на подписание транзакций. можно выставлять от 1.1 до 2

rpc_links = {
    'ETH': 'https://rpc.ankr.com/eth',
    'scroll': 'https://rpc.ankr.com/scroll',
}