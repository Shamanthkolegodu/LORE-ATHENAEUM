# LORE-ATHENAEUM
Lore Athenaeum - Ebooks store


## Problem Statement
The ebook store allows its users to browse and buy electronic books and read them on the
device the application is being used in. It provides the following services and support.
● It keeps track of users with an authentication system by validating their login credentials.
● It provides utilities like wishlist, library, cart and payment to all of its users and also
maintains user details like user’s name, username, password, email id, date of birth (DOB),
UPI/card details.
● Wishlist maintains a list of user’s want to read books, Library stores the books the user buys,
Cart maintains a list of books that the user is ready to buy and the user can buy the books
through payment using Card/UPI.
● Payment keeps track of order, transaction, the amount to be paid and date and time of
transaction.
● It maintains the book catalogue with its ISBN, name, category, genre, publisher, author, year
of publishing, language, rating, price, size of the book and their edition.
● It maintains a sales report that helps keep track of best selling and new books.
● It also provides customer support - email id and phone number for the users.

## Entities and Attributes:
● User - The User entity contains the following attributes: Userid, Name, Username, Date of
Birth, Password, Email-id, Phone number.
● Book - The Book entity contains the following attributes: ISBN, Name, Publisher, Category,
Genre, Language, Author, Size, Rating, Year of Publishing, Price, Edition.
● Wishlist - The Wishlist entity contains the following attributes: Wishlist-id.
● Library - The Library entity contains the following attributes: Library-id.
● Cart - The Cart entity contains the following attributes: Cart-id, Total Price, Number of
Items.
● Payment - The Payment entity contains the following attributes: Order-id, Transaction-id,
Price, Date-time.
● Store - The Store entity contains the following attributes: Name, HeadQuarters Location,
Store id, Customer Support containing Phone Number and Email-id.
● Sales - The Sales entity contains the following attributes: Sales-id, Total Revenue, Number of
copies sold.
