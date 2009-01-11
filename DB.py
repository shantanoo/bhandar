import sqlite3

class DB:
    def __init__(self,db=None, busy_timeout=600000):
        self.tbl = None
        self.dbh = None
        self.db = db
    def set_db(self, db):
        if db:
            self.db = db
        else:
            return 'EDB'
    def connect(self):
        if not self.db:
            return 'EDB'
        self.dbh = sqlite3.connect(self.db)
    def disconnect(self):
        if self.dbh:
            self.dbh.close()
    def do_query(self, sql):
        if not self.dbh or not sql:
            return 'EDB'
        try:
            self.dbh.execute(sql)
            self.dbh.commit()
        except:
            return 'EDB'
    def select_query(self, sql):
        if not self.dbh or not sql:
            return 'EDB'
        try:
            return self.dbh.execute(sql).fetchall()
        except:
            return 'EDB'
    def insert(self,args):
        if(args['tbl']):
            self.tbl = args['tbl']
        if not self.dbh or not self.tbl or not args['data']:
            return 'EDB'
        sql = 'insert into ' + self.tbl + ' (' + ','.join(args['data'].keys()) + ') values ('
        for x in args['data'].values():
            sql += "'"+ x +"'"
        sql += ')'
        try:
            self.dbh.execute(sql)
            self.dbh.commit()
            return 0
        except:
            return 'EDB'
    def update(self, args):
        if(args['tbl']):
            self.tbl = args['tbl']
        if not self.dbh or not self.tbl or not args['data']:
            return 'EDB'
        sql = 'update ' + self.tbl + ' set '
        x = []
        while 1:
            try:
                y = args['data'].popitem()
                x.append(y[0]+"='"+y[1]+"'")
            except:
                break
        sql += ','.join(x)
        args['condition'] = args['condition'].lstrip().rstrip()
        if args['condition']:
            sql += 'where '+ args['condition']
        print sql
        try:
            self.dbh.execute(sql)
            self.dbh.commit()
            return 0
        except:
            return 'EDB'
