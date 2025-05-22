import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
import locale
import os 

ventana_modos = None
ventana_gatitos = None
idioma_actual = "en"
current_cat_photo = None
etiqueta_imagen_gatito = None

ICON_URL = "https://raw.githubusercontent.com/ripsaku/meow/refs/heads/main/meow.ico"


# --- Función para aplicar el icono descargado ---
def apply_window_icon(window):
    try:
        response = requests.get(ICON_URL)
        response.raise_for_status()
        icon_image_pil = Image.open(BytesIO(response.content))
        icon_tk = ImageTk.PhotoImage(icon_image_pil)
        window.iconphoto(True, icon_tk)
        window.image_icon_ref = icon_tk 
    except requests.exceptions.RequestException:
        pass
    except Exception:
        pass

def obtener_idioma():
    global idioma_actual
    try:
        locale.setlocale(locale.LC_ALL, '')
        lang_code, _ = locale.getlocale()
        if lang_code:
            idioma_actual = lang_code.split('_')[0]
        else:
            idioma_actual = "en"
    except locale.Error:
        idioma_actual = "en"
    except Exception:
        idioma_actual = "en"
    return idioma_actual

def obtener_traduccion(clave):
    traducciones = {
        "en": {
            "selecciona_modo": "SELECT A MODE",
            "predeterminado": "Default",
            "cerrar": "Close",
            "cambiar_modo": "Change Mode",
            "generar": "Generate",
            "connection_error_title": "Connection Error",
            "connection_error_msg": "Can't connect to API.",
            "error_title": "Error",
            "error_msg": "Sorry"
        },
        "es": {
            "selecciona_modo": "SELECCIONA UN MODO",
            "predeterminado": "Predeterminado",
            "cerrar": "Cerrar",
            "cambiar_modo": "Cambiar Modo",
            "generar": "Generar",
            "connection_error_title": "Error de Conexión",
            "connection_error_msg": "No se puede conectar a la API.",
            "error_title": "Error",
            "error_msg": "Lo siento"
        },
        "fr": {
            "selecciona_modo": "SÉLECTIONNEZ UN MODE",
            "predeterminado": "Par défaut",
            "cerrar": "Fermer",
            "cambiar_modo": "Changer de Mode",
            "generar": "Générer",
            "connection_error_title": "Erreur de Connexion",
            "connection_error_msg": "Impossible de se connecter à l'API.",
            "error_title": "Erreur",
            "error_msg": "Désolé"
        },
        "de": {
            "selecciona_modo": "MODUS WÄHLEN",
            "predeterminado": "Standard",
            "cerrar": "Schließen",
            "cambiar_modo": "Modus wechseln",
            "generar": "Generieren",
            "connection_error_title": "Verbindungsfehler",
            "connection_error_msg": "Verbindung zur API nicht möglich.",
            "error_title": "Fehler",
            "error_msg": "Entschuldigung"
        },
        "it": {
            "selecciona_modo": "SELEZIONA UNA MODALITÀ",
            "predeterminado": "Predefinito",
            "cerrar": "Chiudi",
            "cambiar_modo": "Cambia Modalità",
            "generar": "Genera",
            "connection_error_title": "Errore di Connessione",
            "connection_error_msg": "Impossibile connettersi all'API.",
            "error_title": "Errore",
            "error_msg": "Spiacente"
        },
        "pt": {
            "selecciona_modo": "SELECIONE UM MODO",
            "predeterminado": "Padrão",
            "cerrar": "Fechar",
            "cambiar_modo": "Mudar Modo",
            "generar": "Gerar",
            "connection_error_title": "Erro de Conexão",
            "connection_error_msg": "Não é possível conectar à API.",
            "error_title": "Erro",
            "error_msg": "Desculpe"
        },
        "zh": {
            "selecciona_modo": "选择模式",
            "predeterminado": "默认",
            "cerrar": "关闭",
            "cambiar_modo": "更改模式",
            "generar": "生成",
            "connection_error_title": "连接错误",
            "connection_error_msg": "无法连接到API。",
            "error_title": "错误",
            "error_msg": "抱歉"
        },
        "ja": {
            "selecciona_modo": "モードを選択",
            "predeterminado": "デフォルト",
            "cerrar": "閉じる",
            "cambiar_modo": "モード変更",
            "generar": "生成",
            "connection_error_title": "接続エラー",
            "connection_error_msg": "APIに接続できません。",
            "error_title": "エラー",
            "error_msg": "ごめんなさい"
        },
        "ru": {
            "selecciona_modo": "ВЫБЕРИТЕ РЕЖИМ",
            "predeterminado": "По умолчанию",
            "cerrar": "Закрыть",
            "cambiar_modo": "Изменить режим",
            "generar": "Генерировать",
            "connection_error_title": "Ошибка подключения",
            "connection_error_msg": "Не удалось подключиться к API.",
            "error_title": "Ошибка",
            "error_msg": "Извините"
        }
    }
    return traducciones.get(idioma_actual, traducciones["en"]).get(clave, clave)

