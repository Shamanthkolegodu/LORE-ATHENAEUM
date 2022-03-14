# run: python3 back.py

from flask import Flask, render_template, request, redirect, Response, json, render_template, url_for
import psycopg2
import datetime


app = Flask(__name__)

conn = None
cur = None
user = None
password = None
user_id_g = None


@app.route('/')
def main():
    print("hello world")
    return render_template('index.html')

@app.route('/home/<id>')
def home(id):
    return render_template('home.html',data={'id':id})

@app.route('/login', methods=['POST'])
def login():
    global conn
    global cur
    global user
    global user_id_g
    global password
    if(conn is not None):
        conn.close()
    if(cur is not None):
        cur.close()

    books_record = None
    username = request.form.get("user")
    user = username
    password = request.form.get("password")
    try:
        print(username, "'"+str(password)+"'")
        conn = psycopg2.connect(
            dbname="ebooks", user=username, password=password, host="my_db",port="5432")
        cur = conn.cursor()
        
        query_user = "select userid from "+username+"_user"
        cur.execute(query_user)
        id = cur.fetchone()
        id = int(str(id)[1:-2])
        user_id_g = id
        print(id)
        print(books_record)
    except Exception as ex:
        print(ex)
        return render_template('error.html', data={"message": "You are not authorized to access the database"})

    return render_template('home.html', data={'username': username, 'id': id, 'items': books_record})

@app.route('/all_books/<id>', methods=['POST', 'GET'])
def all_books(id):
    query = "select b.*,g.genre from book_catalogue as b,book_catalogue_genre as g where b.isbn=g.isbn order by b.isbn"
    cur.execute(query)
    books_record = cur.fetchall()
    return render_template('books.html', data={'id': id, 'items': books_record,'username':user})

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    '''
    Input for postman
    {   
    "firstname":"skm",
    "lastname":"skm",
    "user_name":"skm",
    "email_id":"abc@gmail.com",
    "ph_no":"1111111111",
    "dob":"2001-01-01",
    "password":"123",
    "card_upi":"123",
    "store_id":"1"
    }
    '''
    if request.method == 'POST':
        data = request.json
        insert_commd_autom = "INSERT INTO user_details (userid,firstname,lastname,user_name,email_id,ph_no,dob,password,card,store_id) VALUES ((SELECT MAX(userid)+1 FROM user_details),"

        key_val_insert = list(data.values())
        key_val_insert = ["'"+i+"'" for i in key_val_insert]
        final_val_insert = ','.join(key_val_insert)
        final_insert_commd_autom = insert_commd_autom + final_val_insert + ")"
        print(final_insert_commd_autom)
        cur.execute(final_insert_commd_autom)
        conn.commit()
        return render_template('data.html', data=data)


@app.route('/add_to_cart/<isbn>', methods=['POST', 'GET'])
def add_to_cart(isbn):
    '''
    {   
        "userid":"1",
        "isbn":"2",
        "cart_id":"1"
    }
    '''
    get_all_cart = "select * from cart"
    cur.execute(get_all_cart)
    all_in_cart = cur.fetchall()
    print(all_in_cart)
    get_all_cart = "select * from library"
    cur.execute(get_all_cart)
    all_in_library = cur.fetchall()
    print(all_in_library)
    book=(user_id_g,str(isbn),str(user_id_g))
    print(book)
    if(book not in all_in_cart  and book not in all_in_library):
        insert_commd_autom = "INSERT INTO cart (userid,isbn,cart_id) VALUES ("+str(user_id_g)+",'"+str(isbn)+"','"+str(user_id_g)+"')"
        print(insert_commd_autom)
        cur.execute(insert_commd_autom)
        conn.commit()
        return render_template('data.html', data={'message':"Added to cart","id":user_id_g})
    elif (book in all_in_cart  and book not in all_in_library):
               return render_template('data.html', data={'message':"Book already exists in cart","id":user_id_g}) 
    else:
        return render_template('data.html', data={'message':"Book already exists in library","id":user_id_g})



