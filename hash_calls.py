


from tkinter import *
import requests
from requests.exceptions import HTTPError

class window:

    def __init__(self):

        self.userInfo = {}
        self.access_token = ""
        self.groupContacts = []

        self.window = Tk()
        self.window.geometry('600x600')
        self.window.title("This is...Kevin's Event Guest List Email Scrubber")

        self.cidlbl = Label(self.window, text="client ID")
        self.cidlbl.grid(column=3, row=0)
        self.cid_txt = Entry(self.window,width=10)
        self.cid_txt.grid(column=4, row=0)

        self.cslbl = Label(self.window, text="client Secret")
        self.cslbl.grid(column=3, row=1)
        self.cs_txt = Entry(self.window,width=10)
        self.cs_txt.grid(column=4, row=1)

        self.unlbl = Label(self.window, text="username")
        self.unlbl.grid(column=3, row=2)
        self.un_txt = Entry(self.window,width=10)
        self.un_txt.grid(column=4, row=2)

        self.pwlbl = Label(self.window, text="password")
        self.pwlbl.grid(column=3, row=3)
        self.pw_txt = Entry(self.window,width=10)
        self.pw_txt.grid(column=4, row=3)

        self.eidlbl = Label(self.window, text="event ID")
        self.eidlbl.grid(column=3, row=4)
        self.eid_txt = Entry(self.window,width=10)
        self.eid_txt.grid(column=4, row=4)

        self.access_tokenlbl = Label(self.window, text= "Access Token")
        self.access_tokenlbl.grid(column=3, row=5)
        self.access_token_input = Label(self.window, text= "---------")
        self.access_token_input.grid(column=4, row=5)
        #center window
        w = 600 # width for the Tk root
        h = 600 # height for the Tk root

        # get screen width and height
        ws = self.window.winfo_screenwidth() # width of the screen
        hs = self.window.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def start_window(self):
        self.window.mainloop()

    def create_buttons(self):
        self.step1 =Button(self.window, text = "step 1: get the Token...wait till something appears in the Access Token",
           command = self.get_input_and_get_token).grid(row = 10, sticky = W,column = 4)

        self.step2 = Button(self.window, text = "step 2: hash the emails ",
           command = self.hash_the_emails).grid(row =11, sticky = W,column = 4)

    def get_input_and_get_token(self):
        cid = self.cid_txt.get()
        secret = self.cs_txt.get()
        un = self.un_txt.get()
        pw = self.pw_txt.get()
        eid = self.eid_txt.get()
        
        thisdict = {
        "cid": cid,
        "secret": secret,
        "username": un,
        "password": pw,
        "eid" : eid
        }
  
        self.userInfo = thisdict
        self.get_token(self.userInfo)
        self.access_token_input.configure(text = self.access_token)

    def get_token(self,userInfo):
        
        url = f'https://api.splashthat.com/oauth/v2/token?client_id={userInfo["cid"]}&client_secret={userInfo["secret"]}&grant_type=password&scope=user&username={userInfo["username"]}&password={userInfo["password"]}'
        try:
            response = requests.get(url)
            #print(response)
            #print(response.json())
            #print(response.json()["access_token"])
            self.access_token = response.json()["access_token"]
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
        finally:
            print("this is the finally self token")
            print(self.access_token)

    def get_group_contactIDs(self):
        #use access token and userinfo
        url = f'https://api.splashthat.com/groupcontacts?event_id={self.userInfo["eid"]}&access_token={self.access_token}&limit=250'
        currGroupContacts = []
        try:
            response = requests.get(url)
        
            jsonContacts = response.json()['data']
            for gc in jsonContacts:
                currGroupContacts.append(gc['id'])
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.
        finally:
            return currGroupContacts
            
    def hash_the_emails(self):
        groupContactIDs = self.get_group_contactIDs()
        #print(groupCons)
        for gc in groupContactIDs:
            url = "https://api.splashthat.com/groupcontact/"+ str(gc)
            try:
                querystring = {"access_token":self.access_token}
                payload = "{\n  \"status\": \"rsvp_yes\",\n  \"confirmation_email\": 0,\n  \"email\":\"oooOOOoolatenow@XXXXX.com\",\n  \"last_name\": \"XXXX\",\n  \"first_name\": \"XXXXXXXX\"\n}"
                headers = {
                    'ajax': "null",
                    'X-Requested-With': "XMLhttpRequest",
                    'Content-Type': "application/json",
                    'cache-control': "no-cache",
                    'Postman-Token': "0a7d2f37-57ca-4c74-8499-9dfc2ab1befb"
                }
                response = requests.request("PUT", url, data=payload, headers=headers, params=querystring)
                #response = requests.get(url)
                #print(response)
                #print(response.json()['data'])
                #responseJSON = json.loads(response.json())
            
            # If the response was successful, no Exception will be raised
                #response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.
                continue
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
                continue
            else:
                print('Success!')
                continue
    
    def generate_link_to_event(self):
        pass


        
