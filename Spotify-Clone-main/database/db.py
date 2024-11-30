import psycopg2
import csv
import uuid

id = uuid.uuid4()
print(id)
# with open('dataset.csv', 'r') as file:
#     pass

def getConnection():
    conn = psycopg2.connect(
        database= 'postgres',
        user= 'postgres',
        password= 'password',       
        host= 'localhost',
        port= '5432'
        )
    return conn

def artistas_con_mas_canciones_un_genero_especifico(genre):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.name AS artist_name, COUNT(t.track_id) AS num_tracks 
        FROM public.artists a 
        JOIN public.artists_tracks at ON a.artist_id = at.artist_id 
        JOIN public.tracks t ON at.track_id = t.track_id 
        JOIN public.genres g ON t.genre_id = g.genre_id 
        WHERE g.genre_name = %s 
        GROUP BY a.name 
        ORDER BY num_tracks DESC 
        LIMIT 20
    ''', (genre, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def colaboradores_de_un_artista(artist_name):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT
        a2.name AS collaborator_name
        FROM public.artists a1
        JOIN public.artists_tracks at1 ON a1.artist_id = at1.artist_id
        JOIN public.artists_tracks at2 ON at1.track_id = at2.track_id
        JOIN public.artists a2 ON at2.artist_id = a2.artist_id
        WHERE a1.name = %s  
        AND a2.artist_id != a1.artist_id  
    ''', (artist_name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def albumes_en_que_ha_colaborado(artist_name):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT al.album_id, al.album_name
        FROM public.albums al
        JOIN public.tracks t ON al.album_id = t.album_id
        JOIN public.artists_tracks at1 ON t.track_id = at1.track_id
        JOIN public.artists a1 ON at1.artist_id = a1.artist_id
        JOIN public.artists_tracks at2 ON t.track_id = at2.track_id
        JOIN public.artists a2 ON at2.artist_id = a2.artist_id
        WHERE a1.name = %s
        AND a2.artist_id != a1.artist_id
    ''', (artist_name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def info_canciones_populares(artist_name):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            tai.track_name,
            tai.popularity,
            tai.album_name,
            tai.genre_name
        FROM 
            track_artist_info tai
        WHERE 
            tai.artist_name ILIKE %s
        ORDER BY 
            tai.popularity DESC;
    ''', (artist_name, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def info_genre_rank(genre):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        WITH genre_filtered_tracks AS (
        SELECT 
            t.track_id,
            t.popularity,
            t.genre_id
        FROM 
            tracks t
        JOIN 
            genres g ON t.genre_id = g.genre_id
        WHERE 
            g.genre_name ILIKE %s 
    ),
    artist_popularity_stats AS (
        SELECT 
            at.artist_id,
            a.name AS artist_name,
            COUNT(gft.track_id) AS total_tracks,
            ROUND(AVG(gft.popularity), 4) AS avg_popularity
        FROM 
            genre_filtered_tracks gft
        JOIN 
            artists_tracks at ON gft.track_id = at.track_id
        JOIN 
            artists a ON at.artist_id = a.artist_id
        GROUP BY 
            at.artist_id, a.name
    ),
    top_artists AS (
        SELECT 
            aps.artist_name,
            aps.total_tracks,
            aps.avg_popularity
        FROM 
            artist_popularity_stats aps
        WHERE 
            aps.avg_popularity > (
                SELECT 
                    ROUND(AVG(avg_popularity), 4)
                FROM 
                    artist_popularity_stats
            ) 
        ORDER BY 
            aps.avg_popularity DESC, aps.total_tracks DESC
    )
    SELECT * 
    FROM top_artists
    LIMIT 30
    ''', (genre, ))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_genres(query):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT genre_name 
        FROM public.genres 
        WHERE genre_name ILIKE %s 
        LIMIT 10
    ''', (f'%{query}%',))
    genres = cursor.fetchall()
    cursor.close()
    conn.close()
    return [genre[0] for genre in genres]