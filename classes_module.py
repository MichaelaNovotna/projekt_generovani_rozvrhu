class Person:
    def __init__(self, name, course, mozne_hodiny):
        self.name = name
        self.course = course
        self.mozne_hodiny = mozne_hodiny

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


class Student(Person):
    
    def __init__(self, name, course, mozne_hodiny, cas_kurzu, jeho_kurz, jeho_lektor):
        Person.__init__(self, name, course, mozne_hodiny)
        self.cas_kurzu = cas_kurzu
        self.jeho_kurz = jeho_kurz
        self.jeho_lektor = jeho_lektor


class Lektor(Person):
    
    def __init__(self, name, course, mozne_hodiny, schedule):
        Person.__init__(self, name, course, mozne_hodiny)
        self.schedule = schedule


class Kurz():

    def __init__(self, original, name, cas, lektor, seznam_studentu):
        self.original = original
        self.name = name
        self.cas = cas
        self.lektor = lektor
        self.seznam_studentu = seznam_studentu
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