def centrar_ventana(ventana, ancho_ventana, alto_ventana):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

def mostrar_error(titulo, mensaje):
    obtener_idioma()
    ventana_error = tk.Toplevel()
    ventana_error.title(titulo)
    etiqueta_error = tk.Label(ventana_error, text=mensaje, padx=20, pady=20)
    etiqueta_error.pack()
    boton_ok = tk.Button(ventana_error, text="OK", command=ventana_error.destroy)
    boton_ok.pack(pady=10)

    ventana_error.update_idletasks()
    ancho_ventana_error = etiqueta_error.winfo_reqwidth() + 40
    alto_ventana_error = etiqueta_error.winfo_reqheight() + boton_ok.winfo_reqheight() + 40
    centrar_ventana(ventana_error, ancho_ventana_error, alto_ventana_error)

def iniciar_programa(modo_seleccionado):
    global ventana_modos
    if ventana_modos and ventana_modos.winfo_exists():
        ventana_modos.withdraw()
    crear_o_actualizar_ventana_gatitos()

def volver_a_modos():
    global ventana_gatitos, ventana_modos
    if ventana_gatitos and ventana_gatitos.winfo_exists():
        ventana_gatitos.withdraw()

    if ventana_modos and ventana_modos.winfo_exists():
        ventana_modos.deiconify()
        ventana_modos.lift()
    else:
        crear_ventana_modos()

