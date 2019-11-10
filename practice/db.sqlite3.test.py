print("Hello World")
import sqlite3

db_path = 'D:\workspace\vmatrix\django111\db.sqlite3'
conn = sqlite3.connect('test.db')
c = conn.cursor()
cursor = c.execute('select * from django_session')

# cursor = c.execute('SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE "auth_user"."username" = "asimo"')

for row in cursor:
    print(row)