# Scentifique - Manual Testing

## Front-End Functionality

### Header Navigation

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Site title|When clicked, the user is taken to the homepage|Clicked|As expected|None|
|Account menu|When the user is not logged in, the icon is white and the menu has sign-up and sign-in options|Viewed header when logged out|As expected|![Account logged out](./images/testing/account-logged-out.png)|
|Account menu|When the user is logged in, the icon is gold, the text is bold and the menu has user-profile and sign-out options|Viewed header when logged in|As expected|![Account logged in](./images/testing/account-logged-in.png)|
|Sign-up menu item|When clicked, the user is taken to the sign-up page|Clicked|As expected|None|
|Sign-in menu item|When clicked, the user is taken to the sign-in page|Clicked|As expected|None|
|Sign-out menu-item|When clicked, the user is taken to the sign-out page|Clicked|As expected|None|
|Cart link|When the cart is empty, the icon is white|Viewed when cart was empty|As expected|![Cart link empty](./images/testing/cart-empty.png)|
|Cart link|When the cart is not empty, the icon is gold and the text is bold|Viewed when cart was not empty|As expected|![Cart link not empty](./images/testing/cart-not-empty.png)|
|Home link|When clicked, the user is taken to the home page|Clicked|As expected|None|
|Home link|When the user is on the home page, the text is bold|Viewed from home page|As expected|![Home page nav](./images/testing/home-nav.png)|
|About link|When clicked, the user is taken to the About page|Clicked|As expected|None|
|About link|When the user is on the About page, the text is bold|Viewed from About page|As expected|![About page nav](./images/testing/about-nav.png)|
|Products link|When clicked, the user is taken to the Products page|Clicked|As expected|None|
|Products link|When the user is on the Products page, the text is bold|Viewed from Products page|As expected|![Products page nav](./images/testing/products-nav.png)|

## Messages

Messages were testing during each of the relevant testing sections below.

## Homepage Hero

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Shop now button|When clicked, the user is taken to the products page|Clicked|As expected|None|

## Contact Details

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Social media icons|When clicked, the user is taken to the relevant social media platform|Clicked|As expected|None|

## Product List

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Product image|When clicked, the user is taken to the product details page for that product|Clicked|As expected|None|
|View button|When clicked, the user is taken to the product details page for that product|Clicked|As expected|None|

## Product Detail

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Colour, Fragrance and Quantity selectors|When clicked, the user is able to select a colour, fragrance or quantity|Clicked|As expected|![Product detail selector](./images/testing/product-detail-selector.png)|
|Add-to-cart button|When clicked, the product is added to the cart, the user remains on the product detail page and a success message is displayed|Clicked|As expected|![Product detail add-to-cart success](./images/testing/product-detail-add-to-cart-success.png)|
|Edit-product button|When clicked by a logged-in admin, the admin is taken to the edit product page|Clicked|As expected|![Product detail add-to-cart success](./images/testing/product-detail-edit-delete-buttons.png)|
|Delete button|When clicked by a logged-in admin, the product is deleted, the admin is taken to the products page and a success message is shown|Clicked|As expected|![Product detail delete success](./images/testing/product-detail-delete-success.png)|

## Add Product

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Validation|If the form is submitted with blank mandatory fields, submission fails and a validation error is shown|Clicked|As expected|![Product add mandatory error](./images/testing/product-add-mandatory-error.png)|
|Add product button|If the form is submitted with valid data, a product is created, the admin is redirected to the product detail page for the new product, and a success message is shown|Clicked|As expected|![Product add success](./images/testing/product-add-success.png)|
|Authentication|If a logged in non-admin user visits the add product page, they are redirected to the home page and an error message is displayed|Clicked|As expected|![Product add authentication](./images/testing/product-add-authentication.png)|

## Edit Product

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Validation|If the form is submitted with blank mandatory fields, submission fails and a validation error is shown|Clicked|As expected|![Product edit mandatory error](./images/testing/product-edit-mandatory-error.png)|
|Update product button|If the form is submitted with valid data, the product is updated, the admin is redirected to the product's detail page and a success message is shown|Clicked|As expected|![Product edit success](./images/testing/product-edit-success.png)|
|Authentication|If a logged in non-admin user visits the edit product page, they are redirected to the home page and an error message is displayed|Clicked|As expected|![Product add authentication](./images/testing/product-edit-authentication.png)|

## Shopping Basket

|Feature|Expect|Action|Result|Image|
|---|---|---|---|---|
|Empty cart|When the cart is empty, the user is informed and a continue shopping button is shown|Visited the shopping cart page when the cart was empty|As expected|![Empty cart](./images/testing/cart-empty-page.png)|
|Non-empty cart|When the cart is not empty, a list of the products in the cart is shown, along with relevant details|Visited the shopping cart page when the cart was not empty|As expected|![Not empty cart](./images/testing/cart-not-empty-page.png)|
|Update button|If a cart item's update button is clicked after its colour, fragrance and/or quantity have been changed, the changes are saved, the page is refreshed and a success message is shown|Changed a cart item's colour, fragrance and quantity and clicked the update button|As expected|![Updated cart item](./images/testing/cart-item-updated.png)|
|Limiting quantity|If a cart item is updated to match the colour, fragrance and product type of another cart item, the two items are combined and their quantities are summed, with a limit value of 12|Changed a cart item's colour, fragrance and quantity and clicked the update button|As expected|![Updated cart item](./images/testing/cart-item-updated.png)|
Remove button...
etc...
