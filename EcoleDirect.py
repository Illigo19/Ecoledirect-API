import requests
import json
import datetime 

class EcoleDirect:
    """ Permet de se connecter et faire des requetes a l'API d'école direct
    Allow to connect and make requests to Ecoledirect's API """


    def __init__(self, username = None, password = None):
        """Create a new EcoleDirect object"""

        self.token = None
        self.id = None
        if username is not None and password is not None:
            self.connect(username, password)
        

    def __req(self, url, payload):
        """this function make all requests to the api"""
        return requests.post(url, data = payload)


    def connect(self, username : str, password : str):
        """create an connection to the API"""

        connection = self.__req('https://api.ecoledirecte.com/v3/login.awp', """data={}"identifiant": "{}","motdepasse": "{}"{}""".format("{",username, password, "}"))
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            self.token = connection.json()['token']
            self.id = connection.json()['data']['accounts'][0]['id']
            
    

    def getWT(self, startDate = datetime.date.today().strftime("%Y-%m-%d"), endDate = (datetime.date.today() + datetime.timedelta(days=6) ).strftime("%Y-%m-%d")):
        """get the work time from the api"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return

        connection = self.__req('https://api.ecoledirecte.com/v3/E/{}/emploidutemps.awp?verbe=get&'.format(self.id), """data={}"token":"{}","dateDebut": "{}","dateFin": "{}","avecTrous": false,{}""".format("{", self.token,startDate,endDate, "}"))
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            return connection.json()['data']
    

    def getHW(self):
        """get homework from the api"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return   

        connection = self.__req('https://api.ecoledirecte.com/v3/Eleves/{}/cahierdetexte.awp?verbe=get&'.format(self.id), """data={}"token":"{}"{}""".format("{", self.token, "}"))
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            return connection.json()['data']
            


    def getNotes(self):
        """get notes from the api"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return 
            
        connection = self.__req('https://api.ecoledirecte.com/v3/eleves/{}/notes.awp?verbe=get&'.format(self.id), """data={}"token":"{}"{}""".format("{", self.token, "}"))
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            return connection.json()['data']


    def getSL(self):
        """get sochlar life from the API"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return 
            
        connection = self.__req('https://api.ecoledirecte.com/v3/eleves/{}/viescolaire.awp?verbe=get&='.format(self.id), """data={}"token":"{}"{}""".format("{", self.token, "}"))
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            return connection.json()['data']

    def getCloud(self):
        """get the cloud from the API"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return 
            
        connection = self.__req('https://api.ecoledirecte.com/v3/cloud/E/{}.awp?verbe=get&='.format(self.id), """data={}"token":"{}"{}""".format("{", self.token, "}"))
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            return connection.json()['data']
        
        #news
    def GetWorkTimeById(self, ID = None,helpId = False,  startDate = datetime.date.today().strftime("%Y-%m-%d"), endDate = (datetime.date.today() + datetime.timedelta(days=6) ).strftime("%Y-%m-%d")):
        """retrieves the content of the schedule according to the name of the given dictionary key  """
        if ID == None: #checks if an ID is given
            print("error ! Id not specified")
        else:
            """like GetWT()"""

            """get the work time from the api"""
            if self.token is None or self.id is None:
                print("Error connection must be activate")
                return

            connection = self.__req('https://api.ecoledirecte.com/v3/E/{}/emploidutemps.awp?verbe=get&'.format(self.id), """data={}"token":"{}","dateDebut": "{}","dateFin": "{}","avecTrous": false,{}""".format("{", self.token,startDate,endDate, "}"))
            if connection.json()['code'] != 200:
                print("error ! bad username or password")
            else:
                # self.token = connection.json()['token']
                #retrieves the contents of all dictionaries from the given key/ID
                megaData = connection.json()['data']
                IDlist = []
                for x in range(0,len(megaData)):
                    dataDico = megaData[x]
                    IDlist.append(dataDico[ID])

                    pass
                
                #bonus : allows to give all the IDs available in the schedule to the devs : obj.GetWorkTimeById("matiere", True)
                if helpId:
                    exemple = megaData[x]
                    print("ID available : \n")
                    for cle,valeur in exemple.items():
                        print(cle) #give ID
                    pass
                return IDlist
            
            
    def getMessage(self):
        """get messagerie from the API"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return 
            
        
        connection = self.__req('https://api.ecoledirecte.com/v3/eleves/{}/messages.awp?verbe=getall&'.format(self.id),"""data={}"token":"{}"{}""".format("{", self.token, "}"))
        
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            return connection.json()['data']

    def getMessageById(self, ID = None, classe = None): # ID is the key content, classe is the class holds the message : received, sent
        """get key of Message => exemple : "subject", "id" """
        if ID == None:
            print("error ! Id not specified")
        else:
            message = self.getMessage()
            messages = message['messages']
            try:
                classe = messages[classe]
                IdListMessage = []
                for x in range(0,len(classe)):
                    Group = classe[x]
                    IdListMessage.append(Group[ID])
                return IdListMessage

            except:
                print("error ! invalid class : ",classe," isn't valid")
                print("class valid :\n")
                for cle,valeur in messages.items():
                    print(cle)
                    pass
    def getMessageContent(self, MessageId):
        """get the content of message from the given ids, to get the ids => getMessageById('id', "received") ('received' only for received messages)"""
        if self.token is None or self.id is None:
            print("Error connection must be acitvate")
            return 
            
        
        connection = self.__req('https://api.ecoledirecte.com/v3/eleves/{}/messages/{}.awp?verbe=get&mode=destinataire'.format(self.id, MessageId),"""data={}"token":"{}"{}""".format("{", self.token, "}") )
        
        if connection.json()['code'] != 200:
            print("error ! bad username or password")
        else:
            # self.token = connection.json()['token']
            content =  connection.json()['data']
            trueContent = content['content']
            decrypte = base64.b64decode(trueContent)
            print(decrypte)
