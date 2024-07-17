# vestide_scrapper
This is a webscrapper for Vestide rooms
This project scrapes rooms posted in Vestide
The crawler checks that the room has 'Toilet', 'Shower','Kitchen' independent you can delete any of them according to your needs
Feel free to change the refresh time (default 2700 secs)

There are 2 methods to alert you:
<li> <b>send_mail</b> to send gmail (by default to the same account)</li>
<li> <b>post_discord</b> to send a notification to a discord channel</li>

When an alert is sent, it is cached locally in the folder `rooms` to avoid spam.
TO RUN:
1. ```python3 -m venv myenv```
2. ```source myenv/bin/activate```
3. ```pip install -r requirements.txt```
4. ```python vestide.py```
