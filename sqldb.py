import pymysql

class sqldb:
    
    username = "root"
    password = "123"
    dbname = ""
    table = ""
    cursor = ""
    db = ""
    
    def read_db(self):
        sql = "SELECT * FROM %s" % (self.table)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                name = row[1]
                plateno = row[2]
                mobile = row[3]
                balance = row[4]
            print ("Name : %s\nPlate Number : %s\nMobile : %s\nBalance : %d" % (name, plateno, mobile, 
                                                                                balance))
        except:
            print ("Error: Unable to fetch database")

    def search_db(self, plate_no):
        sql = "SELECT * FROM %s WHERE plateno = '%s'" % (self.table, plate_no)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                name = row[1]
                plate = row[2]
                mobile = row[3]
                balance = row[4]
            print ("Name : %s\nPlate Number : %s\nMobile : %s\nBalance : %d" % (name, plate, mobile, 
                                                                                balance))
        except:
            print ("Error: No such plate found in the database")
    
    def debit(self, plate_no, amount):
        sql = "SELECT * FROM %s WHERE plateno = '%s'" % (self.table, plate_no)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                plate = row[2]
                balance = row[4]
            print ("Plate Number : %s\nOld Balance : %d" % (plate, balance))
            balance -= amount
            if (balance >= 0):
                self.cursor = self.db.cursor()
                sql = "UPDATE %s SET balance = %d WHERE plateno = '%s'" % (self.table, balance, plate_no)
                self.cursor.execute(sql)
                self.db.commit()
                print ("New Balance : %d" % (balance))  
            else:
                print ("Insufficient Balance")
        except:
            self.db.rollback()
            print ("Error: No such plate found in the database") 
            
    def update_mobile(self, plate_no, mobile):
        sql = "UPDATE %s SET mobile = '%s' WHERE plateno = '%s'" % (self.table, mobile, plate_no)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print ("Successfully updated mobile number to %s" % (mobile))
        except:
            self.db.rollback()
            print ("Error: No such plate found in the database") 
        
    def update_balance(self, plate_no, balance):
        sql = "UPDATE %s SET balance = '%d' WHERE plateno = '%s'" % (self.table, balance, plate_no)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print ("Successfully updated account balance to %d" % (balance))
        except:
            self.db.rollback()
            print ("Error: No such plate found in the database") 
            
    def credit(self, plate_no, amount):
        sql = "SELECT * FROM %s WHERE plateno = '%s'" % (self.table, plate_no)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                plate = row[2]
                balance = row[4]
            print ("Plate Number : %s\nOld Balance : %d" % (plate, balance))
            balance += amount
            self.cursor = self.db.cursor()
            sql = "UPDATE %s SET balance = %d WHERE plateno = '%s'" % (self.table, balance, plate_no)
            self.cursor.execute(sql)
            self.db.commit()
            print ("New Balance : %d" % (balance))
        except:
            self.db.rollback()
            print ("Error: No such plate found in the database") 
        
    def get_table_count(self):
        sql = "SELECT COUNT(*) FROM %s" % (self.table)
        self.cursor.execute(sql)
        count = self.cursor.fetchall()    
        print ("Number of rows in table : %d" % count[0])
        
    def __init__(self, dbname, tablename):
        self.dbname = dbname
        self.table = tablename
        self.db = pymysql.connect("localhost", self.username, self.password, self.dbname)        
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print ("Connected to database %s" % self.dbname)
        print ("Database version : %s\n" % data)
