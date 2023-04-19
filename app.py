from flask import Flask, render_template, request, redirect, url_for # Фреймворк для создания веб-приложений
import psycopg2 # Фрейворк для работы с базой данных Postgresql
import jinja2 # Шаблонизатор
import requests # Это модуль Python, который вы можете использовать для отправки всех видов HTTP-запросов
import json # Дает возможность работать с json файлами
from bs4 import BeautifulSoup # Это библиотека Python для извлечения данных из файлов HTML и XML

# Даем имя нашему приложения на Python с указанием папки с html файлами
app = Flask(__name__, template_folder='templates')

# Определение новой функции для подключения к базще данных
def get_connection():
    conn = psycopg2.connect( # Это строка кода, которая создает соединение с базой данных PostgreSQL с помощью библиотеки psycopg2
        dbname = "postgres", # Наименование БД
        user = "postgres", # Имя пользователя
        password = "1212", # Пароль от БД
        host = "localhost", # Хост БД
        port = "5432" # Порт БД
    )
    return conn # Это строка кода, которая возвращает объект conn, созданный функцией psycopg2.connect()

# Функция для получения списка сотрудников
def get_employees():
    conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
    cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
    cur.execute("SELECT * FROM employees ORDER BY employee_id ASC") # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur для отображения списка всех сотрудников
    rows = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
    conn.close() # Это строка кода, которая закрывает соединение с базой данных, которое было открыто с помощью метода connect() модуля psycopg2
    return rows # Это строка кода, которая возвращает объект rows

# Роут заказа
@app.route('/order', methods=['GET'])
def order(): # Функция для получения списка заказов
    if request.method == 'GET': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса GET-запросом
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        with conn.cursor() as cursor:
            query = f'SELECT * FROM orders ORDER BY order_id ASC' # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur для отображения списка всех заказов
            cur.execute(query) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            result = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
        if conn:
            conn.close() # Это метод, который закрывает соединение с базой данных
        return render_template('order.html', products=result) # Это строка кода, которая возвращает HTML-страницу пользователю
    else:
        pass # Пропуск if 
    return app.send_static_file('order.html') # Это строка кода, которая возвращает статический файл в ответ на запрос пользователя

# Функция для выполнения запросов в базу данных
def execute_query(query, params=None): # функция для упрощения работы с БД
    conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
    cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
    cur.execute(query, params) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
    conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    cur.close() # Это метод, который закрывает курсор, связанный с выполнением SQL-запросов в базу данных
    conn.close() #  Это строка кода, которая закрывает соединение с базой данных, которое было открыто с помощью метода connect() модуля psycopg2

