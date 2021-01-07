# It's not procrastinating if it's in Python

Maybe it would be faster to browse one ad after another and not write an app right away...? 
I guess we'll never know...

#### Information from the announcement:
- the price of the apartment
- district
- the size of the apartment
- do we have a flat projection
- how many rooms
- what does it look on pictures

#### Additional information from the text:
- exact location - which street
- which floor
- rent amount
- is there a balcony / loggia / terrace
- year of construction
- what's in the vicinity
- storage room downstairs / basement
- garage? (+ how much)

#### Calculate later:
- distance to the metro station
- distance from the park
- how to get to my gym (!!!)
- average price per meter

> LOCATION, LOCATION, LOCATION

# Plan
1. Collect data from all ads (+ photos)
2. Clean data
3. Store data in a meaningful way (+ cloud backup)
4. Website in Flask to view selected offers - according to my criteria + all photos at once
5. Anomaly detection analysis?
    - average price per meter in the district
    - notification when a new ad is _sus_
6. Preview on the map (how far to Gorilla) and the [acoustic map of Warsaw](http://mapa.um.warszawa.pl/mapaApp1/mapa?service=mapa_akustyczna&L=PL&X=7501841.83526767&Y=5782957.86084302&S=15&O=0&T=7dffc0100100001007fff004xA9)  
7. Check if the advertisement is still hanging (add the date on which it disappeared)
8. Check occasionally if the price hasn't changed (to get the feeling of real prices :P)


## Assumptions
1. Each apartment has one bathroom minimum - so if it is not mentioned in the advertisement, the default value of num_bathrooms is 1
2. When the price is changed, the ad ID remains the same
3. If the "flat" costs less than PLN 100,000, it probably means the exchange / sharing of ownership and I do not want to have this advertisement in the database
4. Only one price change per day can be saved in the database


## New plan?
Perhaps just an app in Flask to check the distance from many places at once.
New apartment address - gym, dance school ... at different times