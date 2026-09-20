"""
Servidor local de desarrollo con soporte de Hot-Reload para la presentación.
Ejecutar con:
    uv run dev.py
o:
    python dev.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# Asegurar codificación UTF-8 en Windows para evitar errores de consola
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class NoCacheHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Desactivar la caché para que el hot-reload en el navegador sea instantáneo
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        # Silenciar los logs de sondeo continuo del hot-reload para mantener la terminal limpia
        if len(args) >= 2 and "GET /index.html" in str(args[0]) and "200" in str(args[1]):
            return
        super().log_message(format, *args)


def main():
    # Permitir reutilizar la dirección rápidamente si se reinicia el servidor
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer(("", PORT), NoCacheHTTPHandler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            print("=" * 65)
            print("[HOT-RELOAD] SERVIDOR DE DESARROLLO ACTIVO")
            print(f"URL: {url}")
            print("=" * 65)
            print("Cada vez que guardes cambios en 'index.html', el navegador")
            print("se actualizara automaticamente en menos de 1 segundo.")
            print("Tu posicion actual de diapositiva se mantendra intacta.")
            print("Presiona Ctrl + C en esta terminal para detener el servidor.\n")

            # Intentar abrir automáticamente en el navegador por defecto
            try:
                webbrowser.open(url)
            except Exception:
                pass

            httpd.serve_forever()
    except OSError as e:
        if e.errno in (98, 10048):
            print(f"[!] El puerto {PORT} ya esta en uso. Prueba cerrando el proceso anterior.")
        else:
            raise e
    except KeyboardInterrupt:
        print("\n[!] Servidor detenido.")


if __name__ == "__main__":
    main()
