"""
Generador de códigos QR en SVG utilizando segno para garantizar
cumplimiento total del estándar ISO/IEC 18004 y escaneo universal.
"""
import segno

def generate_qr_svg(url: str, filename: str):
    qr = segno.make(url, error='m')
    # scale=6 con border=4 (quiet zone estándar ISO)
    qr.save(filename, scale=6, dark='#0f172a', light='#ffffff', border=4)
    print(f'Generado exitosamente: {filename}')

if __name__ == '__main__':
    generate_qr_svg('https://josu-dev.github.io/apu-ttps-final', 'qr_presentation.svg')
    generate_qr_svg('https://github.com/josu-dev/apu-ttps-final', 'qr_repo.svg')

