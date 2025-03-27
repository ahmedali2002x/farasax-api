import subprocess
import os
from flask import Flask, request, jsonify

# تحديد مسار Farasa
FARASA_JAR_PATH = r"C:\Users\ALNOUR\Desktop\STUDY 24\QCRI\Dev\ArabicNLP\Farasa\FarasaDiacritizeJar\dist\FarasaDiacritizeJar.jar"

# التأكد من أن الملف موجود
if not os.path.exists(FARASA_JAR_PATH):
    raise FileNotFoundError(f"Farasa JAR not found at {FARASA_JAR_PATH}")

# إنشاء Flask API
app = Flask(__name__)

@app.route('/diacritize', methods=['POST'])
def diacritize_text():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "يجب إرسال النص في JSON بصيغة {'text': 'النص'}"}), 400

    input_text = data["text"]

    input_file = "farasa_input.txt"
    output_file = "farasa_output.txt"

    with open(input_file, "w", encoding="utf-8") as f:
        f.write(input_text)

    command = [
        "java", "-jar", FARASA_JAR_PATH,
        "-i", input_file,
        "-o", output_file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            diacritized_text = f.read().strip()
        return jsonify({"original": input_text, "diacritized": diacritized_text})

    return jsonify({"error": "حدث خطأ أثناء تشغيل Farasa"}), 500

# تشغيل السيرفر
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
