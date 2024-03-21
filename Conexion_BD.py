import psycopg2
import os
import traceback
import logging
import csv

logging.basicConfig(level=logging.INFO)

postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_database = os.environ.get('POSTGRES_DATABASE', 'postgres')
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'password')
postgres_port = os.environ.get('POSTGRES_PORT', '5432')

conn_string = f"host={postgres_host} dbname={postgres_database} user={postgres_user} password={postgres_password} port={postgres_port}"

def create_postgres_table(cur):
    try:
        cur.execute("""
                    CREATE TABLE infarto(
            gender              VARCHAR(6) NOT NULL 
            ,age                 NUMERIC(4,2) NOT NULL
            ,hypertension        BIT  NOT NULL
            ,Heart_disease     BIT  NOT NULL
            ,Ever_married      VARCHAR(3) NOT NULL
            ,Work_type        VARCHAR(13) NOT NULL
            ,Residence_type    VARCHAR(5) NOT NULL
            ,Avg_glucose_level NUMERIC(6,2) NOT NULL
            ,bmi                 VARCHAR(4) NOT NULL
            ,Smoking_status    VARCHAR(8) NOT NULL
            ,stroke              VARCHAR(6) NOT NULL
            )
        """)
        conn.commit()
        logging.info('Tabla creada correctamente en la base de datos.')
    except Exception as e:
        logging.error(f'Error al crear la tabla: {e}')

def cargar_datos_desde_csv(ruta_csv, conn):
    try:
        # Abrir el archivo CSV
        with open(ruta_csv, 'r', newline='') as file:
            reader = csv.DictReader(file)
            cursor = conn.cursor()

            for row in reader:
                query = """
                    INSERT INTO infarto (gender,age,hypertension,Heart_disease, Ever_married, Work_type, Residence_type, Avg_glucose_level, bmi, Smoking_status, stroke )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (row['gender'], row['age'], row['hypertension'], row['Heart_disease'],
                                       row['Ever_married'], row['Work_type'], row['Residence_type'],
                                       row['Avg_glucose_level'], row['bmi'], row['Smoking_status'],
                                       row['stroke']))
            conn.commit()
            logging.info("Datos cargados exitosamente desde el archivo CSV.")
    except Exception as e:
        logging.error(f'Error al cargar los datos desde el archivo CSV: {e}')

if __name__ == '__main__':
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        logging.info("Conexión exitosa a la base de datos PostgreSQL.")
        create_postgres_table(cur)
        cargar_datos_desde_csv('/home/roo/Documentos/dataproyect/Predicción de infartos/healthcare-dataset-stroke-data.csv', conn)
    except Exception as e:
        traceback.print_exc()
        logging.error("No se pudo establecer la conexión o cargar los datos desde el archivo CSV.")
    finally:
        if conn:
            conn.close()
            logging.info("Conexión cerrada.")
