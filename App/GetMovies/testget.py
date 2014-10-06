import sqlite3

def main():
    nowplaying_con=sqlite3.connect('nowplaying.db')
    nowplaying_cursor=nowplaying_con.cursor()
    query1='SELECT \
            moviename,\
            thumbnail,\
            prediction\
            FROM nowplaying\
            ORDER BY prediction DESC\
            LIMIT 10 '
    nowplaying_cursor.execute(query1)
    moviedata=nowplaying_cursor.fetchall()
    
    for data in moviedata:
        print data

if __name__=="__main__":
    main()