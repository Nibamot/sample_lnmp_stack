import os
from mysql.connector import connect, Error #mysql-connector-python

try:
    with connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE']
    ) as connection:
        print(connection)
        cursor=connection.cursor(buffered=True)
        db_query="CREATE TABLE if not exists cats (id INT, name VARCHAR(255))"
        cursor.execute(db_query)
        print(cursor.execute("SHOW TABLES from mydb"))
        for table in cursor:
            print(table)
        cursor.execute("show databases")
        fname = cursor.fetchone()[0]
        cursor.execute("select * from cats")
        cursor.execute("insert into cats(id,name) VALUES(12, 'Not so Johnny Bravo')")
        connection.commit()
        cursor.execute("select * from cats")
        for id, name in cursor:
            print("ID:",id, " NAME:",name)
        cursor.fetchone()[0]
        print(cursor.rowcount)
        cursor.close()
        connection.close()
except Error as e:
    print("Error:", e) 