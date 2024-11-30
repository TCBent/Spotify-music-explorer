## Indices
\subsection{Índices}

\begin{Enumerate}

\item \textbf{idx_tracks_popularity:} El primer índice es de la tabla tracks y se crea en la columna popularidad. Este índice permite realizar búsquedas y ordenamiento de tracks en base su popularidad. Como mencionado, es especialmente útil si se realizan consultas que filtran u ordenan la columna de popularidad. Por ejemplo, se encuentran las canciones más populares o se generan clasificaciones.

\item \textbf{idx_tracks_duration:} Se crea otro índice en tracks, para la columna de duración de las canciones. Nuevamente, este índice es especialmente útil si se desea buscar canciones que estén dentro de un intervalo específico de duración o si se desea ordenar las canciones en base a su duración. 

\item \textbf{idx_artist_name:} El tercer índice se crea en la tabla artistas para la columna de nombres. Como se espera que los artistas participen dentro de las consultas, se espera que por la frecuencia de estas el índice optimice acelere las búsquedas y ahorre recursos.

\item \textbf{idx_artist_track:} Se crea un índice en la tabla artist tracks para las columnas \textbf{artist_id} y \textbf{track_id}. Este índice acelera operaciones o consultas que involucren a lasdos columnas mencionadas. Por ejemplo, buscar las canciones asociadas a un artista determinado o los artistas que colaboraron en una canción. 

\item \textbf{idx_album_tracks:} El último índice creado también es para la tabla tracks, y se crea en la columna \textbf{album_id}. Este índice ayuda a a la consulta de tracks asociadas a un álbum específico. Sirve además para consultas que tengan que juntar álbums. 
\end{enumerate}

Todos los índices creados son tipo B-árbol. Esto ya que son ideales para consultas que requieran comparaciones, o cuando se realizan búsquedas dentro de un rango.



## Vistas
\subsection{Vistas}

Se crea la vista popular tracks, que se beneficia del primer índice creado, ya que los tracks están ordenados por popularidad. 

Además se crea la vista \textbf{track_artist_info}. El cuarto índice mejora el join entre tracks y artists tracks ya que tiene un acceso más rápido a sus relaciones. El tercer índice aquí ayuda a hacer una búsqueda más rápida de los artistas en el join con la tabla artists. Por último, el quinto índice aquí ayuda a optimizar el join entre tracks y albums al realizar una búsqueda más rápida basa en el \textbf{album_id}.