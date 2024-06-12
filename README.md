# 🔓 BruteforceBTC

¡Bienvenido a BruteforceBTC! Este proyecto está diseñado para generar y probar mnemónicos BIP-39 aleatorios y verificar si tienen algún saldo en Bitcoin. ⚡

## 🚀 Descripción del Proyecto

Este script Python realiza las siguientes tareas:

1. **Lee palabras BIP-39 desde un archivo. 📚**
2. **Inicializa una base de datos SQLite para almacenar las combinaciones de mnemónicos probadas y los resultados obtenidos. 📊**
3. **Genera mnemónicos BIP-39 aleatorios y únicos utilizando las palabras leídas. 🎲**
4. **Procesa cada mnemónico generando la correspondiente dirección de Bitcoin y consultando su saldo. 💸**
5. **Almacena los resultados en la base de datos y elimina la billetera temporalmente creada. 🗃️**

## 🛠️ Instalación y Uso

### Prerrequisitos

- Python 3.x
- Dependencias listadas en `requirements.txt` (puedes instalarlas usando `pip install -r requirements.txt`)

### Pasos para Ejecutar el Script

1. **Clonar el repositorio**:
  
   git clone https://github.com/4belz/bruteforceBTC.git
   cd bruteforceBTC
Instalar las dependencias:

pip install -r requirements.txt
Crear el archivo bip39words.txt con las palabras BIP-39 (puedes encontrar una lista en BIP-39 Engli):

plaintext

abandon
ability
able
...
Ejecutar el script:

python bruteforce_btc.py

📂 Estructura del Código
Lectura de palabras BIP-39: Lee las palabras del archivo bip39words.txt.
Inicialización de la base de datos: Crea una base de datos SQLite y las tablas necesarias para almacenar mnemónicos y resultados.
Generación de mnemónicos aleatorios: Genera combinaciones únicas de 24 palabras BIP-39.
Procesamiento de mnemónicos:
Genera una clave privada y una dirección de Bitcoin.
Consulta el saldo de la dirección utilizando una API pública.
Guarda los resultados en la base de datos.
Elimina la billetera temporal.

📝 Detalles del Código
Función read_bip39_words(filename)
Lee y devuelve las palabras BIP-39 desde un archivo de texto.

Función init_db(db_filename)
Inicializa una base de datos SQLite con dos tablas:

claves_nemonicas: para almacenar mnemónicos probados.
claves_procesadas: para almacenar mnemónicos, direcciones, claves privadas y saldos.
Función read_tried_mnemonics(conn)
Lee y devuelve un conjunto de mnemónicos que ya han sido probados.

Función save_tried_mnemonic(conn, mnemonic)
Guarda un mnemónico en la base de datos para evitar que sea probado nuevamente.

Función generate_and_test_random_mnemonic(words_filename, conn)
Genera y retorna mnemónicos aleatorios únicos de 24 palabras.

Función procesar_grupo_mnemonico(id, mnemonic_words, conn)
Procesa un mnemónico:

Genera una clave privada.
Crea una billetera Bitcoin.
Obtiene y guarda la dirección de Bitcoin y su saldo.
Elimina la billetera temporalmente creada.
Ejecución del Script
El script:

Inicializa la base de datos.
Genera mnemónicos aleatorios y los procesa indefinidamente.
Almacena los resultados en la base de datos y elimina las billeteras temporales.
🚧 Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir mejoras o solucionar problemas.

📜 Licencia
Este proyecto está licenciado bajo la MIT License.

¡Gracias por usar BruteforceBTC! 🚀🔓
