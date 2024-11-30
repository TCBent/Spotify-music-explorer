import psycopg2
import csv
import uuid  # en mi caso, ocupé uuid

# conn base de datos
conn = psycopg2.connect(host="localhost", user="postgres", database="postgres", password="password", port="5432")
cur = conn.cursor()


cur.execute("TRUNCATE TABLE tracks RESTART IDENTITY CASCADE")
cur.execute("TRUNCATE TABLE artists RESTART IDENTITY CASCADE")
cur.execute("TRUNCATE TABLE albums RESTART IDENTITY CASCADE")
cur.execute("TRUNCATE TABLE genres RESTART IDENTITY CASCADE")
cur.execute("TRUNCATE TABLE artists_tracks RESTART IDENTITY CASCADE")

# archivo de nodos, reemplazar path
with open('path\llnodes.csv', 'r', encoding='utf-8') as csvfile2:
    reader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
    next(reader2)  # skip header

    for i, row in enumerate(reader2, start=2):
        try:
            artist_id = str(uuid.uuid4())  # genera uuid
            name = row[1]
            followers = float(row[2])
            popularity = row[3]

            # print consola
            print(f"\nInsertando fila {i}: {name}")

            # verificar si el artista ya existe
            cur.execute("SELECT artist_id FROM artists WHERE name = %s", (name,))
            artista = cur.fetchone()

            if not artista:
                # insertar artista si no existe
                cur.execute("INSERT INTO artists (artist_id, name, followers, popularity) VALUES (%s, %s, %s, %s)", (artist_id, name, followers, popularity))
                print(f"Artista insertado: {name} con ID {artist_id}")
            else:
                print(f"Álbum ya existe: {name}")
            conn.commit()

        except Exception as e:
            print(f"Error en fila {i}: {e}")
            conn.rollback()  # deshacer cambios en caso de error
            continue  # pasar a la siguiente fila

###############################################################################################
# leer el archivo de tracks, reemplazar path
with open('path\dataset.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader)  # skip header

    for i, row in enumerate(reader, start=2):
        try:
            track_id = str(uuid.uuid4())  # genera uuid track
            artists = row[2].split(";")  # manejar múltiples artistas
            album_name = row[3]
            track_name = row[4]
            popularity = row[5]
            duration_ms = row[6]
            explicit = row[7]
            danceability = row[8]
            energy = row[9]
            key = row[10]
            loudness = row[11]
            mode = row[12]
            speechiness = row[13]
            acousticness = row[14]
            instrumentalness = row[15]
            liveness = row[16]
            valence = row[17]
            tempo = row[18]
            time_signature = row[19]
            track_genre = row[20]

            # print consola
            print(f"\nInsertando fila {i}: {track_name}")

            # verificar si el album ya existe
            cur.execute("SELECT album_id FROM albums WHERE album_name = %s", (album_name,))
            album = cur.fetchone()

            if not album:
                album_id = str(uuid.uuid4())  # genera uuid album
                cur.execute("INSERT INTO albums (album_id, album_name) VALUES (%s, %s)", (album_id, album_name))
                print(f"Álbum insertado: {album_name} con ID {album_id}")
            else:
                album_id = album[0]
                print(f"Álbum ya existe: {album_name} con ID {album_id}")
            conn.commit()

            # insertar género si no existe
            if track_genre:  # verificar que el género no esté vacío
                cur.execute("SELECT genre_id FROM genres WHERE genre_name = %s", (track_genre,))
                genre = cur.fetchone()
                if not genre:
                    genre_id = str(uuid.uuid4())  # genera uuid género
                    cur.execute("INSERT INTO genres (genre_id, genre_name) VALUES (%s, %s)", (genre_id, track_genre))
                    print(f"Género insertado: {track_genre} con ID {genre_id}")
                else:
                    genre_id = genre[0]
                    print(f"Género ya existe: {track_genre} con ID {genre_id}")
            else:
                genre_id = None  # si no hay género, se permite que sea nulo
                print(f"Warning: Track sin género - fila {i}")
            conn.commit()

            # insertar track
            cur.execute("""
                INSERT INTO tracks (track_id, album_id, track_name, popularity, duration_ms, explicit, danceability,
                energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, 
                time_signature, genre_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (track_id, album_id, track_name, popularity, duration_ms, explicit, danceability, energy, key, 
                  loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, 
                  time_signature, genre_id))
            print(f"Track insertado: {track_name} con ID {track_id}")
            conn.commit()

            # insertar artistas y la relación con la canción
            for artist_name in artists:
                cur.execute("SELECT artist_id FROM artists WHERE name = %s", (artist_name.strip(),))
                artist = cur.fetchone()
                if not artist:
                    artist_id = str(uuid.uuid4())  # genera uuid artista
                    cur.execute("INSERT INTO artists (artist_id, name) VALUES (%s, %s)", (artist_id, artist_name.strip()))
                    print(f"Artista insertado: {artist_name.strip()} con ID {artist_id}")
                else:
                    artist_id = artist[0]
                    print(f"Artista ya existe: {artist_name.strip()} con ID {artist_id}")
                conn.commit()

                # insertar relación en artists_tracks
                cur.execute("INSERT INTO artists_tracks (artist_id, track_id) VALUES (%s, %s)", (artist_id, track_id))
                print(f"Relación insertada: artista {artist_id} con track {track_id}")
                conn.commit()

        except Exception as e:
            print(f"Error en fila {i}: {e}")
            conn.rollback()  # deshacer cambios en caso de error
            continue  # pasar a la siguiente fila

# confirmar los cambios
conn.commit()

# cerrar la conexión
cur.close()
conn.close()
