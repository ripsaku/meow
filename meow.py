import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
import locale

def obtener_idioma():
    try:
        locale.setlocale(locale.LC_ALL, '')
        lang_code, _ = locale.getlocale()
        if lang_code:
            return lang_code.split('_')[0]
        else:
            return "en"
    except locale.Error:
        return "en"
    except Exception as e:
        return "en"

def mostrar_gatito():
    idioma = obtener_idioma() # Llama a la función para obtener el idioma

    try:
        response = requests.get("https://cataas.com/cat/cute")
        response.raise_for_status()

        imagen = Image.open(BytesIO(response.content))

        ancho_max = 1366
        alto_max = 768
        imagen.thumbnail((ancho_max, alto_max), Image.LANCZOS)

        ventana = tk.Tk() # La ventana se crea aquí, antes de usarla
        ventana.title("˃ 𖥦 ˂")
        ventana.resizable(False, False)

        foto = ImageTk.PhotoImage(imagen)

        etiqueta_imagen = tk.Label(ventana, image=foto)
        etiqueta_imagen.pack(padx=10, pady=10)
        etiqueta_imagen.image = foto

        # Define el texto del botón "Close" según el idioma
        if idioma == "en":
            texto_boton_cerrar = "Close"
        elif idioma == "es":
            texto_boton_cerrar = "Cerrar"
        elif idioma == "fr":
            texto_boton_cerrar = "Fermer"
        elif idioma == "de":
            texto_boton_cerrar = "Schließen"
        elif idioma == "it":
            texto_boton_cerrar = "Chiudi"
        elif idioma == "pt":
            texto_boton_cerrar = "Fechar"
        elif idioma == "zh":
            texto_boton_cerrar = "关闭"
        elif idioma == "ja":
            texto_boton_cerrar = "閉じる"
        elif idioma == "ru":
            texto_boton_cerrar = "Закрыть"
        else:
            texto_boton_cerrar = "Close" # Idioma por defecto si no coincide con ninguno

        boton_cerrar = tk.Button(ventana, text=texto_boton_cerrar, command=ventana.destroy)
        boton_cerrar.pack(pady=5)

        ancho_imagen = foto.width()
        alto_imagen = foto.height()
        ancho_ventana = ancho_imagen + 20
        alto_ventana = alto_imagen + 20 + 40
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        ventana.mainloop()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading the image: {e}")
        mostrar_error("Connection error", "Can't connect to API.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        mostrar_error("Error", f"sorry: {e}")

def mostrar_error(titulo, mensaje):
    ventana_error = tk.Tk()
    ventana_error.title(titulo)
    etiqueta_error = tk.Label(ventana_error, text=mensaje, padx=20, pady=20)
    etiqueta_error.pack()
    boton_ok = tk.Button(ventana_error, text="OK", command=ventana_error.destroy)
    boton_ok.pack(pady=10)
    ventana_error.mainloop()

if __name__ == "__main__":
    mostrar_gatito()

# MEOW 
# https://github.com/ripsaku
