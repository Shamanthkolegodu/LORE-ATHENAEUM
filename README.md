# LoreAthenaeum-Ebooks-store
The ebook store allows its users to browse and buy electronic books and read them on the
device the application is being used in. It provides the following services and support.

## Problem Statement
The ebook store allows its users to browse and buy electronic books and read them on the
device the application is being used in. It provides the following services and support.
1. It keeps track of users with an authentication system by validating their login credentials.
2. It provides utilities like wishlist, library, cart and payment to all of its users and also
maintains user details like user’s name, username, password, email id, date of birth (DOB),
UPI/card details.
3. Wishlist maintains a list of user’s want to read books, Library stores the books the user buys,
Cart maintains a list of books that the user is ready to buy and the user can buy the books
through payment using Card/UPI.
4. Payment keeps track of order, transaction, the amount to be paid and date and time of
transaction.
5. It maintains the book catalogue with its ISBN, name, category, genre, publisher, author, year
of publishing, language, rating, price, size of the book and their edition.
6. It maintains a sales report that helps keep track of best selling and new books.
7. It also provides customer support - email id and phone number for the users.

## Entities and Attributes:
1. User - The User entity contains the following attributes: Userid, Name, Username, Date of
Birth, Password, Email-id, Phone number.
2. Book - The Book entity contains the following attributes: ISBN, Name, Publisher, Category,
Genre, Language, Author, Size, Rating, Year of Publishing, Price, Edition.
3. Wishlist - The Wishlist entity contains the following attributes: Wishlist-id.
4. Library - The Library entity contains the following attributes: Library-id.
5. Cart - The Cart entity contains the following attributes: Cart-id, Total Price, Number of
Items.
6. Payment - The Payment entity contains the following attributes: Order-id, Transaction-id,
Price, Date-time.
7. Store - The Store entity contains the following attributes: Name, HeadQuarters Location,
Store id, Customer Support containing Phone Number and Email-id.
8. Sales - The Sales entity contains the following attributes: Sales-id, Total Revenue, Number of
copies sold.

## ER Diagram of ebooks store
![alt ps](https://github.com/Shamanthkolegodu/LoreAthenaeum-Ebooks-store/blob/main/ER-Diagram.jpg)

## Relational Schema of ebooks store
![alt ps](https://github.com/Shamanthkolegodu/LoreAthenaeum-Ebooks-store/blob/main/RelationalSchema.jpg)

## Tech Used:
1. Postgresql as RDBMS server
2. Python3 and Flask for backend
3. HTML, CSS and Bootstrap for frontend 
4. Psycopg2 as database adapter for the Python backend

Part of 5th semester Mini-Project for the course Database Management Systems at PES University, Bangalore
