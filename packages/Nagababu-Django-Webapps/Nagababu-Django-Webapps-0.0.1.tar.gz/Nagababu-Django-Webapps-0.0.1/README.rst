# Django-Food-Webapps
  -------------------


Nsoft-Food contains three Django apps named as ``webapp1`` , ``webapp2`` , ``webapp3``. 
``webapp1`` used for Authantication and Autharization 
``webapp2`` used for navigating Food items
``webapp3`` used for Adding items to Cart, Remove items from Cart and Payment processing.



# Quick start


1. Add ``webapp1``,``webapp2``,``webapp3`` to your INSTALLED_APPS setting like this::
    
    INSTALLED_APPS = [
        		...
     			``webapp1``,
     			``webapp2``,
     			``webapp3``,
                        ``widget_tweaks``,
                        ``crispy_forms``,  
   	            ]
    

2. Include the every app URLconf in your project urls.py like this
       
      urlpatterns = [
    			path('food/',include(``webapp1.urls``)),
    			path('items/',include(``webapp2.urls``)),
    			path('order_items/',include(``webapp3.urls``)),
		     ]
      

3. Run ``python manage.py migrate`` to create the ``webapp1`` , ``webapp2`` , ``webapp3``  models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a those three apps (you'll need the Admin app enabled).
   - create a admin 
   	-- python manage.py createsuperuser

5. Visit http://127.0.0.1:8000/food/Registration/ to create a Registration 
6. Visit http://127.0.0.1:8000/food/Login/  Navigates to the Login interface.
7. Detail documentation [click here](https://github.com/Nagababu995/Naga-Django-Webapps/blob/master/README.md)
