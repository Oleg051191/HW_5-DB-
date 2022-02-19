from pprint import pprint
import sqlalchemy
db = 'postgresql://postgres:escort@localhost:5432/data_b_hw2'
engine = sqlalchemy.create_engine(db)
sql_query = engine.connect()

sel1 = sql_query.execute("""SELECT genre_id, COUNT(artist_id) AS C_art FROM artist_genre 
                            GROUP BY genre_id ORDER BY genre_id""").fetchall()
# print(sel1)
sel2 = sql_query.execute("""SELECT title_album, count(t.id) as t_count FROM
                            albums a JOIN tracks t ON a.id=t.name_album
                            WHERE year_production BETWEEN '01-01-2019' AND '31-12-2020'
                            GROUP BY a.title_album;""").fetchall()
# print(sel2)

sel3 = sql_query.execute("""SELECT title_album, count(t.id) as t_count, round(avg(t.duration),1) as d_avg FROM albums a
                            JOIN tracks t ON a.id=t.name_album
                            GROUP BY a.title_album 
                            ORDER BY d_avg DESC;""").fetchall()
# pprint(sel3)

sel4 = sql_query.execute("""SELECT distinct name_of_artist, title_album, year_production  FROM artists a 
                            JOIN artist_albums aa ON a.id=aa.artist_id 
                            JOIN albums a2 ON aa.album_id = a2.id 
                            WHERE year_production NOT IN(SELECT year_production FROM albums
                             WHERE year_production BETWEEN '01-01-2019' and '31-12-2019');""").fetchall()
# pprint(sel4)

sel5 = sql_query.execute("""SELECT name_collection, count(t.id) as Rammstein_tracks FROM collection c
                            JOIN collection_track ct ON c.id=ct.collection_id JOIN tracks t ON ct.track_id=t.id
                            JOIN albums a ON a.id=t.name_album JOIN artist_albums aa ON aa.album_id = a.id
                            JOIN artists a2 ON aa.artist_id =a2.id
                            WHERE name_of_artist = 'Rammstein'
                            GROUP BY name_collection
                            ORDER BY Rammstein_tracks DESC;""").fetchall()
# print(sel5)

sel6 = sql_query.execute("""SELECT title_album FROM albums a 
                            JOIN artist_albums aa ON a.id = aa.album_id 
                            JOIN artists a2 ON aa.artist_id = a2.id 
                            JOIN artist_genre ag ON a2.id = ag.artist_id 
                            JOIN genre g ON ag.genre_id = g.id 
                            GROUP BY title_album 
                            HAVING count(name_of_artist)>1;""").fetchall()
# pprint(sel6)

sel7 = sql_query.execute("""SELECT id, name_track, collection_id FROM tracks t
                            LEFT JOIN collection_track ct ON t.id=ct.track_id 
                            WHERE collection_id is null ORDER BY id;""").fetchall()
# pprint(sel7)

sel8 = sql_query.execute("""SELECT name_of_artist,name_track , duration FROM artists a 
                            JOIN artist_albums aa on a.id=aa.artist_id 
                            JOIN albums a2 on aa.album_id=a2.id 
                            JOIN tracks t on a2.id=t.name_album 
                            WHERE duration =(SELECT MIN(duration) FROM tracks);""").fetchone()
# pprint(sel8)


                                    #Альбом, где меньше всего треков
sel9 = sql_query.execute("""SELECT title_album, count(name_track) as tracks_c 
                            FROM albums a 
                            JOIN tracks t ON a.id=t.name_album 
                            GROUP BY title_album 
                            HAVING COUNT(name_track) = (SELECT MIN(name_album) FROM tracks);""").fetchall()
# print(sel9)

sel10 = sql_query.execute("""WITH new_table as 
                             (SELECT name_album, COUNT(t.id) as tracks_c FROM tracks t 
                             JOIN albums a ON t.name_album=a.id 
                             GROUP BY name_album) 
                             SELECT name_album, tracks_c FROM new_table 
                             WHERE tracks_c < (SELECT MAX(tracks_c) FROM new_table);""").fetchall()
pprint(sel10)