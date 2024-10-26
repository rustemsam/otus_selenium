# Bugs

## Bug 1

#### Name

When you're trying to add some items from main page to the basket, it's opening the information about an item instead

#### Severity

Medium

#### Steps to reproduce

1. Open the page:http://192.168.1.47:8081/en-gb?route=common/home
2. Try to add from main page, for example, Canon EOS 5D, by clicking on the button:
   Add to Card

#### Expected result

1. The item was added to the shopping card

#### Actual result

1. The page about the item was opened: http://192.168.1.47:8081/en-gb/product/canon-eos-5d

________________________________________________________________________________________________________________________

# Bugs

## Bug 2

#### Name

Total count of elements on the page != count of elements on the left side

#### Severity

Medium

#### Steps to reproduce

1. Open the page:http://192.168.1.47:8081/en-gb?route=common/home
2. Click Desktops
3. Click Show All Desktops
4. Check the numbers in () for Desktops and total in the bottom

#### Expected result

1. It's showing Desktops (13), so I'm expecting to see also in the bottom: Showing 1 to 10 of 13 (2 Pages)

#### Actual result

1. It's showing Desktops (13), but in the bottom: Showing 1 to 10 of 12 (2 Pages)

________________________________________________________________________________________________________________________

## Bug 3

#### Name

Total count of elements on the page != count of categories

#### Severity

Medium

#### Steps to reproduce

1. Open the page:http://192.168.1.47:8081/en-gb?route=common/home
2. Click Desktops
3. Click Show All Desktops
4. Check the numbers in () for Desktops and numbers for subcategories

#### Expected result

1. It's showing Desktops (13), so I'm expecting to see that subcategories also show the total this amount

#### Actual result

1. It's showing Desktops (13), but subcategories:    - PC (0) and - Mac (1)

________________________________________________________________________________________________________________________

## Bug 4

#### Name

There is no validation for the field "Qty"

#### Severity

Medium

#### Steps to reproduce

1. Open the page:http://192.168.1.47:8081/en-gb?route=common/home
2. Click Desktops
3. Click Show All Desktops
4. Click on the left side for category Mac
5. Click for the item iMac
6. In the field Qty change 1 to some string, for example, "test"
7. Click Add to Cart

#### Expected result

1. Either it will not allow us to put string in this field, or it will show us some alert with red background that it's
   not allowed to put in this field string value

#### Actual result

1. It's showing success alert with text: Success: You have added iMac to your shopping cart
   ![Bug](src/tests/resources/bugs/bug-quantity.png)

________________________________________________________________________________________________________________________

## Bug 5

#### Name

There is a possibility to create a password with length more than 20 symbols, even the limit is 20

#### Severity

Medium

#### Steps to reproduce

1. Open the page:http://192.168.1.47:8081/en-gb?route=account/register
2. Fill first name, last name, email
3. Fill the password with length more than 20 symbols
4. Agree to policy and click Continue

#### Expected result

1. It will return an error/alert that password is more than 20 symbols, like it returns when you're filling the password
   less than 4 symbols
      ![Bug](src/tests/resources/bugs/email.png)

#### Actual result

1. The account is created without any error


________________________________________________________________________________________________________________________
