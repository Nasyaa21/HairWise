# =[Modules dan Packages]========================

from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
import os
from PIL import Image
from fungsi import make_model, NUM_CLASSES

# =[Variabel Global]=============================

app = Flask(__name__, static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
app.config['UPLOAD_PATH'] = './static/images/uploads/'

model = None

hair_classes = ["Curly Hair", "Straight Hair", "Wavy Hair"]

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]
@app.route("/")
def beranda():
    return render_template('index.html')

# [Routing untuk API]    
@app.route("/api/deteksi", methods=['POST'])
def apiDeteksi():
    # Set nilai default untuk hasil prediksi dan gambar yang diprediksi
    hasil_prediksi = '(none)'
    gambar_prediksi = '(none)'
    rekomendasi_pria = '(none)'
    rekomendasi_wanita = '(none)'

    # Get File Gambar yg telah diupload pengguna
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    
    # Periksa apakah ada file yg dipilih untuk diupload
    if filename != '':
    
        # Set/mendapatkan extension dan path dari file yg diupload
        file_ext = os.path.splitext(filename)[1]
        gambar_prediksi = '/static/images/uploads/' + filename
        
        # Periksa apakah extension file yg diupload sesuai (jpg)
        if file_ext in app.config['UPLOAD_EXTENSIONS']:
            
            # Simpan Gambar
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            
            # Memuat Gambar
            test_image = Image.open('.' + gambar_prediksi)

            # Konversi gambar ke RGB jika memiliki 4 channel (RGBA)
            if test_image.mode == 'RGBA':
                test_image = test_image.convert('RGB')
            
            # Mengubah Ukuran Gambar (pastikan ukuran sesuai dengan input shape model)
            test_image_resized = test_image.resize((300, 400))
            
            # Konversi Gambar ke Array
            image_array = np.array(test_image_resized)
            test_image_x = (image_array / 255.0) - 0.5
            test_image_x = np.expand_dims(test_image_x, axis=0)
            
            # Prediksi Gambar
            y_pred_test_single = model.predict(test_image_x)
            y_pred_test_classes_single = np.argmax(y_pred_test_single, axis=1)
            
            hasil_prediksi = hair_classes[y_pred_test_classes_single[0]]

            if hasil_prediksi == "Curly Hair":
                rekomendasi_pria = "Curly Undercut, Curly Fringe, Afro"
                rekomendasi_wanita = "Curly Lob (Long Bob), Curly Shag, Tight Curls"
            elif hasil_prediksi == "Wavy Hair":
                rekomendasi_pria = "Short Textured Crop, Messy Quiff, Undercut with Waves"
                rekomendasi_wanita = "Beach Waves, Wavy Bob, Shaggy Layers"
            elif hasil_prediksi == "Straight Hair":
                rekomendasi_pria = "Slick Back, Side Part, Pompadour"
                rekomendasi_wanita = "Blunt Bob, Long Layers, Pixie Cut"
            
            # Return hasil prediksi dengan format JSON
            return jsonify({
                "prediksi": hasil_prediksi,
                "gambar_prediksi": gambar_prediksi,
                "rekomendasi_pria": rekomendasi_pria,
                "rekomendasi_wanita": rekomendasi_wanita
            })
        else:
            # Return hasil prediksi dengan format JSON
            gambar_prediksi = '(none)'
            return jsonify({
                "prediksi": hasil_prediksi,
                "gambar_prediksi": gambar_prediksi
            })

# =[Main]========================================        

if __name__ == '__main__':
    
    # Load model yang telah ditraining
    model = make_model()
    model.load_weights("HairWise.h5")

    # Run Flask di localhost S
    app.run(host="0.0.0.0", port=5000, debug=True)
