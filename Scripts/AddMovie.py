import psycopg2
from psycopg2 import sql
import re
from sshtunnel import SSHTunnelForwarder
# Example credientials file, named .credentials
# <username>
# <password>

# open credential file and read credentials
f = open('Scripts/.credentials', "r")

username = f.readline().replace("\n", "")
password = f.readline()

try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': 'p320_35',
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")
        with open("Scripts/MovieMockData.csv", "r") as dataFile:
            next(dataFile)
            for line in dataFile:
                line = line.strip()
                splitLine = re.findall(r'(".*?"|[^,]+)', line)
                # print(splitLine) # for testing
                movie_id = splitLine[0]
                title = splitLine[1]
                length = splitLine[2]
                release_date = splitLine[3]
                mpaa_rating = splitLine[4]
                
                # if(splitLine[1] < splitLine[4]):      # removed
                    # splitLine[1] = splitLine[4]       # removed
                # curs.execute(f"INSERT INTO \"Movie\"(movie_id, title, length, release_date, mpaa_rating) VALUES ({movie_id}, \'{title}\', \'{length}\', \'{release_date}\', \'{mpaa_rating}\')")
                sql = "INSERT INTO \"Movie\" (movie_id, title, length, release_date, mpaa_rating) VALUES (%s, %s, %s, %s, %s)"
                val = (movie_id, title, length, release_date, mpaa_rating)
                curs.execute(sql, val)

        print("Successful inserted")
        conn.commit()
        conn.close()
except Exception as exception:
    print("Connection failed")
    print(exception)