# Добавление нового сотрудника
@app.route("/add", methods=["POST"]) #
def add_employee(): # Функция для добавления нвоых сотрудников
    if request.method == "POST": #Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        last_name = request.form["last_name"] # Это строка кода, которая получает значение поля last_name из HTML-формы, отправленной пользователем на сервер
        first_name = request.form["first_name"] # Это строка кода, которая получает значение поля first_name из HTML-формы, отправленной пользователем на сервер
        middle_name = request.form["middle_name"] # Это строка кода, которая получает значение поля middle_name из HTML-формы, отправленной пользователем на сервер
        position = request.form["position"] # Это строка кода, которая получает значение поля position из HTML-формы, отправленной пользователем на сервер
        address = request.form["address"] # Это строка кода, которая получает значение поля address из HTML-формы, отправленной пользователем на сервер
        phone = request.form["phone"] # Это строка кода, которая получает значение поля phone из HTML-формы, отправленной пользователем на сервер
        public_number = request.form["public_number"] # Это строка кода, которая получает значение поля public_number из HTML-формы, отправленной пользователем на сервер
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("INSERT INTO employees \
            (last_name, first_name, middle_name, position, address, phone, public_number)\
                VALUES (%s, %s, %s, %s, %s, %s, %s)", (last_name, first_name, middle_name, position, address, phone, public_number)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на добавление сотрудника
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return redirect(url_for('director')) # Это строка кода, которая выполняет перенаправление пользователя на другую страницу

# Роут обноваления сотрудников
@app.route("/update", methods=["POST"]) #
def update_employee(): # Функция для изменения данных сотрудников
    if request.method == "POST": # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        id = request.form["id"] # Это строка кода, которая получает значение поля id из HTML-формы, отправленной пользователем на сервер
        last_name = request.form["last_name"] # Это строка кода, которая получает значение поля last_name из HTML-формы, отправленной пользователем на сервер
        first_name = request.form["first_name"] # Это строка кода, которая получает значение поля first_name из HTML-формы, отправленной пользователем на сервер
        middle_name = request.form["middle_name"] # Это строка кода, которая получает значение поля middle_name из HTML-формы, отправленной пользователем на сервер
        position = request.form["position"] # Это строка кода, которая получает значение поля position из HTML-формы, отправленной пользователем на сервер
        address = request.form["address"] # Это строка кода, которая получает значение поля address из HTML-формы, отправленной пользователем на сервер
        phone = request.form["phone"] # Это строка кода, которая получает значение поля phone из HTML-формы, отправленной пользователем на сервер
        public_number = request.form["public_number"] # Это строка кода, которая получает значение поля public_number из HTML-формы, отправленной пользователем на сервер
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("UPDATE employees SET \
            last_name=%s, first_name=%s, middle_name=%s, position=%s, address=%s, phone=%s, public_number=%s \
            WHERE id=%s", (last_name, first_name, middle_name, position, address, phone, public_number, id)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на изменение записи в зависимости от id
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return redirect(url_for('director')) # Это строка кода, которая выполняет перенаправление пользователя на страницу директора

# Роут обновления сотрудников
@app.route("/update1", methods=["POST"]) #
def update_employee1(): # Функция для изменения данных сотрудников
    if request.method == "POST": # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        id = request.form["id"] # Это строка кода, которая получает значение поля id из HTML-формы, отправленной пользователем на сервер
        last_name = request.form["last_name"] # Это строка кода, которая получает значение поля last_name из HTML-формы, отправленной пользователем на сервер
        first_name = request.form["first_name"] # Это строка кода, которая получает значение поля first_name из HTML-формы, отправленной пользователем на сервер
        middle_name = request.form["middle_name"] # Это строка кода, которая получает значение поля middle_name из HTML-формы, отправленной пользователем на сервер
        position = request.form["position"] # Это строка кода, которая получает значение поля position из HTML-формы, отправленной пользователем на сервер
        address = request.form["address"] # Это строка кода, которая получает значение поля address из HTML-формы, отправленной пользователем на сервер
        phone = request.form["phone"] # Это строка кода, которая получает значение поля phone из HTML-формы, отправленной пользователем на сервер
        public_number = request.form["public_number"] # Это строка кода, которая получает значение поля public_number из HTML-формы, отправленной пользователем на сервер
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("UPDATE employees SET \
            last_name=%s, first_name=%s, middle_name=%s, position=%s, address=%s, phone=%s, public_number=%s \
            WHERE id=%s", (last_name, first_name, middle_name, position, address, phone, public_number, id)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на изменение записи в зависимости от id
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return redirect(url_for('deputydirector')) # Это строка кода, которая выполняет перенаправление пользователя на страницу заместителя директора

# Роут для удаления записи из базы данных
@app.route('/delete', methods=['GET', 'POST']) #
def delete(): # Функция для удаления сотрудников из списка
    if request.method == 'POST': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        id = request.form['id'] # Это строка кода, которая получает значение поля id из HTML-формы, отправленной пользователем на сервер
        execute_query('DELETE FROM employees WHERE id = %s', (id,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на удаление сотрудника в зависимости от его id
        return "Запись удалена" # Возвращает страницу с ответом об успешном удалении записи
    else:
        return redirect(url_for('delete')) # Это строка кода, которая выполняет перенаправление пользователя на страницу удаления

# Главная страница
@app.route('/') 
def index(): # Функция для определения стартовой страницы
    return render_template('index.html') # Это строка кода, которая возвращает HTML-страницу пользователю

# Поиск информации о клиенте 
@app.route('/search', methods=['POST']) # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
def search(): # Функция для поиска клиентов в списке
    client_name = request.form['name'] #
    conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
    cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
    cur.execute("SELECT * FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
    client = cur.fetchone() # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
    if client: #
        total_purchase = client[2] #
        current_balance = client[3] #
        credit_limit = client[4] #
        current_debt = client[5] #
        remaining_credit = credit_limit - current_debt #
        comment = client[7] #
        return render_template('search.html', client_name=client_name, total_purchase=total_purchase,
                               current_balance=current_balance, credit_limit=credit_limit,
                               current_debt=current_debt, remaining_credit=remaining_credit,
                               comment=comment) # Это строка кода, которая возвращает HTML-страницу пользователю с результатами поиска
    else:
        return render_template('search.html', name=client_name, error='Клиент не найден') # Это строка кода, которая возвращает HTML-страницу пользователю с ошибкой поиска

# Роут поиска
@app.route("/search")
def search_employee(): # Функция для поиска сотрудников 
    return render_template("search.html") # Это строка кода, которая возвращает HTML-страницу пользователю

# Роут создания заказа
@app.route('/create_order', methods=['GET', 'POST']) #
def new_order(): # Функция для добавления нового заказа
    conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
    cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
    cur.execute("SELECT client_name FROM clients ORDER BY client_id ASC") # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на отображение столбца с именами клиентов
    clients = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
    cur.execute("SELECT product_name FROM products ORDER BY product_id ASC") # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на отображение столбца с наименованиями товаров
    products = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
    if request.method == 'POST': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        client_name = request.form['client_name'] # Это строка кода, которая получает значение поля client_name из HTML-формы, отправленной пользователем на сервер
        product_name = request.form['product_name'] # Это строка кода, которая получает значение поля product_name из HTML-формы, отправленной пользователем на сервер
        sale_type = request.form['sale_type'] # Это строка кода, которая получает значение поля sale_type из HTML-формы, отправленной пользователем на сервер
        quantity = int(request.form['quantity']) # Это строка кода, которая получает значение поля quantity из HTML-формы, отправленной пользователем на сервер
        cur.execute("SELECT price FROM products WHERE product_name = %s", (product_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации о стоимости товара в зависимости от введенного наименования
        price = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT total_purchase FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации об общей сумме покупок в зависимости от введенного имени клиента
        total_purchase = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT current_balance FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации о балансе клиента в зависимости от введенного имени клиента
        current_balance = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT credit_limit FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации о кредитном лимите в зависимости от введенного имени клиента
        credit_limit = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT current_debt FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации о долге клиента в зависимости от введенного имени клиента
        current_debt = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT remaining_credit FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации об оставшемся кредите в зависимости от введенного имени клиента
        remaining_credit = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT comment FROM clients WHERE client_name = %s", (client_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод комментария о клиенте в зависимости от введенного имени клиента
        comment = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        cur.execute("SELECT product_quantity FROM products WHERE product_name = %s", (product_name,)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur на вывод информации о количесте товара в зависимости от наименования товара
        product_quantity = cur.fetchone()[0] # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        if sale_type == 'cash': # Способ оплаты наличка
            cur.execute("UPDATE clients SET total_purchase = %s WHERE client_name = %s", (total_purchase + price * quantity, client_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            cur.execute("UPDATE products SET product_quantity = %s WHERE product_name = %s", (product_quantity - quantity, product_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            total_price = price * quantity #
        elif sale_type == 'credit': # Способ оплаты кредит
            if current_balance + price * quantity > credit_limit * 0.9: #
                return 'You have reached your credit limit' #
            cur.execute("UPDATE clients SET total_purchase = %s, current_debt = %s, remaining_credit = %s WHERE client_name = %s", (total_purchase + price * quantity, current_debt * remaining_credit - price * quantity, credit_limit * 0.9 - (current_balance + price * quantity), client_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            cur.execute("UPDATE products SET quantity = %s WHERE product_name = %s", (product_quantity - quantity, product_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            total_price = price * quantity #
        elif sale_type == 'cashless':
            cur.execute("UPDATE clients SET total_purchase = %s WHERE client_name = %s", (total_purchase + price * quantity, client_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            cur.execute("UPDATE clients SET current_balance = %s WHERE client_name = %s", (current_balance - price * quantity, client_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            cur.execute("UPDATE products SET product_quantity = %s WHERE product_name = %s", (product_quantity - quantity, product_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            total_price = price * quantity
        elif sale_type == 'settlement': # Способ оплаты взаимозачет
            cur.execute("UPDATE clients SET total_purchase = %s, current_debt = %s, remaining_credit = %s WHERE client_name = %s", (total_purchase + price * quantity, current_debt - price * quantity, remaining_credit + price * quantity, client_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            cur.execute("UPDATE products SET product_quantity = %s WHERE product_name = %s", (product_quantity - quantity, product_name)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            total_price = price * quantity #
        else:
            return 'Invalid sale type' #
        cur.execute("INSERT INTO orders (client_name, product_name, sale_type, quantity, total_price) VALUES (%s, %s, %s, %s, %s)", (client_name, product_name, sale_type, quantity, total_price)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return render_template('create_order.html', clients=clients, products=products) # Это строка кода, которая возвращает HTML-страницу пользователю

@app.route('/create_barter_order', methods=['POST', 'GET'])
def create_barter_order():
    conn = get_connection()
    cur = conn.cursor()
    # Get form data
    client_name = request.form['client_name']
    product_in = request.form['product_in']
    quantity_in = request.form['quantity_in']
    price_in = get_product_price(product_in) * quantity_in
    product_out = request.form['product_out']
    quantity_out = request.form['quantity_out']
    price_out = get_product_price(product_out) * quantity_out
    # Calculate total price
    total_price = 0
    remains = 0
    if request.method == 'POST':
        if price_in == price_out:
            total_price = 0
        # Insert order into database
            cur.execute("INSERT INTO orders (client_name, product_name, sale_type, quantity, total_price) VALUES (%s, %s, %s, %s, %s)", (client_name, product_out, "barter", quantity_out, total_price))
            cur.execute("UPDATE products SET product_quantity = product_quantity + %s WHERE product_name = %s", (quantity_in, product_in))
            cur.execute("UPDATE products SET product_quantity = product_quantity - %s WHERE product_name = %s", (quantity_out, product_out))
            conn.commit()
            cur.close()
            return redirect(url_for('order'))
        elif price_in > price_out:
            total_price = 0
            remains = price_in - price_out
            cur.execute("UPDATE clients SET current_balance = current_balance + %s WHERE client_name = %s", (remains, client_name))
            cur.execute("INSERT INTO orders (client_name, product_name, sale_type, quantity, total_price) VALUES (%s, %s, %s, %s, %s)", (client_name, product_out, "barter", quantity_out, total_price))
            cur.execute("UPDATE products SET product_quantity = product_quantity + %s WHERE product_name = %s", (quantity_in, product_in))
            cur.execute("UPDATE products SET product_quantity = product_quantity - %s WHERE product_name = %s", (quantity_out, product_out))
            conn.commit()
            cur.close()
            return redirect(url_for('order'))
        elif price_in < price_out:
            remains = price_out - price_in
            cur.execute("UPDATE clients SET total_purchase = total_purchase - %s WHERE client_name = %s", (remains, client_name))
            cur.execute("INSERT INTO orders (client_name, product_name, sale_type, quantity, total_price) VALUES (%s, %s, %s, %s, %s)", (client_name, product_out, "barter", quantity_out, remains))
            cur.execute("UPDATE products SET product_quantity = product_quantity + %s WHERE product_name = %s", (quantity_in, product_in))
            cur.execute("UPDATE products SET product_quantity = product_quantity - %s WHERE product_name = %s", (quantity_out, product_out))
            conn.commit()
            cur.close()
            return redirect(url_for('order'))
        else:
            return "Error: Products are not equal in price"
        
    else:
        return redirect(url_for('order'))

# Helper function to get product price
def get_product_price(product_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT price FROM products WHERE product_name = %s", (product_name,))
    price = cur.fetchone()[0]
    cur.close()
    return price

# Роут товара
@app.route('/products', methods=['POST', 'GET']) #
def products(): # Функция для получения списка товаров
    if request.method == 'GET': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса GET-запросом
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        with conn.cursor() as cursor: #
            query = f'SELECT * FROM products ORDER BY product_id ASC' #
            cur.execute(query) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            result = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
        if conn: #
            conn.close() # Это строка кода, которая закрывает соединение с базой данных, которое было открыто с помощью метода connect() модуля psycopg2
        return render_template('products.html', products=result) # Это строка кода, которая возвращает HTML-страницу пользователю
    else:
        pass # Пропуск if
    return app.send_static_file('products.html') # Это строка кода, которая возвращает статический файл в ответ на запрос пользователя

# Роут доабвления товара
@app.route("/add_p", methods=["POST"]) 
def add_p(): # Функция для добавления товаров
    if request.method == "POST": # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        name = request.form["name"] # Это строка кода, которая получает значение поля name из HTML-формы, отправленной пользователем на сервер
        price = request.form["price"] # Это строка кода, которая получает значение поля price из HTML-формы, отправленной пользователем на сервер
        quantity = request.form["quantity"] # Это строка кода, которая получает значение поля quantity из HTML-формы, отправленной пользователем на сервер
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("INSERT INTO products (product_name, price, product_quantity) VALUES (%s, %s, %s)", (name, price, quantity)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return redirect(url_for('products')) # Это строка кода, которая выполняет перенаправление пользователя на страницу продуктов

# Роут изменения количества товара
@app.route("/update_quantity/<int:product_id>", methods=["POST"]) #
def update_quantity(product_id): # Функция для изменения количества товаров на складе
    if request.method == "POST": # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        quantity_change = int(request.form['quantity_change']) # Преобразует полученное значение в целочисленный тип данных
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("UPDATE products SET product_quantity = product_quantity + %s WHERE product_id = %s", (quantity_change, product_id)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return redirect(url_for('products')) # Это строка кода, которая выполняет перенаправление пользователя на страницу продуктов

@app.route("/update_price/<int:product_id>", methods=["POST"]) #
def update_price(product_id): # Функция для изменения количества товаров на складе
    if request.method == "POST": # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        price_change = int(request.form['price_change']) # Преобразует полученное значение в целочисленный тип данных
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("UPDATE products SET price = %s WHERE product_id = %s", (price_change, product_id)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
        conn.commit() # Это метод, который подтверждает транзакцию и применяет изменения, внесенные в базу данных
    return redirect(url_for('products')) # Это строка кода, которая выполняет перенаправление пользователя на страницу продуктов

# Роут логина
@app.route('/login', methods=['GET', 'POST']) #
def login(): # Функция для добавления возможности входа по логину и паролю
    if request.method == 'POST': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса POST-запросом
        username = request.form['username'] # Это строка кода, которая получает значение поля username из HTML-формы, отправленной пользователем на сервер
        password = request.form['password'] # Это строка кода, которая получает значение поля password из HTML-формы, отправленной пользователем на сервер
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        with conn.cursor() as cursor: # Это строка кода, которая создает курсор для выполнения операций с базой данных
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'" #
            cursor.execute(query) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            result = cursor.fetchone() # Это строка кода, которая получает одну строку, которая была выбрана в результате выполнения SQL-запроса, с помощью курсора cur
        if conn: #
            conn.close() # Это строка кода, которая закрывает соединение с базой данных, которое было открыто с помощью метода connect() модуля psycopg2
        if result: #
            if result[1] == 'director': # Это начало условной конструкции, которая проверяет, равняется ли второй элемент кортежа result значению director
                return redirect('/director') # Это строка кода, которая выполняет перенаправление пользователя на страницу директора
            elif result[1] == 'deputydirector': # Это начало условной конструкции, которая проверяет, равняется ли второй элемент кортежа result значению deputydirector
                return redirect('/deputydirector') # Это строка кода, которая выполняет перенаправление пользователя на страницу заместителя директора
            elif result[1] == 'secretary': # Это начало условной конструкции, которая проверяет, равняется ли второй элемент кортежа result значению secretary
                return redirect('/secretary') # Это строка кода, которая выполняет перенаправление пользователя на страницу секретаря
            elif result[1] == 'guest': # Это начало условной конструкции, которая проверяет, равняется ли второй элемент кортежа result значению guest
                return redirect('/guest') # Это строка кода, которая выполняет перенаправление пользователя на страницу гостя
            else:
                return redirect('/login') # Это строка кода, которая выполняет перенаправление пользователя на страницу логина
        else:
            return redirect('/login') # Это строка кода, которая выполняет перенаправление пользователя на страницу логина
    else:
        return render_template('login.html') # Это строка кода, которая возвращает HTML-страницу пользователю

# Роут директора
@app.route('/director', methods=['GET', 'POST']) #
def director(): # Функция для добавления прав директора
    if request.method == 'GET': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса GET-запросом
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        with conn.cursor() as cursor: #
            query = f'SELECT * FROM employees ORDER BY id ASC' #
            cur.execute(query) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            result = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
        if conn: #
            conn.close() # Это строка кода, которая закрывает соединение с базой данных, которое было открыто с помощью метода connect() модуля psycopg2
        return render_template('director.html', employees=result) # Это строка кода, которая возвращает HTML-страницу пользователю
    else: #
        id = request.form["id"] # Это строка кода, которая получает значение поля id из HTML-формы, отправленной пользователем на сервер
        last_name = request.form["last_name"] # Это строка кода, которая получает значение поля last_name из HTML-формы, отправленной пользователем на сервер
        first_name = request.form["first_name"] # Это строка кода, которая получает значение поля first_name из HTML-формы, отправленной пользователем на сервер
        middle_name = request.form["middle_name"] # Это строка кода, которая получает значение поля middle_name из HTML-формы, отправленной пользователем на сервер
        position = request.form["position"] # Это строка кода, которая получает значение поля position из HTML-формы, отправленной пользователем на сервер
        address = request.form["address"] # Это строка кода, которая получает значение поля address из HTML-формы, отправленной пользователем на сервер
        phone = request.form["phone"] # Это строка кода, которая получает значение поля phone из HTML-формы, отправленной пользователем на сервер
        public_number = request.form["public_number"] # Это строка кода, которая получает значение поля public_number из HTML-формы, отправленной пользователем на сервер
        print(id, last_name, first_name, middle_name, position, address, phone, public_number) #
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("INSERT INTO employees \
            (last_name, first_name, middle_name, position, address, phone)\
                VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, last_name, first_name, middle_name, position, address, phone, public_number)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
    return app.send_static_file('director.html') # Это строка кода, которая возвращает статический файл в ответ на запрос пользователя

# Роут заместителя директора
@app.route('/deputydirector', methods=['GET', 'POST']) #
def deputy_director(): # Фукнция для добавления прав заместителя директора
    if request.method == 'GET': # Это условный оператор в языке программирования Python, который проверяет, является ли метод HTTP-запроса GET-запросом
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        with conn.cursor() as cursor: #
            query = f'SELECT * FROM employees ORDER BY id ASC' #
            cur.execute(query) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
            result = cur.fetchall() # Это строка кода, которая получает все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
        if conn: #
            conn.close() # Это строка кода, которая закрывает соединение с базой данных, которое было открыто с помощью метода connect() модуля psycopg2
        return render_template('deputydirector.html', employees=result) # Это строка кода, которая возвращает HTML-страницу пользователю
    else: #
        id = request.form["id"] # Это строка кода, которая получает значение поля id из HTML-формы, отправленной пользователем на сервер
        last_name = request.form["last_name"] # Это строка кода, которая получает значение поля last_name из HTML-формы, отправленной пользователем на сервер
        first_name = request.form["first_name"] # Это строка кода, которая получает значение поля first_name из HTML-формы, отправленной пользователем на сервер
        middle_name = request.form["middle_name"] # Это строка кода, которая получает значение поля middle_name из HTML-формы, отправленной пользователем на сервер
        position = request.form["position"] # Это строка кода, которая получает значение поля position из HTML-формы, отправленной пользователем на сервер
        address = request.form["address"] # Это строка кода, которая получает значение поля address из HTML-формы, отправленной пользователем на сервер
        phone = request.form["phone"] # Это строка кода, которая получает значение поля phone из HTML-формы, отправленной пользователем на сервер
        public_number = request.form["public_number"] # Это строка кода, которая получает значение поля public_number из HTML-формы, отправленной пользователем на сервер
        print(id, last_name, first_name, middle_name, position, address, phone, public_number) #
        conn = get_connection() # Это строка кода, которая вызывает функцию get_connection() и сохраняет возвращаемый ей объект conn в переменной с именем conn
        cur = conn.cursor() # Это строка кода, которая создает курсор для выполнения операций с базой данных
        cur.execute("INSERT INTO employees \
            (last_name, first_name, middle_name, position, address, phone)\
                VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, last_name, first_name, middle_name, position, address, phone, public_number)) # Это строка кода, которая выполняет SQL-запрос к базе данных с помощью курсора cur
    return app.send_static_file('deputydirector.html') # Это строка кода, которая возвращает статический файл в ответ на запрос пользователя

# Роут секретаря
@app.route('/secretary', methods=['GET', 'POST']) #
def secretary(): # Функция для добавления прав гостя
    if request.method == 'GET': # Проверяем, является ли метод HTTP-запроса GET-запросом
        conn = get_connection() # Получаем соединение с базой данных и сохраняем его в переменной conn
        cur = conn.cursor() # Создаем курсор для выполнения операций с базой данных
        with conn.cursor() as cursor: # Создаем контекстный менеджер с курсором для выполнения SQL-запросов
            query = f'SELECT * FROM employees ORDER BY id ASC' # Формируем SQL-запрос для получения всех записей из таблицы employees и сортировки их по id
            cur.execute(query) # Выполняем SQL-запрос к базе данных с помощью курсора cur
            result = cur.fetchall() # Получаем все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
        if conn: # Если было создано соединение с базой данных
            conn.close() # Закрываем соединение с базой данных, которое было открыто с помощью метода get_connection()
    return render_template('secretary.html', employees=result) # Возвращаем HTML-страницу с результатами SQL-запроса, чтобы отобразить их пользователю

# Роут гостя
app.route('/guest', methods=['GET', 'POST']) #
def guest(): # Функция для добавления прав гостя
    if request.method == 'GET': # Проверяем, является ли метод HTTP-запроса GET-запросом
        conn = get_connection() # Получаем соединение с базой данных и сохраняем его в переменной conn
        cur = conn.cursor() # Создаем курсор для выполнения операций с базой данных
        with conn.cursor() as cursor: # Создаем контекстный менеджер с курсором для выполнения SQL-запросов
            query = f'SELECT * FROM employees ORDER BY id ASC' # Формируем SQL-запрос для получения всех записей из таблицы employees и сортировки их по id
            cur.execute(query) # Выполняем SQL-запрос к базе данных с помощью курсора cur
            result = cur.fetchall() # Получаем все строки, которые были выбраны в результате выполнения SQL-запроса, с помощью курсора cur
        if conn: # Если было создано соединение с базой данных
            conn.close() # Закрываем соединение с базой данных, которое было открыто с помощью метода get_connection()
    return render_template('guest.html', employees=result) # Возвращаем HTML-страницу с результатами SQL-запроса, чтобы отобразить их пользователю

# Роут парсинг API
@app.route('/realtime') #
def realtime(): # Определение функции с именем realtime
    url = "https://openexchangerates.org/api/latest.json?app_id=4beefb5c1ae146168f09d5ffb90360e6&symbols=RUB,EUR,JPY,GBP,CAD,CHF,AUD,CNY,HKD,SEK" # Указание ссылки на API, которую мы будем парсить
    response = requests.get(url) # Выполнение GET-запроса по указанному url-адресу и сохранение ответа в переменной response
    data = response.json() # Получение данных из ответа в формате JSON и сохранение их в переменной data
    return render_template('realtime.html', rates=data['rates']) # Возврат HTML-страницы, которая использует шаблон 'realtime.html' и передает в него данные из словаря 'rates', которые были получены из ответа API

# Роут парсинг url
@app.route('/currency') 
def currency():  # Объявление функции currency
    url = 'https://www.cbr.ru/currency_base/daily/'  # URL-адрес для получения данных о курсах валют
    response = requests.get(url)  # Отправка HTTP-запроса на получение данных по указанному URL-адресу
    soup = BeautifulSoup(response.content, 'html.parser')  # Создание объекта BeautifulSoup для парсинга HTML-кода страницы
    table = soup.find('table', attrs={'class': 'data'})  # Нахождение таблицы на странице, содержащей информацию о курсах валют
    rows = table.find_all('tr')  # Получение всех строк таблицы
    result = ''  # Объявление пустой строки для хранения результатов парсинга таблицы
    for row in rows:  # Итерация по строкам таблицы
        cols = row.find_all('td')  # Получение всех столбцов в текущей строке
        cols = [ele.text.strip() for ele in cols]  # Очистка содержимого ячеек от лишних пробелов и переносов строк
        result += '<tr><td>' + '</td><td>'.join(cols) + '</td></tr>'  # Формирование строки HTML-кода для текущей строки таблицы
    return '<table border="1">' + result + '</table>'  # Возврат результата в виде HTML-кода таблицы

if __name__ == '__main__': # Запуск приложения
    app.run(debug=True) # Запуск приложения с debug-menu