@app.route('/add_to_wishlist/<isbn>', methods=['POST', 'GET'])
def add_to_wishlist(isbn):
    '''
    {   
        "userid":"1",
        "isbn":"2",
        "lib_id":"1"
    }
    '''
    get_all_wishlist = "select * from wishlist"
    cur.execute(get_all_wishlist)
    get_all_wishlist = cur.fetchall()

    get_all_lib = "select * from library"
    cur.execute(get_all_lib)
    all_in_library = cur.fetchall()


    book=(user_id_g,str(isbn),str(user_id_g))
    print(book)
    if((book not in get_all_wishlist ) and (book not in all_in_library)):
        insert_commd_autom = "INSERT INTO wishlist (userid,isbn,wishlist_id) VALUES ("+str(user_id_g)+",'"+str(isbn)+"','"+str(user_id_g)+"')"
        cur.execute(insert_commd_autom)
        conn.commit()
        return render_template('data.html', data={'message':"Added to wishlist","id":user_id_g})
    elif (book in get_all_wishlist  and book not in all_in_library):
               return render_template('data.html', data={'message':"Book already exists in wishlist","id":user_id_g}) 
    else:
        return render_template('data.html', data={'message':"Book already exists in library","id":user_id_g})


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    '''
    {   
        "transaction_id":"2",
        "price":"1",
        "date_time":"2020-10-19 10:23:54",
        "userid":"1"
    }
    '''

    get_all_cart = "select * from cart"
    cur.execute(get_all_cart)
    all_in_cart = cur.fetchall()
    # print(all_in_cart)
    get_all_cart = "select * from library"
    cur.execute(get_all_cart)
    all_in_library = cur.fetchall()
    # print(all_in_library)

    get_all_wishlist = "select * from wishlist"
    cur.execute(get_all_wishlist)
    get_all_wishlist = cur.fetchall()
    # print(get_all_wishlist)
    
    for item in all_in_cart:
        if item in get_all_wishlist:
            query='Delete from wishlist where userid='+str(user_id_g)+" and isbn='"+str(item[1])+"'"
            cur.execute(query)
            conn.commit()
            print("====")

    date_time=datetime.datetime.now()
    # print(1)

    for item in all_in_cart:
        if item not in all_in_library:
            query_book = "select * from book_catalogue where isbn='"+str(item[1])+"'"
            cur.execute(query_book)
            book= cur.fetchall()
            
            try:
                query_sales="select * from sales"
                cur.execute(query_sales)
                sales = cur.fetchall()
                inse=0
                for i in sales:
                    if str(item[1])==i[2]:
                        inse=1
                        break;
                if(inse==0):
                    query_book_sales = "insert into sales values ((SELECT MAX(sales_id)+1 FROM sales),1,'"+str(item[1])+"','1')"
                    cur.execute(query_book_sales)
                    conn.commit()
                else:
                    query_book_sales = "update sales set no_copies_sold= no_copies_sold+1 where isbn='"+str(item[1])+"'"
                    cur.execute(query_book_sales)
                    conn.commit()
            except Exception as e:
                print(e)
    
            # print(2)
            insert_query = "INSERT INTO library (userid,isbn,lib_id) VALUES ("+str(item[0])+","+str(item[1])+","+str(item[2])+")"
            cur.execute(insert_query)
            conn.commit()
            # print(insert_query)
            insert_payment_query="insert into payment (order_id,transaction_id,price,date_time,userid) values((SELECT MAX(order_id)+1 FROM payment),(SELECT MAX(transaction_id)+1 FROM payment),'"+str(book[0][3])+"','"+str(date_time)+"','"+str(user_id_g)+"')"
            # print(insert_payment_query)
            cur.execute(insert_payment_query)
            conn.commit()

    truncate_cart = "truncate cart"
    cur.execute(truncate_cart)
    conn.commit()    
    return render_template('data.html', data={'message':"payment sucessful","id":user_id_g})


@app.route('/lib_view', methods=['POST', 'GET'])
def lib_view():
    query = "select * from library"
    cur.execute(query)
    library_record = cur.fetchall()
    a = {'data': library_record}
    print(a)

    return render_template('data.html', data=["SUCESS"])
    # status=200
    # return Response(response=json.dumps({"data": books_record}), status=status, mimetype="application/json")


@app.route('/cart/<id>', methods=['POST', 'GET'])
def cart(id):
    query = "select * from cart where userid='"+str(id)+"'"
    cur.execute(query)
    cart_details = cur.fetchall()
    books = []
    for i in cart_details:
        # print(i)
        query2 = "select * from book_catalogue where isbn='"+str(i[1])+"'"
        cur.execute(query2)
        book = cur.fetchall()
        books.append(book[0])
    # print(books)
    return render_template('cart.html', data={'id': id, 'cart_data': books})


@app.route('/library/<id>', methods=['POST', 'GET'])
def library(id):
    query = "select * from library where userid='"+str(id)+"' order by isbn"
    cur.execute(query)
    cart_details = cur.fetchall()
    books = []
    for i in cart_details:
        print(i)
        query2 = "select * from book_catalogue where isbn='"+str(i[1])+"'"
        cur.execute(query2)
        book = cur.fetchall()
        books.append(book[0])
    print(books)
    return render_template('library.html', data={'id': id, 'lib_data': books})

