Category, Brand, Color, ColorPrice, and Discount do not need any list-view, detail-view, update-view, or delete-view
unless we need to manage them via completely customized admin interface instead of django-admin interface.

Product has detai-view but its list-view is actually implemented in 'vitrin' app. Product detail-view and update-view
have not implemented. They only needed to defined when we want to create a completely new admin interface from scrach.

Every product with unknown brand will get 'other' brand.

For better performance, we can creat a model for every Brand - Category. But we can create an index for every Product
to with its brand and category as index field.

If 'Product.is_active' is 'False', it means the product couldn't be bought or shipped. If there is a problem with the
product, we should raise this flag.

Discounts effect on price for the product will be affected in the 'shop.signals'.
