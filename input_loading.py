from classes_module import Student, Lektor


def _pridej_do_dict_moznych_hod(nadpisy_hodin, mozne_hodiny, casove_moznosti):
    for i in range(0, 25):
        if casove_moznosti[i] == "ano":
            dostupny = True
        elif casove_moznosti[i] == "":
            dostupny = False
        mozne_hodiny[nadpisy_hodin[i]] = dostupny


def _pridej_do_dict_schedule(nadpisy_hodin, schedule):
    for i in range(0, 25):
        schedule[nadpisy_hodin[i]] = ""


def nacti(soubor, je_student):
    """loads input file line by line and divides it into columns for name, course and availability,
    and assigns each person a class (student or lector) and puts them into list"""
    list_of_people = []
    with open(soubor, encoding="utf-8") as vstup:
        line_counter = 0
        for line in vstup:
            mozne_hodiny = {}
            schedule = {}
            radek = line.strip().split(";")
            if line_counter == 0:
                nadpisy_hodin = radek[2:27]
            elif line_counter > 0:
                name = radek[0]
                course = radek[1]
                _pridej_do_dict_moznych_hod(nadpisy_hodin, mozne_hodiny, casove_moznosti=radek[2:27])
                _pridej_do_dict_schedule(nadpisy_hodin, schedule)
                if je_student:
                    clovek = Student(name, course, mozne_hodiny, cas_kurzu="", jeho_kurz="", jeho_lektor="")
                else:
                    clovek = Lektor(name, course, mozne_hodiny, schedule)
                list_of_people.append(clovek)        # append student to list of students (for class Student)
            line_counter += 1
    return list_of_people


def load_students(soubor):
    return nacti(soubor, True)


def load_lectors(soubor):
    return nacti(soubor, False)
