import os
from analyzer import count_people
from flask import Flask, flash, request, redirect, url_for, render_template
# объясняется ниже
from werkzeug.utils import secure_filename


# папка для сохранения загруженных файлов
UPLOAD_FOLDER = 'files/'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# создаем экземпляр приложения
app = Flask(__name__)
# конфигурируем
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/s', methods=["GET"])
def s():
    count = count_people()
    return render_template("result.html", css = url_for('static', filename = 'result-styles.css'), path = url_for('static', filename = 'result.jpg'), count = count)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю 
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            # сохраняем файл
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "1.jpg"))
            # если все прошло успешно, то перенаправляем  
            # на функцию-представление `download_file` 
            # для скачивания файла
            return redirect(url_for('s', name = filename))
    return render_template("index.html", css = url_for('static', filename = 'styles.css'))


if __name__ == '__main__':
    app.run()