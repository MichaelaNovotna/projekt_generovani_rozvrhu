import pandas as pd
import pprint
import os


# INPUT LOADING


from input_loading import load_students, load_lectors
from classes_module import Kurz

students = load_students("input/students_availability.csv")

lectors = load_lectors("input/lectors_availability.csv")

courses = []


# FUNCTION FOR SCHEDULE GENERATING

def _make_dict_courses():
    """returns a dict where key is course and value is 
    a list of all students who want to study this particular course"""
    dict_of_courses = {}
    for student in students:
        course = student.course
        if course not in dict_of_courses.keys():
            dict_of_courses[course] = [student]
        else:
            dict_of_courses.get(course).append(student)
    return dict_of_courses


def _make_dict_main(dict_of_courses):
    """returns a dict where key is course and value is a nested dict,
    in which key is time and value is a list of students from the 
    particular course that are available at that time"""
    dict_course_time_students = {}
    for kurz, students in dict_of_courses.items():
        new_dict = {}
        for student in students:
            for hodina, TF in student.mozne_hodiny.items():
                if TF:
                    if hodina not in new_dict.keys():
                        new_dict[hodina] = [student]
                    else:
                        new_dict.get(hodina).append(student)
        dict_course_time_students[kurz] = new_dict
    return dict_course_time_students


def _lektor_available(cas):
    """checks whether at least one of the lectors is available
    at the time and returns bool"""
    TF = False
    for lektor in lectors:
        TF = lektor.mozne_hodiny[cas]
        if TF:
            return True
    return TF


def _longest_in_dict(dict):
    """input is dict with key as lesson and value as list
    of available students"""
    """returns a dict of times when the most of students from
    the particular course is available and the list of these students"""
    nejdelsi = 0
    slovnik_casu_a_seznam_studentu = {}
    for key in dict.keys():
        TF = _lektor_available(key)
        if TF:
            podseznam_studenti = dict.get(key)
            if len(podseznam_studenti) > nejdelsi:
                nejdelsi = len(podseznam_studenti)
                slovnik_casu_a_seznam_studentu = {}
                slovnik_casu_a_seznam_studentu[key] = podseznam_studenti
            elif len(podseznam_studenti) == nejdelsi:
                slovnik_casu_a_seznam_studentu[key] = podseznam_studenti
    return slovnik_casu_a_seznam_studentu


def _make_dict_of_courses_and_possible_times(dict_course_time_students):
    """creates a dict where key is course and value is nested dict,
    in which key is time when most of students is available and value 
    is the students available. ALso checks whether lector are available
    and returns only times when yes"""
    dict_of_courses_and_possible_times = {}
    for key, value in dict_course_time_students.items():
        dict_of_times = _longest_in_dict(value)
        dict_of_courses_and_possible_times[key] = dict_of_times
    return dict_of_courses_and_possible_times


def rearrange_dict(dict):
    """function rearranges dict - first go the courses
    with the least possibilities to choose from"""
    sorted_dict = {}
    for i in range(26):
        for klic, hodnota in dict.items():
            if len(hodnota) == i:
                sorted_dict[klic] = hodnota
    return sorted_dict


def _course_not_in_schedule(kurz):
    """checks whether at least one lector is available
    at the time and returns bool"""
    for lektor in lectors:
        if kurz in lektor.schedule.values():
            return False
    return True


def _register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz):
    for i in range(len(lectors)):
        # pokud kurz ještě není v rozvrhu lektoru
        if _course_not_in_schedule(kurz + str(varka)):
            # if True (jestli lektor v dany cas muze; je uprednostnen lektor 1)
            if lectors[i].mozne_hodiny[cas]:
                # pokud čas v rozvrhu ještě není obsazený
                if lectors[i].schedule[cas] == "":
                    # pridej do schedule lektora kurz
                    lectors[i].schedule[cas] = kurz + str(varka)
                    course = Kurz(kurz, kurz + str(varka), cas, lectors[i], studenti_konkr_kurz)
                    courses.append(course)
                    for student in studenti_konkr_kurz:  #add attributes
                        student.cas_kurzu = cas
                        student.jeho_kurz = kurz + str(varka)
                        student.jeho_lektor = lectors[i]


def main_algorithm(dict, varka):
    for kurz, cas_studenti in dict.items():           # cas_studenti is nested dict, therefore is opened on next line
        for cas, studenti_konkr_kurz in cas_studenti.items():     # time and list of students e.g. "monday 13:00": [Student 1, Student 2, ...]
            _register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)


