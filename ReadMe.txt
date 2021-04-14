Shopping Cart Assigment:

Folder Structure:	

	CuraTech_Assignment
		|----purchase
		|	|----migrations
		|	|----templates
		|	|	|----purchase
		|	|		|----checkout.html
		|	|		|----item_details.html
		|	|		|----master.html
		|	|		|----shopping_cart.html
		|	|
		|	|----admin.py
		|	|----apps.py
		|	|----models.py
		|	|----tests.py
		|	|----urls.py
		|	|----utils.py
		|	|----views.py
		|	
		|----ShoppingCart
		|	|----asgi.py
		|	|----settings.py
		|	|----urls.py
		|	|----wsgi.py
		|	
		|----static
		|	|----css		
		|	|     |----bootstrap.css
		|	|     |----bootstrap.min.css
		|	|     |----main.css
		|	|
		|	|----images
		|	|	|----placeholder.jfif
		|	|	|----shopping_cart.png
		|	|
		|	|----js
		|	|    |----bootstrap.js
		|	|    |----bootstrap.min.js
		|	|    |----cart.js
		|	|    |----jquery.min.js
		|
		|----db.sqlite3
		|----manage.py
		|----ReadMe.txt
	

models.py :

	1. Customer - Stores the customer details.

		user  (OneToOneField)      : Points to the user(example: admin)
		name  (CharField, len:200) : Represents the customer name.
		email (CharField, len:200) : Represents the customer mail id.

	2. Item - Stores the item details.

		item_name         (CharField, len:200) : Represents the item name.
		item_price        (IntegerField)       : Represents the price of one unit.
		discount_quantity (IntegerField)       : Represents minimum number of items to be 
	                                                 purchased to avail discount.
		discount-amount   (IntegerField)       : Represents discount amount on purchase of 
				                         item in accordance with discount_quantity.

	3. Order - Stored order related information.
		
		customer    (ForeignKey Customer)     : Relation with the Customer model.
		order_id    (CharField, len:200)      : Application generated order_id.
		order_date  (DateTimeField)           : Auto generated date.
		cart_status (BooleanField, def=False) : Represents the status of the cart.

	4. OrderItem - Stores the items added to the cart by user.

		item	   (ForeignKey Item)  : Relation with Item model.
		order      (ForeignKey Order) : Relation with Order model.
		quantity   (IntegerField)     : Stores the quantity of items added to cart.
		date_added (DateTimeField)    : Auto generated date.

	5. ShippingDetails - Stores the shipment information of user.

		customer   (ForeignKey Customer) : Relation with Customer model.
		order      (ForeignKey Customer) : Relation with Order model.
		address    (CharField, len:200)  : Stores the user address.
		city       (CharField, len:200)  : Stores the user city.
		state      (CharField, len:200)  : Stores the user state.
		pin_code   (CharField, len:200)  : Stores the user pin_code.
		date_added (DateTimeField)       : Auto generated date

	6. FinalDiscount - 

		cart_total      (IntegerField) : Stores the minimum cart amount to avail additional discount.
		discount_amount (IntegerField) : Stores the additional discount amount.

views.py :

	1. item_details  : Renders the store home page from where user can select a product and add it to their cart.
	2. shopping_cart : Renders the cart page where the added items are displayed along with the discount and total calculation.
	3. checkout      : Renders the checkout page where the user can fill in shipping information and make the payment.
                           (Payment integration have not been done yet)
	4. get_total     : Handles the discount calculation logic for each item.
	5. update_item   : Handles the logic for addition and deletion of items to the cart from the cart page itself.
	6. process_order : Sends the user data including shipping address, purchased items to the backend for storing.


utils.py : Utility file that handles the most operations done by the views.py

	1. guest_cart     : Handles the logic for a guest user to be able to add items to the cart and purchase it using a created cookie.
	2. cart_purchase  : Handles the logic for purchase of all cart items by an user.
	3. guest_checkout : Handles the logic of creating a user for the guest and adding his purchase to the backend.


templates -> purchase :

	1. master.html        : Contains the basic page structure that will be inherited by the other html pages.
			        Also handles the csrf token generation and the cookie creating for handling the guest user purchase.
	2. item_details.html  : Extends the master and adds the items view in the page allowing the user to choose and add it to cart.
	3. shopping_cart.html : Contains the cart page view.
	4. checkout.html      : Contains the checkout page view. Uses javascript to capture the data from the page and send it to backend for validation and storing.


static -> css -> main.css : Stores the created css classes and style for design of the webpages.


static -> js -> cart.js   : JavaScript with functions to update user order into database, add guest user items to the created cookie and updating the cart functionality on button click.


Database : sqlite3

Run application : 

	1. Follow the folder structure and type in the terminal : python manage.py runserver
	2. Open any browser and go to : localhost:8000/purchase
