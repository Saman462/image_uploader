from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image, ImageEnhance, ImageOps
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    effect = request.form.get('effect')

    if file.filename == '':
        return redirect(url_for('index'))

    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = Image.open(filepath).convert("RGB")

    # Apply effect
    if effect == "grayscale":
        image = ImageOps.grayscale(image)
    elif effect == "invert":
        image = ImageOps.invert(image)
    elif effect == "enhance":
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(2.0)

    output_filename = f"styled_{filename}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    image.save(output_path)

    return render_template('results.html', filename=output_filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
