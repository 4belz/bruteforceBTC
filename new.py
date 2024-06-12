import itertools
import random
import sqlite3
import requests
from mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet, wallet_delete_if_exists

# Función para leer las palabras del archivo
def read_bip39_words(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

# Función para inicializar la base de datos
def init_db(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claves_nemonicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mnemonic TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claves_procesadas (
            id INTEGER PRIMARY KEY,
            mnemonic TEXT,
            address TEXT,
            private_key TEXT,
            balance REAL
        )
    ''')
    conn.commit()
    return conn

# Función para leer las claves probadas anteriormente desde la base de datos
def read_tried_mnemonics(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT mnemonic FROM claves_nemonicas')
    return set(row[0] for row in cursor.fetchall())

# Función para guardar las claves probadas en la base de datos
def save_tried_mnemonic(conn, mnemonic):
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO claves_nemonicas (mnemonic) VALUES (?)', (mnemonic,))
    conn.commit()

# Función para generar claves privadas aleatorias y probarlas
def generate_and_test_random_mnemonic(words_filename, conn):
    # Leemos las palabras del archivo
    words = read_bip39_words(words_filename)
    
    # Leemos las combinaciones probadas anteriormente
    tried_mnemonics = read_tried_mnemonics(conn)
    
    while True:
        # Generamos una combinación aleatoria de 24 palabras
        random.shuffle(words)
        mnemonic = ' '.join(words[:24])
        
        # Verificamos si esta combinación ya ha sido probada
        if mnemonic not in tried_mnemonics:
            tried_mnemonics.add(mnemonic)
            save_tried_mnemonic(conn, mnemonic)
            yield mnemonic

# Función para procesar un grupo de 24 palabras mnemónicas
def procesar_grupo_mnemonico(id, mnemonic_words, conn):
    cursor = conn.cursor()
    try:
        # Crear la semilla desde las palabras mnemónicas
        mnemo = Mnemonic("english")
        seed = mnemo.to_seed(mnemonic_words)

        # Generar la clave privada (usamos la semilla como ejemplo)
        private_key = seed.hex()

        # Nombre de la billetera a crear
        wallet_name = f'wallet_{mnemonic_words[:4]}'  # Generar un nombre único para la billetera

        try:
            # Crear una nueva billetera
            wallet = Wallet.create(wallet_name, keys=seed, network='bitcoin')
            print(f"Billetera '{wallet_name}' creada exitosamente.")

        except Exception as e:
            print(f"Error al crear la billetera '{wallet_name}': {e}")
            return

        # Obtener la dirección de Bitcoin
        address = wallet.get_key().address

        try:
            # Consultar el saldo de la dirección
            response = requests.get(f"https://blockstream.info/api/address/{address}")
            response.raise_for_status()  # Raise an error for bad response status

            # Parsear la respuesta JSON
            data = response.json()

            # Obtener el saldo de la dirección
            balance = data['chain_stats']['funded_txo_sum'] / 100000000  # Convertir de satoshis a BTC

            # Imprimir resultados
            print(f"La dirección {address} tiene un saldo de {balance} BTC.")

            # Insertar resultados en la tabla claves_procesadas
            cursor.execute('''
                INSERT INTO claves_procesadas (id, mnemonic, address, private_key, balance) 
                VALUES (?, ?, ?, ?, ?)
            ''', (id, mnemonic_words, address, private_key, balance))
            conn.commit()

        except requests.exceptions.RequestException as e:
            print(f"Error al consultar el saldo de la dirección {address}: {e}")

        except (KeyError, ValueError) as e:
            print(f"Error al parsear la respuesta JSON: {e}")

        except Exception as e:
            print(f"Error desconocido: {e}")

        finally:
            # Eliminar la billetera después de obtener el saldo
            try:
                wallet_delete_if_exists(wallet_name)
                print(f"Billetera '{wallet_name}' eliminada exitosamente.")
            except Exception as e:
                print(f"Error al eliminar la billetera '{wallet_name}': {e}")

    except ValueError as e:
        print(f"Error al convertir las palabras mnemónicas: {e}")

# Nombre del archivo que contiene las palabras
words_filename = 'bip39words.txt'
# Nombre del archivo de la base de datos SQLite
db_filename = 'prod_loterybtc.db'

# Inicializamos la base de datos
conn = init_db(db_filename)

# Generamos claves privadas aleatorias y las probamos
mnemonic_generator = generate_and_test_random_mnemonic(words_filename, conn)

# Infinitamente probamos grupos de claves privadas aleatorias
while True:
    mnemonic = next(mnemonic_generator)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM claves_nemonicas WHERE mnemonic = ?', (mnemonic,))
    result = cursor.fetchone()
    if result:
        id = result[0]
        procesar_grupo_mnemonico(id, mnemonic, conn)

# Cerramos la conexión a la base de datos
conn.close()
