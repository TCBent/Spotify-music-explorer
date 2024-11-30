## Información general 

Para realizar esta aplicación se ocupó el framework de Flask en python y se ocuparon además los repositorios en [Créditos](#créditos). Además, en esta versión del código se ocupó la librería uuid de python para crear las llaves primarias. Para evitar inyecciones se ocuparon la función escape de la librería markupsafe y además se escribieron consultas preparadas. 

Del código citado se ocuparon los archivos de index.html, los códigos de css, y los javascript dropdown.js y script.js. Como mencionado, el templating se hizo a partir del archivo index.html, y partir de este se crearon el resto de los templates.

## Instrucciones de uso

Luego de descargar el repositorio se recomienda crear un ambiente virtual, activarlo, y escribir en la consola:

    pip install requirements.txt

Si están en carpetas distintas (en relación al venv) verificar el path del archivo requirements. 

- Crear tablas con el archivo recreatetables.sql
- Dentro del archivo createtable.py modificar los datos de conexión de la base de datos
- Correr createtable.py
- Modificar los datos de conexión del archivo db.py
- Cambiar consola al directorio del archivo app.py
- En consola correr:

    flask run

- Copiar el link http y pegarlo en el buscador deseado

## <a name="créditos"></a>Créditos

Github
- [0xtaufeeq](https://github.com/0xtaufeeq/Spotify-Clone)

Kaggle
- [Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
- [nodes](https://www.kaggle.com/datasets/jfreyberg/spotify-artist-feature-collaboration-network?select=nodes.csv)
