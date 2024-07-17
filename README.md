# vestide_scrapper
This is a webscrapper for Vestide rooms
This project scrapes rooms posted in Vestide
The crawler checks that the room has 'Toilet', 'Shower','Kitchen' independent you can delete any of them according to your needs
Feel free to change the refresh time (default 2700 secs)
There are 2 methods to alert you:
`send_mail` to send gmail (by default to the same account)
`post_discord` to send a notification to a discord channel
When an alert is sent, it is cached locally in the folder `rooms` to avoid spam.
TO RUN:
```python3 -m venv myenv```
```source myenv/bin/activate```
```pip install -r requirements.txt```
```python vestide.py```