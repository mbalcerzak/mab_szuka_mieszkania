# It's not procrastinating if it's in Python

This project was created to aid in apartment search in Warsaw. Since then the author decided not to buy any real estate in Poland and travel instead and Gumtree Polska closed. 

#### Information from the announcement:
- the price of the apartment
- district
- the size of the apartment
- do we have a flat projection
- how many rooms
-  pictures

#### Additional information from the text:
- exact location - which street
- which floor
- rent amount
- is there a balcony / loggia / terrace
- year of construction
- what's in the vicinity
- storage room downstairs / basement
- garage? (+ how much)

## Assumptions
1. Each apartment has one bathroom minimum even if it is not mentioned in the advertisement (the default value of num_bathrooms is 1)
2. If the "flat" costs less than PLN 100,000, it probably means the exchange / sharing of ownership and I do not want to have this advertisement in the database