@app.route('/wishlist/<id>', methods=['POST', 'GET'])
def wishlist(id):
    
    query = "select * from wishlist where userid='"+str(id)+"'"
    cur.execute(query)
    cart_details = cur.fetchall()
    books = []
    for i in cart_details:
        print(i)
        query2 = "select * from book_catalogue where isbn='"+str(i[1])+"'"
        cur.execute(query2)
        book = cur.fetchall()
        books.append(book[0])
    print(books)
    conn.commit()
    return render_template('wishlist.html', data={'id': id, 'wishlist_data': books})


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup/add_user', methods=['POST'])
def signup_add_user():
    try:
        conn = psycopg2.connect(
            dbname="ebooks", user='admin', password='admin@123', host="my_db",port="5432")
        cur = conn.cursor()
        print('1')
        username = request.form.get("username")
        user_password = request.form.get("password")
        re_password = request.form.get("re_password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dob = request.form.get("dob")
        ph_no = request.form.get("ph_no")
        card_upi = request.form.get("card_upi")
        email_id = request.form.get("email_id")
        print(2)
        if user_password == re_password:
            insert_user = "INSERT INTO user_details (userid,dob,password,firstname,lastname,email_id,user_name,ph_no,card,store_id ) VALUES ((SELECT MAX(userid)+1 FROM user_details),"

            user_val_insert = [str(dob), str(user_password), first_name,
                               last_name, email_id, username, str(ph_no), str(card_upi), str(1)]
            user_val_insert = ["'"+i+"'" for i in user_val_insert]
            final_val_insert = ','.join(user_val_insert)
            final_insert_commd_autom = insert_user + final_val_insert + ")"
            print(final_insert_commd_autom)
            cur.execute(final_insert_commd_autom)
            conn.commit()

            userid="SELECT MAX(userid) FROM user_details"
            cur.execute(userid)
            userid = cur.fetchall()
            userid=userid[0][0]
            userid=int(userid) 
            
            

            print('==========')
            print(userid)

            sales_id="SELECT MAX(order_id) FROM payment"
            cur.execute(sales_id)
            sales_id = cur.fetchall()
            sales_id=sales_id[0][0]+1
            print("====")
            print(sales_id)
            print(final_insert_commd_autom)
            cur.execute("CREATE user {} password '{}'".format(username,user_password))
            cur.execute("GRANT SELECT ON book_catalogue TO {}".format(username))
            cur.execute("GRANT SELECT ON book_catalogue_genre TO {}".format(username))
            cur.execute("create view "+username +"_user as select * from user_details where user_name = '"+username+"'")
            cur.execute("GRANT SELECT,UPDATE ON " + username + "_user TO "+username)
            cur.execute("GRANT SELECT,DELETE,INSERT,TRUNCATE ON cart TO "+username)
            cur.execute("GRANT SELECT,INSERT ON library TO "+username)
            cur.execute("GRANT SELECT,DELETE,INSERT ON wishlist TO "+username)
            cur.execute("GRANT SELECT,INSERT ON payment TO "+username)
            cur.execute("GRANT SELECT,INSERT,UPDATE ON sales TO "+username)
            cur.execute("INSERT INTO payment VALUES ( "+str(sales_id)+","+str(sales_id+1000)+", 0, '2015-04-11 01:55:24',"+str(userid)+")")
            print(4)
            conn.commit()
            conn.close()
            conn = None
            cur = None
            return render_template('index.html')

        else:
            return render_template('error.html', data={"message": "Passwords do not match"})

    except Exception as ex:
        print(ex)
    # try:
    #     query = "select * from book_catalogue"
    #     cur.execute(query)
    #     books_record = cur.fetchall()
    #     query_user="select userid from user_details where user_name='"+username+"'"
    #     cur.execute(query_user)
    #     id=cur.fetchone()
    #     id=int(str(id)[1:-2])
    #     print(id)
    #     print(books_record)
    # except Exception as ex:
    #     print(ex)
    #     return render_template('error.html', data = {"message": "You are not authorized to access the database"})

    # return render_template('main.html',data={'username':username,'id':id,'items':books_record})
@app.route('/delete_cart/<isbn>')
def delete_from_cart(isbn):
    try:
        print(isbn)
        query="DELETE FROM cart where isbn='"+isbn+"'"
        cur.execute(query)
        conn.commit()
    except Exception as ex:
        print(ex)
    return render_template('data.html', data={'message':"Deleted from cart","id":user_id_g})

@app.route('/delete_wishlist/<isbn>')
def delete_from_wishlist(isbn):
    try:
        
        query="DELETE FROM wishlist where isbn='"+isbn+"'"
        cur.execute(query)
        conn.commit()
    except Exception as ex:
        print(ex)
    return render_template('data.html', data={'message':"Deleted from wishlist","id":user_id_g})

@app.route('/payment_details/<id>')
def payment_details(id):
    query="select * from payment"
    cur.execute(query)
    payment_record = cur.fetchall()
    print(payment_record)
    user_payment=[]
    for item in payment_record:
        print(item[4])
        if int(item[4])==int(user_id_g):
            user_payment.append(item)
    print(user_payment)
    return render_template('payment.html', data={'id': id, 'payment_data': user_payment})
    

@app.route('/logout')
def logout():
    user_id_g=None
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


'''
query = "select count(*) from book_catalogue where isbn="+str(isbn)+" and userid="+str(user_id_g)
        cur.execute(query)
        books_record = cur.fetchall()
        if(len(books_record)!=0):
            return render_template('data.html', data={'message':"Already exists","id":user_id_g})
        print(isbn)
'''