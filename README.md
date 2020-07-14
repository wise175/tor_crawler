# Tor Crawler
<pre>
**Tor Crawler developed by William Solis Guerrero**
</pre>
## Propósito

Este software es una araña web o también conocido como web crawler, para acceder, navegar e indexar el contenido 
alojado en la red Tor, y que a través de técnicas de web scraping y NLP identifica de manera automátizada los servicios
 ONION relacionados a delitos informáticos. Los sitios descubiertos y categorizados son almacenados en una base de datos
 , esto incluye el fuente de la pagina por lo que se exceptua contenidos multimedia.
La informacion relacionada a delitos informaticos pretende ser de alta relevancia para los organismos o entes de control
 en ayuda a descubrir actividades, hábitos o comportamientos objetos de análisis y estudio criminalístico que den o 
 puedan dar como resultado la mitigación de estos actos delictivos.
 
### Flujo de Trabajo
 
#### Crawling
 
    1) Almacenamiento de enlaces semilla a la cola de crawling.
    2) Obtener siguiente sitio en cola de crawling.
    3) Verificación de estado del sitio. En caso de que el dominio padre ya haya sido revisado y no estaba en línea se evita realizar el mismo proceso para enlaces con subdominios de aquel.
    4) Descubrimiento de nuevos enlaces.
    5) Extracción del código fuente del sitio.
    6) Almacenar datos del sitio objeto de crawling y scraping.
    7) Almacenar nuevos enlaces encontrados a la cola de crawling. No se almacenaran enlaces que ya existen en la cola.
    8) Volver a ejecutar desde el paso 2.

#### Categorización de contenido

    1) Obtener siguiente enlace y contenido almacenado para análisis.
    2) Pre-procesamiento y preparación de contenido.
    3) Obtener posible tema del sitio, términos claves relacionados al contenido.
    4) Categorización del sitio mediante comparación con diccionario de delitos.
    5) Almacenar sitio analizado, sus resultados y relación ilegal de ser el caso.
    6) Volver a ejecutar el paso 1.

## Instrucciones
 
### Dependencias en S.O.

- Tor
- Python 3.x
- Postgres 10

### Dependencias Python

- nltk
- gensim
- bs4
- beautifulsoup4
- polyglot
- validators
- urllib3
- psycopg2
- stem

### Configuración Inicial

Es necesario tener instalado y configurado el puerto de control en Tor, esto se lo puede realizar a traves del scritp 
tor_install_config.sh 

`chmod -x tor_install_config.sh`

`bash tor_install_config -p 9051 -w your_password`

<pre>
usage: tor_install_config.sh [-p] [-w]

required arguments:
  -p, --port-control    Asigna el puerto de control para Tor, por defecto es 9051.
  -w, --password        Es el password para evitar accesos de terceros no autorizados. 
</pre>

Crear el esquema inicial de la base de datos, ejecutar:

`psql -U user_db -h host_db -f schema_db.sql`

Instalar dependencias de python, ejecutar:

`pip install -r requirements.txt`

### Puesta en Marcha

#### Crawler

Para ejecutar el crawler es necesario haber ingresado en el archivo `OnionLinkSeed.txt` los enlaces semilla y en 
`config.properties` los parametros de acceso a la base de datos. Posterior sera necesario ejecutar el siguiente comando:

`python main.py -s OnionLinksSeed.txt -c config.properties`

<pre>
usage: main.py [-c] [-s]

required arguments:
  -c, --config-file     Archivo de configuracion de acceso a la base de datos.
  -s, --seed            Archivo que contiene los enlaces semilla. 
</pre>

#### Categorización de sitios

Para ejecutar la categorización de sitios descubiertos es necesario haber ingresado en el archivo `crime_keywords.json` 
los terminos claves de cada crimen a identificar. Posterior sera necesario ejecutar el siguiente comando:

`python main_nlp.py -c config.properties -k crime_keywords.json`

<pre>
usage: main_nlp.py [-c] [-k]

required arguments:
  -c, --config-file     Archivo de configuracion de acceso a la base de datos.
  -k, --keywords-file   Archivo que contiene terminos clave para criterios de categorización. 
</pre>