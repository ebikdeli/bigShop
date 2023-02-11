To initialize sessions needed in the website, we need to define them somewhere to executed exactly before
any view called. To be able to do that, we created a custom Middleware in the cart application. The 
'InitialSessionMiddleware' at the end of middleware chain, executed exactly every time before every view.

for any user connected to the website (UnAuthenticated), a Cart object created without a 'user' field. Any
product added or removed from the cart, added to the 'cart' session first then from cart session added to
the database. If user then authenticate, all data from cart session added to the already registered user
cart and both the session and cart updated to get equal.

Only when 'total_item_number' and 'price' and 'price_end' fields of the Cart object updated, that any of
the cart instance CartItem updated first! In other word, in 'signals' module we done that with 'CartItem'
'post_save' signals.

Delete an item from cart (or delete an CartItem) has created on model level in 'CartItem.delete()' method.

'Cart.object.sync_session_cart_after_authentication()' executed after login or signup.