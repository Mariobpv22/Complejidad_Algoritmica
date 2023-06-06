import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configura tus credenciales de la API de Spotify
CLIENT_ID = 'Insertar cliente ID de Spotify'
CLIENT_SECRET = 'Insertar client secret de Spotify'

# Número de canciones que deseas extraer
NUM_CANCIONES = 1500

# Encabezados de las columnas en el archivo CSV
HEADER = ['Artista', 'Canción', 'Duración (segundos)', 'Álbum', 'Año', 'Género']

# Función para obtener los datos de una canción
def obtener_datos_cancion(cancion):
    artistas = ', '.join([artista['name'] for artista in cancion['artists']])
    nombre_cancion = cancion['name']
    duracion_ms = cancion['duration_ms']
    duracion_segundos = duracion_ms // 1000
    album = cancion['album']['name']
    año = cancion['album']['release_date'][:4]
    genero = cancion.get('genres', [''])[0]
    
    return [artistas], [nombre_cancion], [duracion_segundos], [album], [año], [genero]

# Función principal para obtener las canciones
def obtener_canciones(playlist_id):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    canciones = []
    canciones_recopiladas = 0

    offset = 0
    while canciones_recopiladas < NUM_CANCIONES:
        resultados = sp.playlist_items(playlist_id, fields='items.track', limit=100, offset=offset)
        tracks = resultados['items']
        
        if len(tracks) == 0:
            break
        
        for item in tracks:
            if canciones_recopiladas == NUM_CANCIONES:
                break
            
            try:
                track = item['track']
                artistas, nombre_cancion, duracion_segundos, album, año, genero = obtener_datos_cancion(track)
                canciones.append([artistas, nombre_cancion, duracion_segundos, album, año, genero])
                canciones_recopiladas += 1
                print('Canción', canciones_recopiladas, 'recopilada.')
            except:
                print('Error al obtener datos de la canción.')
        
        offset += 100

    return canciones


# Función para escribir los datos en un archivo CSV
def escribir_csv(canciones):
    with open('canciones.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerow(HEADER)

        for cancion in canciones:
            writer.writerow([c[0] for c in cancion])

    print('Archivo CSV generado correctamente.')

# Obtener las canciones y escribir el archivo CSV
playlist_id = '1pmrctNR3N6XmMlBUOMIVD'
canciones = obtener_canciones(playlist_id)
escribir_csv(canciones)
