class User:
    def __init__(self, firstname, lastname, occupation, education, belonging):
        self.firstname = firstname
        self.lastname = lastname
        self.occupation = occupation
        self.education = education
        self.belonging = belonging

    def Firstname(self):
        return "{} ".format(self.firstname)

    def Lastname(self):
        return "{}".format(self.lastname)

    def Occupation(self):
        return "{}".format(self.occupation)

    def Education(self):
            return "{} ".format(self.education)

    def Belonging(self):
        return "{} ".format(self.belonging)
