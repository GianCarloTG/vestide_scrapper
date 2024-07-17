import requests
import bs4
from bs4 import BeautifulSoup
import re
import time
import os


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


url = 'https://rooms.vestide.nl/en/find-room/detail-accommodation/'
url_room = 'https://rooms.vestide.nl/en/find-room/detail-accommodation/?detailId={room}'
class_check = 'house-thumb-click-area'
room_class = 'specs-list-col-m'

channel = ''
auth = '' 

save_path = './rooms/' #create a folder with this name

mail = "my@gmail.com" # here put your gmail
mail_password = '' # obtain the gmail auth from here: https://support.google.com/mail/answer/185833?hl=en


def send_mail(message, mail, mail_password):
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = mail
    msg['Subject'] = 'Vestide room'

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  
    server.login(mail, mail_password)
    server.sendmail(mail, mail, msg.as_string())
    server.quit()


def post_discord(channel, message, auth):
    '''
    Postss url in a discord channel
    '''
    # not called
    payload = {
        "content":message
    }
    headers = {
        "Authorization":auth
    }
    res = requests.post(channel, payload, headers=headers)


def get_room_ids()-> list:
    '''
    get rooms id
    '''
    response = requests.get(url)
    main_page = BeautifulSoup(response.text, 'html.parser')

    # check rooms availables
    results = main_page.find_all("a", {"class": class_check})
    ids = [int(re.findall(r'\d+', str(id))[0]) for id in results ]
    return ids

def check_conditions(dict_facilities)->bool:
    '''
    Check if accepted for housing allowance
    '''
    # i want 'Toilet', 'Shower','Kitchen' to be independent
    check = all(value == 'independent' for value in dict_facilities.values())
    return check

def check_room(room_id)->str:
    '''
    get room info
    post info into discord
    cache rooms checked 
    '''
    room_response = requests.get(url_room.format(room=room_id))
    room_page = BeautifulSoup(room_response.text, 'html.parser')

    # check conditions
    facilities = [ 'Toilet', 'Shower','Kitchen'] #You can add sink independt too 'Sink',
    dict_facilities = {}
    for facilitie in facilities:
        room_sink = room_page.find('span', text=facilitie)
        if room_sink:
            next_sibling = room_sink.find_next_sibling('span').text
            if next_sibling:
                shared = str(next_sibling.strip()).lower()
        #shared = str(room_sink.find_next_sibling('span').text.strip()).lower()
                dict_facilities[facilitie] = shared
    
    if check_conditions(dict_facilities):
        isExisting = os.path.exists(save_path +'room_'+ str(room_id) + '.txt')
        if not isExisting:
            message = "New room posted: \t"+url_room.format(room = room_id)
            #post_discord(channel, message, auth)
            send_mail(message, mail, mail_password)
            print('Mail sended')
            with open(save_path +'room_'+ str(room_id) + '.txt', 'w') as f:
                f.write(str(message))

def main():
    while(True): 
        rooms_ids = get_room_ids()
        print(rooms_ids)
        for room in rooms_ids:
            check_room(room)
        time.sleep(2700)

if __name__ == "__main__":
    main()
