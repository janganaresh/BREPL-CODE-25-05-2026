import pandas as pd
import mysql.connector
from mysql.connector import pooling

# ✅ CONNECTION POOL
db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host="localhost",
    user="root",
    password="nare@2058",
    database="remedydb",
    autocommit=True,
    connection_timeout=60
)

def get_db_connection():
    return db_pool.get_connection()


def update_db_from_excel():

    file_path = r"C:\Users\LENOVO\Desktop\area1_1160.xlsx"

    try:
        df = pd.read_excel(file_path)

        # ✅ REMOVE ROWS WITH EMPTY VALUES
        df = df.dropna(subset=['Area ID', 'Table ID', 'Pile No', 'Assessment Case'])

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE assessment
            SET `Assessment case` = %s
            WHERE `Area ID` = %s
              AND `Table ID` = %s
              AND `Pile No` = %s
        """

        data = []

        for _, row in df.iterrows():
            try:
                data.append((
                    str(row['Assessment Case']).strip(),
                    str(row['Area ID']).strip(),
                    str(row['Table ID']).strip(),
                    int(row['Pile No'])
                ))
            except Exception:
                # skip bad rows
                continue

        cursor.executemany(query, data)

        cursor.close()
        conn.close()

        print(f"✅ Database updated successfully ({len(data)} rows processed)")

    except Exception as e:
        print("❌ Error:", e)


if __name__ == '__main__':
    update_db_from_excel()