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
|Add-to-cart button|When clicked, the product is added to the cart, the user remains on the product detail page and a relevant message is displayed|Clicked|As expected|![Product detail add-to-cart success](./images/testing/product-detail-add-to-cart-success.png)|
|Edit-product button|When clicked by a logged-in admin, the admin is taken to the edit product page|Clicked|As expected|![Product detail add-to-cart success](./images/testing/product-detail-edit-delete-buttons.png)|
|Delete button|When clicked by a logged-in admin, the product is deleted and the admin is taken to the products page|Clicked|As expected|![Product detail delete success](./images/testing/product-detail-delete-success.png)|

