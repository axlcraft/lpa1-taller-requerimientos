# hotel_app.py - Archivo principal para el ejecutable
import os
import sys
from app import create_app
import webbrowser
import threading
import time

def open_browser():
    """Abrir el navegador después de un breve retraso"""
    time.sleep(1.5)  # Esperar a que el servidor esté listo
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    # Obtener el directorio base del ejecutable
    if getattr(sys, 'frozen', False):
        # Si estamos ejecutando desde un ejecutable de PyInstaller
        base_dir = sys._MEIPASS
    else:
        # Si estamos ejecutando desde el script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cambiar al directorio base
    os.chdir(base_dir)
    
    # Crear la aplicación Flask
    flask_app = create_app()
    
    # Configurar para producción
    flask_app.config['DEBUG'] = False
    flask_app.config['ENV'] = 'production'
    
    print("🚀 Iniciando Sistema de Reservas de Hotel...")
    print("📍 Servidor corriendo en: http://127.0.0.1:5000")
    print("🌐 Abriendo navegador automáticamente...")
    print("❌ Para cerrar la aplicación, presiona Ctrl+C")
    
    # Abrir el navegador en un hilo separado
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Ejecutar la aplicación Flask
        flask_app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error al ejecutar la aplicación: {e}")
        input("Presiona Enter para cerrar...")