def find_next_longest(kurz, varka, dict):
    slovnik_moznych_casu_kurzu = dict[kurz]        # extract dict for one particular course, put it in a new dict
    nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)       # find the longest options in new dict
    for cas in nejdelsi.keys():
        del slovnik_moznych_casu_kurzu[cas]      # delete longest from new dict
    dalsi_nejdelsi = _longest_in_dict(slovnik_moznych_casu_kurzu)
    for cas, studenti_konkr_kurz in dalsi_nejdelsi.items():       # je v něm čas a seznam studentu napr. "pondeli 13:00": [Student 1, Student 2, ...]
        _register_course_to_lector_student(kurz, cas, varka, studenti_konkr_kurz)


def _look_for_next(kurz, varka, dict_course_time_students, opakovani):
    """searches for other intersections among the rest of students"""
    find_next_longest(kurz, varka, dict_course_time_students)
    if _course_not_in_schedule(kurz + str(varka)):  # if tried all lectors and times and course still not there:
        if opakovani < 10:
            opakovani += 1
            _look_for_next(kurz, varka, dict_course_time_students, opakovani)


def all_students_placed(kurz):
    for student in students:
        if student.course == kurz and student.jeho_kurz == "":
            return False
    return True


def the_rest(dict_of_courses):
    """finds students which are not placed yet and 
    puts them into dict where key is course and value is list
    of students from this course not placed yet"""
    the_rest = {}
    for kurz, seznam_studenti in dict_of_courses.items():
        students = []
        for student in seznam_studenti:
            if student.cas_kurzu == "":
                students.append(student)
        the_rest[kurz] = students
    return the_rest


def make_final_dict():
    """makes final nested dict = lector: time: course: list od students"""
    final_dict = {}
    for lektor in lectors:
        zaverecny_slovnik = {}
        for cas, kurz in lektor.schedule.items():
            if lektor.schedule[cas] != "":
                kurz = lektor.schedule[cas]
                nested_slovnik = {}
                for student in students:
                    if student.jeho_kurz == kurz:
                        if kurz not in nested_slovnik.keys():
                            nested_slovnik[kurz] = [student]
                        else:
                            nested_slovnik.get(kurz).append(student)
                zaverecny_slovnik[cas] = nested_slovnik
        final_dict[lektor] = zaverecny_slovnik
    return final_dict


def _go_through_courses(course, cas, ucitel):
    for kurz in courses:
        for student in kurz.seznam_studentu:
            if str(student.course) in str(course) and student.mozne_hodiny[cas]:
                if str(kurz.original) in str(course):
                    for leccion in courses:
                        if str(leccion) == str(course):
                            pocet_zaku = len(leccion.seznam_studentu)
                            if len(kurz.seznam_studentu) > pocet_zaku and student.jeho_kurz != course:
                                    kurz.seznam_studentu.remove(student)
                                    student.cas_kurzu = cas
                                    student.jeho_kurz = course
                                    student.jeho_lektor = ucitel
                                    leccion.seznam_studentu.append(student)


def regroup_students(final_dict):
    """regroups students in courses into equally large groups"""
    for i in range(7):
        for ucitel, vse in final_dict.items():
            for cas, slovnik in vse.items():
                for course, seznam_st in slovnik.items():
                    if i == len(seznam_st):
                        _go_through_courses(course, cas, ucitel)


def print_to_html():
    data = []
    for i in range(len(lectors)):
        data = lectors[i].schedule
        df = pd.DataFrame(data, index=[""])
        df = df.fillna('').T
        df.to_html("output_lector" + str(i) + ".html")
        os.startfile("output_lector" + str(i) + ".html")


def make_schedule():
    """calls all functions in order to create the final
    nested dict and prints it to html"""
    dict_of_courses = _make_dict_courses()
    for varka in range(1, 10):
        dict_course_time_students = _make_dict_main(dict_of_courses)
        dict_of_courses_and_possible_times = _make_dict_of_courses_and_possible_times(dict_course_time_students)
        dict_of_courses_and_possible_times = rearrange_dict(dict_of_courses_and_possible_times)
        main_algorithm(dict_of_courses_and_possible_times, varka)
        for kurz, cas_studenti in dict_of_courses_and_possible_times.items():
            if not all_students_placed(kurz):
                if _course_not_in_schedule(kurz + str(varka)):  # if tried all lectors and times and course still not there
                    _look_for_next(kurz, varka, dict_course_time_students, opakovani=0)
        dict_of_courses = the_rest(dict_of_courses)
    for student in students:
        if student.jeho_kurz == "":
            print(str(student) + " belonging to course " + str(student.course) + " is impossible to place.")

    print_to_html()

    # final dict, for each lector = lector: time: course: list of students
    final_dict = make_final_dict()

    # division by numbers of students in course - the aim is equal combination
    regroup_students(final_dict)

    # final dict again for print
    final_dict = make_final_dict()
    pprint.pprint(final_dict)


make_schedule()