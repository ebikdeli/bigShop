This app contains all the work about 'signup' and 'login' users and closely related to 'accounts' app.
Other things about editing user account and resetting password are also bundeled in the app.

Username mostly done by phone number but also with email.

After user login or signup, 'Cart.object.sync_session_cart_after_authentication()' will be executed. To
obey clean code principles, this implemented in 'login' module.