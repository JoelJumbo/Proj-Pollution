import mysql.connector
import json

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'projectwork5'

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}

def create_db_connection():
    return mysql.connector.connect(**db_config)


def execute_fetchall(query, params=None, dict=False):
    connection = create_db_connection()

    if dict:
        cursor = connection.cursor(dictionary=True)
    else:
        cursor = connection.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result

def dataa(id_stazione, tipologia):
    #'Biossido di Azoto'
    #'Biossido di Zolfo'
    #'Ozono'
    #'Monossido di Carbonio'
    #'PM10 (SM2005)'
    #'Particelle sospese PM2.5'

    query = """
    SELECT data_rilevazione.data_24
    FROM rilevazione
    JOIN data_rilevazione ON rilevazione.id_data_rilevazione = data_rilevazione.id_data_rilevazione
    JOIN sensore ON rilevazione.id_sensore = sensore.id_sensore
    JOIN tipologia ON sensore.id_tipologia = tipologia.id_tipologia
    WHERE sensore.id_stazione = %s AND tipologia.nome = %s;
    """

    data = execute_fetchall(query, (id_stazione, tipologia,), dict=False)
    lista_data = []
    for elem in data:
        lista_data.append(str(elem[0]))

    return lista_data
def valore(id_stazione, tipologia):

    query = """
    SELECT rilevazione.valore
    FROM rilevazione
    JOIN data_rilevazione ON rilevazione.id_data_rilevazione = data_rilevazione.id_data_rilevazione
    JOIN sensore ON rilevazione.id_sensore = sensore.id_sensore
    JOIN tipologia ON sensore.id_tipologia = tipologia.id_tipologia
    WHERE sensore.id_stazione = %s AND tipologia.nome = %s;
    """

    valore = execute_fetchall(query, (id_stazione, tipologia,), dict=False)

    lista_valori = []
    for elem in valore:
        lista_valori.append(elem[0])

    return lista_valori

def crea_json(id_stazione):
# id_stazione = 517


    sostanze = ['Particelle sospese PM2.5', 'PM10 (SM2005)', 'Biossido di Azoto', 'Monossido di Carbonio' ]
    diz_finale = {elem : [dataa(id_stazione, elem), valore(id_stazione, elem)] for elem in sostanze if dataa(id_stazione, elem) != [] }
    print (diz_finale)


    # for elem in sostanze:
    #     lista_dato = [data(id_stazione, elem), valore(id_stazione, elem)]
    #     lista_finale.append(lista_dato)

    #print(diz_finale)

    print(diz_finale.keys())
    lista_chiavi = list(diz_finale.keys())
    print(lista_chiavi)

    # Read JSON data from a file
    with open('plot_definitivo_spero_madavvero.json', 'r') as file:
        data = json.load(file)

        #print(data)

    # Modify the JSON


    if 'Particelle sospese PM2.5' in lista_chiavi:
        data['data'][0]['x'] = diz_finale['Particelle sospese PM2.5'][0]
        data['data'][0]['y'] = diz_finale['Particelle sospese PM2.5'][1]
        data['data'][0]['marker']['color'] = diz_finale['Particelle sospese PM2.5'][1]
    else:
        data['data'][0]['x'] = []
        data['data'][0]['y'] = []

    if 'PM10 (SM2005)' in lista_chiavi:
        data['data'][1]['x'] = diz_finale['PM10 (SM2005)'][0]
        data['data'][1]['y'] = diz_finale['PM10 (SM2005)'][1]
        data['data'][1]['marker']['color'] = diz_finale['PM10 (SM2005)'][1]
    else:
        data['data'][1]['x'] = []
        data['data'][1]['y'] = []

    if 'Biossido di Azoto' in lista_chiavi:
        data['data'][2]['x'] = diz_finale['Biossido di Azoto'][0]
        data['data'][2]['y'] = diz_finale['Biossido di Azoto'][1]
        data['data'][2]['marker']['color'] = diz_finale['Biossido di Azoto'][1]
    else:
        data['data'][2]['x'] = []
        data['data'][2]['y'] = []

    if 'Monossido di Carbonio' in lista_chiavi:
        data['data'][3]['x'] = diz_finale['Monossido di Carbonio'][0]
        data['data'][3]['y'] = diz_finale['Monossido di Carbonio'][1]
        data['data'][3]['marker']['color'] = diz_finale['Monossido di Carbonio'][1]
    else:
        data['data'][3]['x'] = []
        data['data'][3]['y'] = []



    print(data)
    # Write the modified JSON data back to the file
    with open('json_grafici/plot_dati.json', 'w') as output:
        json.dump(data, output, indent=4)
#
# crea_json(517)




