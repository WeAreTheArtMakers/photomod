from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from picamera2 import Picamera2
from datetime import datetime
import time
import os
import cups
import pygame
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = 'supersecretkey'
pygame.mixer.init()

choose_sound = pygame.mixer.Sound("choose.wav")
countdown_sound = pygame.mixer.Sound("countdown.wav")
shutter_sound = pygame.mixer.Sound("shutter.wav")
finish_sound = pygame.mixer.Sound("finish.wav")

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

@app.route('/')
def index():
    return render_template('choose.html')

@app.route('/choose_option', methods=['POST'])
def choose_option():
    data = request.get_json()
    count = data.get('count', 1)
    session['PHOTO_COUNT'] = count
    choose_sound.play()
    return jsonify(success=True)

@app.route('/start_capture')
def start_capture():
    count = int(session.get('PHOTO_COUNT', 1))
    filenames = []

    for i in range(count):
        for j in range(5, 0, -1):
            countdown_sound.play()
            time.sleep(1)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}_{i+1}.jpg"
        filepath = os.path.join('static', filename)
        
        try:
            picam2.capture_file(filepath)
            filenames.append(filename)
            shutter_sound.play()
        except Exception as e:
            print(f"Fotoğraf çekiminde hata: {str(e)}")

    if len(filenames) == count:
        combined_image_path = combine_photos(filenames)
        return jsonify(success=True, filenames=[os.path.basename(combined_image_path)])
    else:
        return "Fotoğraf çekimi tamamlanamadı, lütfen tekrar deneyin.", 500

def combine_photos(filenames):
    if len(filenames) == 1:
        image = Image.open(os.path.join('static', filenames[0]))

        draw = ImageDraw.Draw(image)
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 50)

        date_text = datetime.now().strftime("%Y-%m-%d")
        draw.text((10, image.height - 60), date_text, fill="black", font=font)
        draw.text((10, image.height - 110), "modart", fill="black", font=font)

        combined_image_path = f"static/combined_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        image.save(combined_image_path)

        return combined_image_path

    elif len(filenames) == 4:
        images = [Image.open(os.path.join('static', filename)) for filename in filenames]

        width, height = images[0].size
        combined_image = Image.new('RGB', (width * 2, height * 2), (255, 255, 255))

        combined_image.paste(images[0], (0, 0))
        combined_image.paste(images[1], (width, 0))
        combined_image.paste(images[2], (0, height))
        combined_image.paste(images[3], (width, height))

        draw = ImageDraw.Draw(combined_image)
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 50)

        date_text = datetime.now().strftime("%Y-%m-%d")
        draw.text((10, combined_image.height - 60), date_text, fill="black", font=font)
        draw.text((10, combined_image.height - 110), "modart", fill="black", font=font)

        combined_image_path = f"static/combined_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        combined_image.save(combined_image_path)

        return combined_image_path

    else:
        raise ValueError("Yanlış sayıda fotoğraf çekildi.")

@app.route('/photo/<filenames>')
def show_photos(filenames):
    return render_template('photo.html', filenames=filenames)

@app.route('/print_photos', methods=['POST'])
def print_photos():
    data = request.get_json()
    filenames = data.get('filenames', [])

    conn = cups.Connection()

    # Yazıcının adını doğrudan tanımlayın
    printer_name = "Canon_E3400_series_"  # Yazıcınızın adı burada doğru şekilde tanımlandı

    if printer_name is None:
        return jsonify(success=False, error="Varsayılan yazıcı bulunamadı"), 500

    for filename in filenames:
        filepath = os.path.join('static', filename)
        if os.path.exists(filepath):
            try:
                conn.printFile(printer_name, filepath, "Photobooth Print", {})
                print(f"Yazdırma işlemi başarılı: {filepath}")
            except TypeError as e:
                print(f"Yazdırma hatası: {e}")
                return jsonify(success=False, error="Yazdırma işleminde hata oluştu"), 500
        else:
            print(f"Dosya bulunamadı: {filepath}")
            return jsonify(success=False, error="Dosya bulunamadı"), 404
    
    finish_sound.play()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
