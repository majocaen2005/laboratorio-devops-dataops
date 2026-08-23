import pandas as pd
import psycopg2

# =========================
# Lectura del dataset
# =========================
df = pd.read_csv("data/dataset.csv")
print("Dataset original")
print(df)

# =========================
# Limpieza de datos
# =========================
# Eliminación de duplicados
df = df.drop_duplicates()
# Reemplazo de valores nulos
df = df.fillna(0)
print("\nDataset limpio")
print(df)

# =========================
# Exportación de dataset limpio
# =========================
df.to_csv("output/dataset_limpio.csv", index=False)
print("\nArchivo exportado correctamente")

# =========================
# Conexión PostgreSQL
# =========================
conn = psycopg2.connect(
    host="localhost",
    port="5433",      # <--- Esta línea es la clave
    database="laboratorio",
    user="admin",
    password="admin123"
)
cursor = conn.cursor()
print("\nConexión PostgreSQL exitosa")


# =========================
# Creación de tabla
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INT,
    nombre VARCHAR(50),
    edad INT,
    ciudad VARCHAR(50)
)
""")
conn.commit()
print("Tabla creada correctamente")

# =========================
# Inserción de registros
# =========================
cursor.execute("DELETE FROM clientes")
conn.commit()

for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO clientes (id, nombre, edad, ciudad) VALUES (%s, %s, %s, %s)",
        (
            int(row['id']),
            row['nombre'],
            int(float(row['edad'])),
            row['ciudad']
        )
    )
conn.commit()
print("Datos insertados correctamente")

# =========================
# Validación final
# =========================
cursor.execute("SELECT * FROM clientes")
resultado = cursor.fetchall()
print(f"\nTotal registros: {len(resultado)}")
print("Datos almacenados en PostgreSQL:")
for fila in resultado:
    print(fila)

# =========================
# Cierre de conexión
# =========================
cursor.close()
conn.close()
print("\nProceso finalizado correctamente")