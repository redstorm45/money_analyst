
import PyQt5.QtSql as QtSql


def init_db():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("data.db")

    if not db.open():
        print('no connection :-(')

    query = QtSql.QSqlQuery()

    query.exec("PRAGMA foreign_keys = ON;")

    # --- create the tables ---
    query.exec("CREATE TABLE IF NOT EXISTS categories (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    name CHARACTER(64) NOT NULL,\
                    color CHARACTER(7) NOT NULL,\
                    label INTEGER NOT NULL,\
                    account_id INTEGER,\
                    FOREIGN KEY(account_id) REFERENCES accounts(id),\
                );")
    query.exec("CREATE TABLE IF NOT EXISTS transactions (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    desc CHARACTER(256) NOT NULL,\
                    category_id INTEGER NOT NULL,\
                    amount INTEGER NOT NULL,\
                    date TEXT NOT NULL,\
                    FOREIGN KEY(category_id) REFERENCES categories(id)\
                );")
    query.exec("CREATE TABLE IF NOT EXISTS labels (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    category_id INTEGER NOT NULL,\
                    transaction_id INTEGER NOT NULL,\
                    FOREIGN KEY(category_id) REFERENCES categories(id),\
                    FOREIGN KEY(transaction_id) REFERENCES transactions(id)\
                );")
    query.exec("CREATE TABLE IF NOT EXISTS accounts (\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    name CHARACTER(64) NOT NULL,\
                    bank CHARACTER(64) NOT NULL,\
                    iban CHARACTER(256) NOT NULL,\
                );")
    query.exec("CREATE TABLE IF NOT EXISTS version (value CHARACTER(8));")

    # --- fill / get the version ---
    query.exec("SELECT * FROM version")
    if query.next():
        version = query.value(0)
        versionInt = tuple([int(k) for k in version.split('.')])
    else:
        query.exec("INSERT INTO version (value) VALUES ('0.0.1')")
        versionInt = (0, 0, 1)
    
    # --- do the migrations as needed
    while versionInt != (0, 0, 1):
        if versionInt == (0, 0, 0):
            query.exec("ALTER TABLE categories ADD account_id INTEGER;")
            query.exec("TRUNCATE TABLE version;")
            query.exec("INSERT INTO version (value) VALUES ('0.0.1')")
            versionInt = (0, 0, 1)
    #query.exec("INSERT INTO categories (name, color) VALUES ('Nourriture', '#00cc00');")
    #query.exec("INSERT INTO transactions (desc, category, amount, date) VALUES ('Plein', 1, 3402, '2019-01-02');")
