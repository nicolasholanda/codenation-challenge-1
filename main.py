from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


def calculate_price(start_date, end_date):
    # Função responsável por calcular o preço de uma ligação
    # que começa em start_date e finaliza em end_date

    fee = 0.09
    price = 0.36
    daytime = {
        'start': start_date.replace(hour=6, minute=0, second=0, microsecond=0),
        'end': start_date.replace(hour=22, minute=0, second=0, microsecond=0)
    }

    # Se a ligação começou antes do período diurno, o tempo que será cobrado é dado
    # pela diferença positiva entre o fim da ligação o início do período diurno
    if start_date.hour < daytime['start'].hour:
        time_elapsed = (end_date - daytime['start']).total_seconds() // 60
        if time_elapsed > 0:
            price += time_elapsed * fee

    # Se a ligação terminou no período noturno, o tempo que será cobrado é dado
    # pela diferença positiva entre o início do período diurno e o fim da ligação
    elif end_date.hour > daytime['end'].hour:
        time_elapsed = (daytime['end'] - start_date).total_seconds() // 60
        if time_elapsed > 0:
            price += time_elapsed * fee

    # Se a ligação começou e terminou no período diurno, o tempo que será cobrado é dado
    # pela diferença positiva entre o início e o fim da ligação
    else:
        time_elapsed = end_date - start_date
        price += (time_elapsed.total_seconds() // 60) * fee

    return price


def get_source_numbers(record_list):
    # Função responsável por criar uma lista com os números de origem das
    # ligações, sem repetições.

    source_number_set = set()
    for record in record_list:
        source_number_set.add(record['source'])
    return source_number_set


def record_list_to_billing_list(record_list):
    # Função responsável por transformar a lista de registros em
    # uma lista de faturamento, com a chave 'total' zerada.

    initial_billing_list = []
    source_number_set = get_source_numbers(record_list)
    for i in source_number_set:
        billing = {
            'source': i,
            'total': 0.0
        }
        initial_billing_list.append(billing)
    return initial_billing_list


def classify_by_phone_number(record_list):
    billing_list = record_list_to_billing_list(record_list)

    for record in record_list:
        start_date = datetime.fromtimestamp(record['start'])
        end_date = datetime.fromtimestamp(record['end'])

        billing = next(item for item in billing_list if item['source'] == record['source'])
        billing['total'] = round(billing['total'] + calculate_price(start_date, end_date), 2)

    return sorted(billing_list, key=lambda b: b['total'], reverse=True)


print(classify_by_phone_number(records))