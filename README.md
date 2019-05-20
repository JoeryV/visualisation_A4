# Visualisation Assignment 4

Code in this directory is the result of a dashboard our group designed for a school assignment for the course "Data Visualisation" at the Jheronimus Academy of Data Science ([JADS](https://www.jads.nl)).

The purpose of this assignment was to develop a dashboard which allows for interactive browsing through data. 

Our team chose to work with Top2000 data, a yearly recurring 'song-competition' in the Netherlands where the entire country can vote for the 2000 best songs. The songs that make it into the list are played by Radio 2 from Christmas day noon until midnight of New Years eve. 


#### Team
* Sjoerd Broos
* Casper Verboon
* Vincent Munos
* Nima Mahzoun
* Joery de Vos

#### Result
Examples of what the app visually looks:

Landing page:
![""Landing page"](./Screenshots/Page1.png)

Fun Facts page:
![""Fun Facts"](./Screenshots/Page2.png)

Advanced analytics page:
![""Advanced analytics 1"](./Screenshots/Page3-1.png)
![""Advanced analytics 2"](./Screenshots/Page3-2.png)

Lyric analysis page:
![""alt text"](./Screenshots/Page4.png)


#### Data sources
Data used in this assignment were gathered from the [Wikipedia Top2000 page](https://nl.wikipedia.org/wiki/Lijst_van_Radio_2-Top_2000%27s) and extended using Spotify WEB API's python library [Spotipy](https://spotipy.readthedocs.io/en/latest/)

#### How to run 
In order to make the app work in full, one has to acquire spotify API creditials which can be obtained following the process [here](https://developer.spotify.com/documentation/general/guides/authorization-guide/). The credentials should then be saved in the Code folder in a file called "token_files.py". An example of it is available under the Code folder.
 
The dashboard will run without the spotify API credentials but features such as playing a song and updating images will be unavailable. 

The dashboard can be fired up by either: 
1. running it inside a virtual environment containing the data folder or 
2. updating the "data_location" variable in the [load_data.py](./Code/load_data.py) file to absolute path of the folder containing the data. 

The app is built on the packages and versions listed in requirements.txt

Make the dashboard run on your local machine by executing app.py 