# not using
import app.baseAccount

class Vendor(app.baseAccount.User):
    def __init__(self, name, address, email,password,mobile) -> None:
        super().__init__(name, address, email, password, mobile)


    # def get_name(self):
    #     return self.__name
    # def get_address(self):
    #     return self.__address
    # def get_email(self):
    #     return self.__email
    # def get_password(self):
    #     return self.__password
    # def get_mobile(self):
    #     return self.__mobile
    # def set_name(self, name):
    #     self.__name = name
    # def set_address(self,address):
    #     self.__address = address
    # def set_email(self,email):
    #     self.__email = email
    # def set_pass(self,password):
    #     self.__password = password
    # def set_mobile(self,mobile):
    #     self.__mobile = mobile
