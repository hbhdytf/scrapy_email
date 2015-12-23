__author__ = 'yangtengfei'
import glob
import sqlite3

dbconn=sqlite3.connect(r'../merge.sqlite')

count=0

for filename in glob.glob(r'*.sqlite'):
    print filename
    conn=sqlite3.connect(filename)
    cur=conn.execute('select * from ustc')
    sum=0
    for re in cur.fetchall():
        if "username=" in re[0]:
            temp=re[0].split("username=")[1]
            re=(temp,re[1],re[2])
            print re
        if re[0][:2]=='20':
            temp=re[0].split("20")[1]
            re=(temp,re[1],re[2])
            print re
        try:
            dbconn.execute('insert into ustc values(?,?,?)',re)
            sum+=1
        except:
            pass
    print 'db %s : %d' % (filename,sum)
    count+=sum
    dbconn.commit()
dbconn.close()
print count