from user.routes import app as user
from books.book_routes import app as book
from cart.cart_routes import app as carts


# flask --app app:user run --debug --port 7000
# flask --app app:carts run --debug --port 8000
# flask --app app:book run --debug --port 5000