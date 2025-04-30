import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = "received_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML в стиле Apple AirDrop с анимацией
HTML_FORM = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AirDrop для ПК</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #000;
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            opacity: 0;
            animation: fadeIn 1s ease-in-out forwards;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        h2 {
            font-size: 24px;
            font-weight: 600;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(255, 255, 255, 0.1);
        }
        .upload-label {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100px;
            height: 100px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            cursor: pointer;
            transition: background 0.3s ease-in-out;
            animation: pulse 1.5s infinite ease-in-out;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .upload-label:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        .upload-label img {
            width: 50px;
            height: 50px;
        }
        input[type="file"] {
            display: none;
        }
        .status {
            font-size: 18px;
            font-weight: 500;
            opacity: 0.8;
            transition: opacity 0.3s ease-in-out;
        }
        .back-btn {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            text-decoration: none;
            font-size: 18px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 5px;
            opacity: 0.8;
            transition: opacity 0.3s ease-in-out;
        }
        .back-btn:hover {
            opacity: 1;
        }
        .back-btn::before {
            content: "←";
            font-size: 20px;
        }
    </style>
</head>
<body>
    <a href="/" class="back-btn">Назад</a>
    <h2>AirDrop для ПК</h2>
    <div class="container">
        <label for="file-upload" class="upload-label">
            <img src="https://cdn-icons-png.flaticon.com/512/60/60775.png" alt="Upload">
        </label>
        <form action="/upload" method="post" enctype="multipart/form-data" id="upload-form">
            <input type="file" name="file" id="file-upload" required>
        </form>
        <p class="status">Выберите файл для отправки</p>
    </div>

    <script>
        document.getElementById("file-upload").addEventListener("change", function() {
            document.querySelector(".status").innerText = "📤 Отправка файла...";
            document.querySelector(".upload-label").style.animation = "none";
            document.getElementById("upload-form").submit();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_FORM)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return f"""
        <h2 style='color: white;'>✅ Файл {file.filename} загружен!</h2>
        <a href='/' class='back-btn'>Назад</a>
        """, 200
    return "Ошибка загрузки", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)