def crear_o_actualizar_ventana_gatitos():
    global ventana_gatitos, current_cat_photo, etiqueta_imagen_gatito

    try:
        response = requests.get("https://cataas.com/cat/cute")
        response.raise_for_status()

        imagen = Image.open(BytesIO(response.content))

        if tk._default_root:
            ancho_pantalla = tk._default_root.winfo_screenwidth()
            alto_pantalla = tk._default_root.winfo_screenheight()
        else:
            temp_root = tk.Tk()
            temp_root.withdraw()
            ancho_pantalla = temp_root.winfo_screenwidth()
            alto_pantalla = temp_root.winfo_screenheight()
            temp_root.destroy()

        ancho_max = int(ancho_pantalla * 0.62)
        alto_max = int(alto_pantalla * 0.62)
        
        imagen.thumbnail((ancho_max, alto_max), Image.LANCZOS)

        if not (ventana_gatitos and ventana_gatitos.winfo_exists()):
            ventana_gatitos = tk.Toplevel()
            ventana_gatitos.title("˃ 𖥦 ˂")
            ventana_gatitos.resizable(False, False)
            ventana_gatitos.protocol("WM_DELETE_WINDOW", ventana_gatitos.quit)
            
            apply_window_icon(ventana_gatitos)

            etiqueta_imagen_gatito = tk.Label(ventana_gatitos)
            etiqueta_imagen_gatito.pack(padx=10, pady=10)

            frame_botones = tk.Frame(ventana_gatitos)
            frame_botones.pack(pady=5)

            boton_cerrar = tk.Button(frame_botones, text=obtener_traduccion("cerrar"), command=ventana_gatitos.quit)
            boton_cerrar.pack(side=tk.LEFT, padx=5)

            boton_cambiar_modo = tk.Button(frame_botones, text=obtener_traduccion("cambiar_modo"), command=volver_a_modos)
            boton_cambiar_modo.pack(side=tk.LEFT, padx=5)

            boton_generar = tk.Button(frame_botones, text=obtener_traduccion("generar"), command=crear_o_actualizar_ventana_gatitos)
            boton_generar.pack(side=tk.LEFT, padx=5)

        current_cat_photo = ImageTk.PhotoImage(imagen)
        etiqueta_imagen_gatito.config(image=current_cat_photo)
        etiqueta_imagen_gatito.image_ref = current_cat_photo

        ventana_gatitos.update_idletasks() 

        frame_altura = 0
        for widget in ventana_gatitos.winfo_children():
            if isinstance(widget, tk.Frame):
                frame_altura = widget.winfo_reqheight()
                break
        
        ancho_ventana_final = etiqueta_imagen_gatito.winfo_reqwidth() + (2 * 10)
        alto_ventana_final = etiqueta_imagen_gatito.winfo_reqheight() + (2 * 10) + frame_altura + 5

        centrar_ventana(ventana_gatitos, ancho_ventana_final, alto_ventana_final)

        ventana_gatitos.deiconify()
        ventana_gatitos.lift()

    except requests.exceptions.RequestException as e:
        print(f"Error descargando la imagen: {e}")
        mostrar_error(obtener_traduccion("connection_error_title"), obtener_traduccion("connection_error_msg"))
    except Exception as e:
        print(f"Error inesperado: {e}")
        mostrar_error(obtener_traduccion("error_title"), f"{obtener_traduccion('error_msg')}: {e}")

def crear_ventana_modos():
    global ventana_modos

    if ventana_modos and ventana_modos.winfo_exists():
        ventana_modos.deiconify()
        ventana_modos.lift()
        return

    obtener_idioma()

    if not tk._default_root:
        ventana_modos = tk.Tk()
        ventana_modos.protocol("WM_DELETE_WINDOW", ventana_modos.quit)
    else:
        ventana_modos = tk.Toplevel() 
        ventana_modos.protocol("WM_DELETE_WINDOW", ventana_modos.destroy)
    
    # Aplica el icono a la ventana de modos
    apply_window_icon(ventana_modos)

    ventana_modos.title("˃ 𖥦 ˂")
    ventana_modos.resizable(False, False)

    etiqueta_modo = tk.Label(ventana_modos, text=obtener_traduccion("selecciona_modo"), font=("Arial", 14, "bold"))
    etiqueta_modo.pack(pady=20)

    modo_predeterminado = tk.BooleanVar(value=True)
    checkbox_predeterminado = tk.Checkbutton(ventana_modos, text=obtener_traduccion("predeterminado"), variable=modo_predeterminado)
    checkbox_predeterminado.pack(pady=5)

    boton_meow = tk.Button(ventana_modos, text="MEOW!", command=lambda: iniciar_programa("predeterminado" if modo_predeterminado.get() else None))
    boton_meow.pack(pady=20)

    ventana_modos.update_idletasks()

    ancho_contenido = max(etiqueta_modo.winfo_reqwidth(), checkbox_predeterminado.winfo_reqwidth(), boton_meow.winfo_reqwidth())
    ancho_ventana_modos = ancho_contenido + 100
    alto_ventana_modos = etiqueta_modo.winfo_reqheight() + checkbox_predeterminado.winfo_reqheight() + boton_meow.winfo_reqheight() + 100

    centrar_ventana(ventana_modos, ancho_ventana_modos, alto_ventana_modos)

    if isinstance(ventana_modos, tk.Tk):
        ventana_modos.mainloop()

if __name__ == "__main__":
    crear_ventana_modos()