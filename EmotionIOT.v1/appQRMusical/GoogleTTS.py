import requests
import os
import tempfile
import magic
import mimetypes
import subprocess

def editarExtension(file_path):
    """!
    @brief Función que edita la extensión de un archivo
    @param file_path Ruta del archivo
    @return Ruta del archivo correctamente formateada
    """
    type = magic.detect_from_filename(file_path).mime_type
    extension = str(mimetypes.guess_extension(type, strict=False))
    if extension is not None:
        if '.jpe' in extension:
            extension = extension.replace('jpe', 'jpg')
        os.rename(file_path, file_path + extension)
        return file_path + extension
    else:
        return file_path

def descargarAudio(url, params=None, headers=None):
    """!
    @brief Función que descarga en archivos temporales un archivo
    @param url Dirección web hacia la que enviar la petición
    @param params Parámetros para añadir a la dirección web
    @param headers Cabeceras de navegador para enviar en la petición
    @return Ruta del archivo correctamente formateada
    """
    try:
        jstr = requests.get(url, params=params, headers=headers, stream=True)
        ext = os.path.splitext(url)[1].split('?')[0]
        f = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        for chunk in jstr.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    except IOError as e:
        return None
    f.seek(0)
    if not ext:
        f.name = editarExtension(f.name)
    return open(f.name, 'rb')

def convertirFormatos(original):
    """!
    @brief Función que transforma el archivo mp3 descargado a formato ogg
    @param original Archivo original mp3
    @return Nombre del archivo ya convertido
    """

    converted = tempfile.NamedTemporaryFile(delete=False, suffix='.ogg')

    conv = subprocess.Popen(
        ['ffmpeg', '-i', original.name, '-c:a', 'libvorbis','-r:a' , '24000' , '-q:a', '5', '-b:a', '89k', '-y', converted.name],
        stdout=subprocess.PIPE)
    while True:
        data = conv.stdout.read(1024 * 100)
        if not data:
            break
        converted.write(data)

    return converted.name


def tts(texto):
    """!
    @brief Función que transforma un texto recibido por parámetro en un archivo de narración
    @param texto Cadena de texto a transformar
    @return Nombre del archivo temporal que contiene el audio narrado en formato ogg
    """

    url = 'http://translate.google.com/translate_tts'
    params = {
        'tl': 'es',
        'q': texto,
        'ie': 'UTF-8',
        'total': len(texto),
        'idx': 0,
        'client': 'tw-ob',
    }
    headers = {
        "Referer": 'http://translate.google.com/',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.8 Safari/537.36"
    }
    jstr = requests.get(
        url,
        params=params,
        headers=headers
    )
    if jstr.status_code != 200:
        print("Error")
        return
    result_url = jstr.url
    return convertirFormatos(descargarAudio(result_url, params=params, headers=headers))
