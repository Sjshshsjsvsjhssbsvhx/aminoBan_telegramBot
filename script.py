from os import path
import sys, json
import aminofix as amino


class Init:
    def __init__(self) -> None:
        email, password, aminoId = self.auth()
        self.client = None
        self.sub_client = None
        self.authorization(email, password, aminoId)

    def init_authFile(self) -> None:
        try:
            with open("auth.json", "w", encoding= "utf-8") as File:
                json.dump(
                    {
                        "email": input("Email: "),
                        "password": input("Password: "),
                        "aminoId": input("Amino ID: ")
                    },
                    File
                )
        except OSError:
            print("@@Error! Cannot init auth file! Exit!")
            sys.exit()

    def auth(self) -> list:
        if path.isfile("auth.json") == False:
            self.init_authFile()
        elif path.isfile("auth.json") == True:
            is_true_auth_data: str = str()
            while (is_true_auth_data != "Y") and (is_true_auth_data != "N"):
                is_true_auth_data = input('Start with last settings?: "Y"/"N": ').upper()
                if (is_true_auth_data != "Y") and (is_true_auth_data != "N"):
                    print("Wrong input! Try again!")
            if is_true_auth_data == "N":
                self.init_authFile()
        try:
            with open("auth.json", "r", encoding= "utf-8") as File:
                data: dict = json.load(File)
                auth: list = [str(data.get("email")), str(data.get("password")), str(data.get("aminoId"))]
        except OSError:
            print("@@Error! Cannot read auth file! Exit!")
            sys.exit()
        return auth

    def authorization(self, email: str, password: str, aminoId: str) -> None:
        self.client = amino.Client()
        try:
            print(f"email: {email}\npassword: {password}")
            self.client.login(email, password)
            try:
                self.sub_client = amino.SubClient(aminoId= aminoId, profile= self.client.profile)
            except ConnectionError:
                print(f"@@@FATAL ERROR. Cannot login into the community.\n  Maybe you typed wrong amino ID. Check it:\n       Amino ID: {aminoId}")
                sys.exit("@@@")
        except ConnectionError:
            print(f"@@@FATAL ERROR. Cannot login into the account.\n  Maybe you trieng login with wrong email/password. Check it:\n       Email: {email}\n       Password: {password}")
            sys.exit()
 

class Amino:
    def __init__(self) -> None:
        self.privat = Init()

    def get_id(self, link: str) -> str:
        try:
            response = self.privat.sub_client.get_from_code(link).objectId
            return response
        except ConnectionError:
            return ""

    def ban(self, link: str, reason: str) -> bool:
        userId: str = self.get_id(link)
        if userId != "":
            try:
                self.privat.sub_client.ban(userId= userId, reason= reason)
                return True
            except ConnectionError:
                return False
        else:
            return False

    def unban(self, link: str, reason: str) -> bool:
        userId: str = self.get_id(link)
        if userId != "":
            try:
                self.privat.sub_client.unban(userId= userId, reason= reason)
                return True
            except ConnectionError:
                return False
        else:
            return False
    
