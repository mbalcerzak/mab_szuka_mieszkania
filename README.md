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
- price "370" means probably "370 000"
3. Store data in a meaningful way (+ cloud backup)
4. Website in Flask to view selected offers - according to my criteria + all photos at once
5. Anomaly detection analysis?
    - average price per meter in the district
    - notification when a new ad is _sus_
6. Preview on the map (how far to Gorilla) and the [acoustic map of Warsaw](http://mapa.um.warszawa.pl/mapaApp1/mapa?service=mapa_akustyczna&L=PL&X=7501841.83526767&Y=5782957.86084302&S=15&O=0&T=7dffc0100100001007fff004xA9)  
7. Check if the advertisement is still hanging (add the date on which it disappeared)
8. Check regularly  if the price hasn't changed (flat owners are the best real price gauge)


## Assumptions
1. Each apartment has one bathroom minimum even if it is not mentioned in the advertisement (the default value of num_bathrooms is 1)
2. If the "flat" costs less than PLN 100,000, it probably means the exchange / sharing of ownership and I do not want to have this advertisement in the database


## Analysis
An app in Flask. Features:
- check the distance from many places at once. New apartment address - gym, 
  dance school ... at different times
- Show the ad in some other way
- Graph showing tha flat's price (and changes) vs. average for the neighborhood
- Flag parts of the ad that are unusual (e.g. for this size it should be more expensive...)


## Ideas for exploration
- Can we extract location from photos? Usually they only tell you street and it's not super specific
- Is the date of taking the ad down important?

## Ads

Free:
 - www.gumtree.pl
 - www.olx.pl
 - www.bezposrednio.com
 - www.domoklik.pl
 - www.anonse.com
 - www.najdom.pl
 - www.nieruchomosci.net.pl
 - www.sprzedajemy.pl

Paid:
 - www.domiporta.pl
 - www.gratka.pl
 - www.otodom.pl
 - www.oferty.net
 - www.nieruchomosci.pl
 - www.morizon.pl
 - www.domy.pl
 - www.tabelaofert.pl
 - www.nieruchomosci-online.pl
