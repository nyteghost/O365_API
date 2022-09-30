import pickle 
import doorKey
config = doorKey.tangerine()

cwURL = 'https://api-na.myconnectwise.net/v2021_3/apis/3.0/'
cwDocURL = 'https://cloud.na.myconnectwise.net/v4_6_development/apis/3.0'
cwAURL = 'https://sca-atl.hostedrmm.com/cwa/api/v1/'
cwTEURL = 'https://api-na.myconnectwise.net/v2021_3/apis/3.0/time/entries'
cwAUTH = {'Authorization':'Basic <token>', 'clientId':'<clientid>'}


def getcwaHEADER():
        file = open('token', 'rb')
        data = pickle.load(file)
        file.close()
        for i in data:
               i
        token = "Bearer "+ i
        cwaGetHeader = {
                "Authorization":token,
                'clientId':config['cwaHeader']['clientID'],
                "Content-Type":"application/json"
                }
        return(cwaGetHeader)

def cwlogin(mfa):
    cwAloginCreds = {
            "Username":config['cwAlogin']['Username'],
            "Password":config['cwAlogin']['Password'],
            "TwoFactorPasscode":mfa
            }
    return(cwAloginCreds)
