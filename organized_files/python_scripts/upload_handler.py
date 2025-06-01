
import os
from flask import Flask, request, render_template, redirect, url_for
import shutil

app = Flask(__name__)

# สร้างโฟลเดอร์ uploads ถ้ายังไม่มี
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        
        # รัน session extractor
        os.system("python session_extractor.py")
        
        return "อัพโหลดไฟล์และค้นหา session ID แล้ว! <a href='/'>กลับไปหน้าหลัก</a>"

@app.route('/capture', methods=['POST'])
def capture_text():
    text = request.form['text']
    
    # บันทึกข้อความลงในไฟล์
    with open("uploads/captured_text.txt", "w") as f:
        f.write(text)
    
    # รัน session extractor
    os.system("python session_extractor.py")
    
    return "บันทึกข้อความและค้นหา session ID แล้ว! <a href='/'>กลับไปหน้าหลัก</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
