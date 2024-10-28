<h1>Установка</h1>
Создаем окружение: <code>python -m venv venv</code><br>
Устанавливаем библиотеки: <code>pip install -r requirements.txt</code><br>
Создаем файлик с переменными окружения (.env) в корневом каталоге:<br>
<code>SECRET_KEY="super secret key"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="comsoftlab"
DB_USER=""
DB_USER_PASSWORD=""
DEBUG="TRUE"
REDIS_HOST="127.0.0.1"
REDIS_PORT="6379"
</code><br>
Создаем базу данных в PostgreSQL(comsoftlab)<br>
Проводим миграции <code>python manage.py migrate</code><br>
Создаем пользователя <code>python manage.py createuser "email" "password"</code><br>
Запускаем сервер <code>python manage.py runserver</code>

<h1>Пояснения</h1>
Тестировал на mail.ru почте с целью упрощения, т.к. в том же gmail нужна реализация подключения через OAuth2, в целом класс EmailClient подготовлен к масштабированию(для других почт).<br>
По пути <code>/api/docs</code> сделал документацию(swagger) для единственного запроса.<br>

