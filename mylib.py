import pymysql
def create_connection():
    con=pymysql.connect(host="localhost",db="saqib",passwd="",user="root",autocommit=True,port=3306)
    cur=con.cursor()
    return cur

def check_photo(email):
    conn=pymysql.Connect(host="localhost",db="saqib",autocommit=True,port=3306,user="root",passwd="")
    cur=conn.cursor()
    cur.execute("select * from photodata where email='"+email+"'")
    n=cur.rowcount
    photo="no"
    if(n>0):
        row=cur.fetchone()
        photo=row[1]
    return photo
