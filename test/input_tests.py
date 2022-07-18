import pytest
from modul_nacteni_vstupu import nacti
from modul_tridy import Student, Lektor


def test_nacteni_s():
    soubor = "vstup_var2_studenti.csv"
    je_student = True
    result = nacti(soubor, je_student)
    assert len(result) > 0


def test_list_s():
    soubor = "vstup_var2_studenti.csv"
    je_student = True
    result = nacti(soubor, je_student)
    assert type(result) is list


def test_typ_tridy_s():
    soubor = "vstup_var2_studenti.csv"
    je_student = True
    result = nacti(soubor, je_student)
    maximum = len(result)
    assert isinstance(result[3], Student)
    if 15 < maximum:
        assert isinstance(result[15], Student)
    if 26 < maximum:
        assert isinstance(result[26], Student)
    if 33 < maximum:
        assert isinstance(result[33], Student)
    assert isinstance(result[maximum - 1], Student)
    with pytest.raises(IndexError):
        isinstance(result[maximum], Student)


def test_trida_s():
    soubor = "vstup_var2_studenti.csv"
    je_student = True
    result = nacti(soubor, je_student)
    kurzy = ["cae", "fce", "ie", "pet", "key"]
    for student in result:
        assert student.name is not None
        assert student.course is not None
        assert student.course in kurzy
        assert student.mozne_hodiny is not None

def test_slovnik_s():
    soubor = "vstup_var2_studenti.csv"
    je_student = True
    result = nacti(soubor, je_student)
    kurzy = ["cae", "fce", "ie", "pet", "key"]
    for student in result:
        slovnik = student.mozne_hodiny
        for klic in slovnik.keys():
            assert klic is not None
        seznam_hodnot = []
        for dostupny in slovnik.values():
            assert dostupny is not None
            assert type(dostupny) == bool
            assert dostupny or not dostupny
            seznam_hodnot.append(dostupny)
        assert True in seznam_hodnot        # student je dostupny alespon 1 hodinu tydne


def test_nacteni_l():
    soubor = "vstup_lektori.csv"
    je_student = False
    result = nacti(soubor, je_student)
    assert len(result) > 0


def test_list_l():
    soubor = "vstup_lektori.csv"
    je_student = False
    result = nacti(soubor, je_student)
    assert type(result) is list


def test_tridy_l():
    soubor = "vstup_lektori.csv"
    je_student = False
    result = nacti(soubor, je_student)
    assert isinstance(result[0], Lektor)
    assert isinstance(result[1], Lektor)
    assert not isinstance(result[0], Student)

def test_trida_l():
    soubor = "vstup_lektori.csv"
    je_student = False
    result = nacti(soubor, je_student)
    for lektor in result:
        assert lektor.name is not None
        assert lektor.course is not None
        assert lektor.course == "vse"
        assert lektor.mozne_hodiny is not None


def test_slovnik_l():
    soubor = "vstup_lektori.csv"
    je_student = False
    result = nacti(soubor, je_student)
    for lektor in result:
        slovnik = lektor.mozne_hodiny
        for klic in slovnik.keys():
            assert klic is not None
        seznam_hodnot = []
        for dostupny in slovnik.values():
            assert dostupny is not None
            assert type(dostupny) == bool
            assert dostupny or not dostupny
            seznam_hodnot.append(dostupny)
        assert True in seznam_hodnot


if __name__ == "__main__":
    pytest.main()