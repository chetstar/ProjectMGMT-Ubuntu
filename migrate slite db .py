# how to migrate sqlite

# change to appold.db

# sqlite3 {app.db}
# ALTER TABLE app.db ADD COLUMN COLNew {type};
# attach database 'appold.db' as db2
# "INSERT INTO db2.{tablename} SELECT * FROM main.{table name};"