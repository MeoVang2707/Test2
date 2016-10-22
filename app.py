from flask import *
from mongoengine import *
from os import *
from werkzeug.utils import secure_filename

# @ds053126.mlab.com:53126/hoang
db_name = "hoang"
host = "ds053126.mlab.com"
port = 53126
user_name = "hoang"
password = "0986369617"

connect(db_name,
        host=host,
        port=port,
        username = user_name,
        password = password)

APP_ROOT = path.dirname(path.abspath(__file__))
UPLOADS_IMAGE = path.join(APP_ROOT, "static/image")

app = Flask(__name__)
app.config["UPLOADS_IMAGE"] = UPLOADS_IMAGE
app.config["SECRET_KEY"] = "ahihi. do's ngok's."


# class Product(Document):
#     Name = StringField()
#     Price = IntField()
#     Image = StringField()

class Person(Document):
    Name = StringField()
    Password = StringField()
    Contact = StringField()
    Product = ListField()

Test = {}
user_fail = {"Name": "ahihi do's ngok's"}


@app.route('/profile/<name>', methods=["get","post"])
def profile(name):
    if "loggedin" in session and session["loggedin"]:
        for key in Person.objects:
            if name == key.Name:
                user = key
                break
        if user_fail["Name"] == name:
            if request.method == "GET":
                return render_template("profile.html", user = user)
            elif request.method == "POST":
                Name = request.form["name"]
                Price = request.form["price"]
                Image = request.files["image"]
                if Image is not None:
                    filename = secure_filename(Image.filename)
                    Image_link_real = path.join(UPLOADS_IMAGE, filename)
                    Image.save(Image_link_real)
                    Image_link_fake = "../static/image/" + filename
                    Test["Name"] = Name
                    Test["Price"] = Price
                    Test["Image"] = Image_link_fake
                    user.Product.append(Test)
                    user.save()
                    # for key in Person.objects:
                        # key.Product.append(Test)
                        # key.save()
                    return render_template("profile.html", user = user)
        else:
            return render_template("profile_guest.html", user = user, name = user_fail["Name"])
    else:
        return redirect(url_for("login"))

# @app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form["usrname"]
        password = request.form["psw"]
        for key in Person.objects:
            if username == key.Name and password == key.Password:
                session["loggedin"] = True
                user = key
                break
            else:
                session["loggedin"] = False
        if session["loggedin"]:
            user_fail["Name"] = key.Name
            # user_fail["Contact"] = key.Contact
            # user_fail["Product_name"] = key.Name
            return redirect(url_for("profile", name=user.Name))
        else:
            return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session["loggedin"] = False
    return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        contact = request.form["contact"]
        print(username)
        print(password)
        print(contact)
        for key in Person.objects:
            if username == key.Name:
                session["loggedin"] = False
                break
            else:
                session["loggedin"] = True
        if session["loggedin"]:
            user = Person(Name = username, Password =password, Contact = contact, Product = [])
            user.save()
            user_fail["Name"] = user.Name
            return redirect(url_for("profile", name = username))
        else:
            return redirect(url_for("register"))

# Search = []
@app.route('/')
@app.route('/Home_page', methods=["GET", "POST"])
def home_page2():
    if request.method == "GET":
        return render_template("home_page2.html", user_list = Person.objects)
    if request.method == "POST":
        search_key_0 = request.form["search"]
        search_key = search_key_0.upper()
        search_list = search_key.split()
        for key_search in search_list:
            for person in Person.objects:
                for product in person.Product:
                    # print(product['Name'])
                    product_list_0 = product['Name'].upper()
                    product_list = product_list_0.split()
                    for key_product in product_list:
                        if key_product == key_search:
                            Test["user"] = person.Name
                            Test["contact"] = person.Contact
                            Test["product_name"] = product['Name']
                            Test["product_price"] = product['Price']
                            Test["product_image"] = product['Image']
                            if Test in Search:
                                Search_result = False
                            else:
                                Search_result = True
                            if Search_result:
                                Search.append(Test)
        return render_template("search2.html", search_list = Search, search_key = search_key_0)

@app.route('/Home_page/<name>', methods=["GET", "POST"])
def home_page(name):
    name_user = name
    if "loggedin" in session and session["loggedin"]:
        if user_fail["Name"] == name:
            if request.method == "GET":
                return render_template("home_page_name.html", user_list = Person.objects, name = name_user)
            elif request.method == "POST":
                search_key_0 = request.form["search"]
                search_key = search_key_0.upper()
                search_list = search_key.split()
                Search = []
                for key_search in search_list:
                    for person in Person.objects:
                        for product in person.Product:
                            # print(product['Name'])
                            product_list_0 = product['Name'].upper()
                            product_list = product_list_0.split()
                            for key_product in product_list:
                                Search_list = {}
                                if key_product == key_search:
                                    Search_list["user"] = person.Name
                                    Search_list["contact"] = person.Contact
                                    Search_list["product_name"] = product['Name']
                                    Search_list["product_price"] = product['Price']
                                    Search_list["product_image"] = product['Image']
                                    if Search_list in Search:
                                        Search_result = False
                                    else:
                                        Search_result = True
                                    if Search_result:
                                        Search.append(Search_list)
                return render_template("search.html", search_list = Search, search_key=search_key_0, name = name_user)
        else:
            if request.method == "GET":
                return render_template("home_page_name_guest.html", user_list = Person.objects, name = user_fail["Name"])
            elif request.method == "POST":
                search_key_0 = request.form["search"]
                search_key = search_key_0.upper()
                search_list = search_key.split()
                Search = []
                for key_search in search_list:
                    for person in Person.objects:
                        for product in person.Product:
                            # print(product['Name'])
                            product_list_0 = product['Name'].upper()
                            product_list = product_list_0.split()
                            for key_product in product_list:
                                Search_list = {}
                                if key_product == key_search:
                                    Search_list["user"] = person.Name
                                    Search_list["contact"] = person.Contact
                                    Search_list["product_name"] = product['Name']
                                    Search_list["product_price"] = product['Price']
                                    Search_list["product_image"] = product['Image']
                                    if Search_list in Search:
                                        Search_result = False
                                    else:
                                        Search_result = True
                                    if Search_result:
                                        Search.append(Search_list)
                return render_template("search.html", search_list = Search, search_key=search_key_0, name = user_fail["Name"])
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run()
