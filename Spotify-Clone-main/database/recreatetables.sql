DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


CREATE TABLE IF NOT EXISTS albums (
    album_id UUID PRIMARY KEY,   
    album_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id UUID PRIMARY KEY,   
    genre_name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS tracks (
    track_id UUID PRIMARY KEY,   
    album_id UUID,               
    track_name VARCHAR(255),
    popularity INTEGER,
    duration_ms INTEGER,
    explicit BOOLEAN,
    danceability FLOAT8,
    energy FLOAT8,
    key INTEGER,
    loudness FLOAT8,
    mode INTEGER,
    speechiness FLOAT8,
    acousticness FLOAT8,
    instrumentalness FLOAT8,
    liveness FLOAT8,
    valence FLOAT8,
    tempo FLOAT8,
    time_signature INTEGER,
    genre_id UUID,               
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE IF NOT EXISTS artists (
    artist_id UUID PRIMARY KEY,   
    name VARCHAR(255),
    followers INTEGER,
    popularity INTEGER
);

CREATE TABLE IF NOT EXISTS artists_tracks (
    artist_id UUID NOT NULL,      
    track_id UUID NOT NULL,       
    PRIMARY KEY (artist_id, track_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);

create index idx_tracks_popularity on tracks(popularity);
create index idx_tracks_duration on tracks(duration_ms);

create index idx_artist_name on artists(name);

create index idx_artist_track on artists_tracks(artist_id, track_id);

create index idx_album_tracks on tracks(album_id);

create view popular_tracks as
select track_name, popularity, album_id
from tracks
order by popularity desc;

create view track_artist_info as
select t.track_name, t.popularity, a.name as artist_name, al.album_name, g.genre_name
from tracks t
join artists_tracks at on t.track_id = at.track_id
join artists a on at.artist_id = a.artist_id
join albums al on t.album_id = al.album_id
join genres g on t.genre_id = g.genre_id;

