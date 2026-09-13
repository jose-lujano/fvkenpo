import MySQLdb

connection = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='17015958',
)
try:
    with connection.cursor() as cursor:
        cursor.execute(
            'CREATE DATABASE IF NOT EXISTS fvk_db '
            'CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
        )
    connection.commit()
    print('Base fvk_db creada o ya existente.')
finally:
    connection.close()
