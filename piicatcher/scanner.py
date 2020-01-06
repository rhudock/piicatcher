"""Different types of scanners for PII data"""
from abc import ABC, abstractmethod
from .commonregex import CommonRegex
import logging
import re
import spacy
import scispacy

from piicatcher.piitypes import PiiTypes


# pylint: disable=too-few-public-methods
class Scanner(ABC):
    """Scanner abstract class that defines required methods"""

    @abstractmethod
    def scan(self, text, data_db, ref):  # data_db being used to track results so I can write them to a database
        """Scan the text and return an array of PiiTypes that are found"""


class RegexScanner(Scanner):
    """A scanner that uses common regular expressions to find PII"""

    def scan(self, text, data_db, ref):
        """Scan the text and return an array of PiiTypes that are found"""
        regex_result = CommonRegex(text)
        types = []
        if regex_result.phones:  # pylint: disable=no-member
            data_db.append(["PHONE", text, "N/A", "N/A", ref])
            types.append(PiiTypes.PHONE)
        if regex_result.emails:  # pylint: disable=no-member
            data_db.append(["EMAIL", text, "N/A", "N/A", ref])
            types.append(PiiTypes.EMAIL)
        if regex_result.credit_cards:  # pylint: disable=no-member
            data_db.append(["CREDIT_CARD", text, "N/A", "N/A", ref])
            types.append(PiiTypes.CREDIT_CARD)
        if regex_result.street_addresses:  # pylint: disable=no-member
            data_db.append(["ADDRESS", text, "N/A", "N/A", ref])
            types.append(PiiTypes.ADDRESS)
        if regex_result.icd10_codes:  # pylint: disable=no-member
            data_db.append(["ICDTEN", text, "N/A", "N/A", ref])
            types.append(PiiTypes.ICDTEN)
        if regex_result.icd9_codes:  # pylint: disable=no-member
            data_db.append(["ICDNINE", text, "N/A", "N/A", ref])
            types.append(PiiTypes.ICDNINE)
        if regex_result.ssn_number:  # pylint: disable=no-member
            data_db.append(["SSN", text, "N/A", "N/A", ref])
            types.append(PiiTypes.SSN)
        if regex_result.amex:
            data_db.append(["AMEX", text, "N/A", "N/A", ref])
            types.append(PiiTypes.AMEX)
        if regex_result.visa:
            data_db.append(["VISA", text, "N/A", "N/A", ref])
            types.append(PiiTypes.VISA)
        if regex_result.mastercard:
            data_db.append(["MASTERCARD", text, "N/A", "N/A", ref])
            types.append(PiiTypes.MASTERCARD)
        if regex_result.tax:
            data_db.append(["TAX", text, "N/A", "N/A", ref])
            types.append(PiiTypes.TAX)
        if regex_result.medical_doctor:
            data_db.append(["MEDICAL_DOCTOR", text, "N/A", "N/A", ref])
            types.append(PiiTypes.MEDICAL_DOCTOR)
        if regex_result.bank_transfer:
            data_db.append(["BANK_TRANSFER", text, "N/A", "N/A", ref])
            types.append(PiiTypes.BANK_TRANSFER)
        if regex_result.medical_records:
            data_db.append(["MEDICAL_RECORDS", text, "N/A", "N/A", ref])
            types.append(PiiTypes.MEDICAL_RECORDS)
        if regex_result.treatment_terms:
            data_db.append(["TREATMENT", text, "N/A", "N/A", ref])
            types.append(PiiTypes.TREATMENT)
        if regex_result.california:
            data_db.append(['CA_DL', text, "N/A", "N/A", ref])
        if regex_result.common_drugs:
            data_db.append(['COMMON_DRUGS', text, "N/A", "N/A", ref])
        if regex_result.diagnosis:
            data_db.append(['DIAGNOSIS', text, "N/A", "N/A", ref])
        return types


class NERScanner(Scanner):
    """A scanner that uses Spacy NER for entity recognition.
        see https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/"""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.max_length = 100000000
        self.nlp2 = spacy.load("en_ner_bc5cdr_md")
        # pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_ner_craft_md-0.2.4.tar.gz
        # pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_core_sci_sm-0.2.4.tar.gz
        self.nlp2.max_length = 100000000
        self.nlp3 = spacy.load("en_ner_bionlp13cg_md")
        self.nlp3.max_length = 100000000

    def scan(self, text, data_db, ref):
        """Scan the text and return an array of PiiTypes that are found"""
        print("Processing '{}'".format(ref))
        doc = self.nlp(text)
        types = set()
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                types.add(PiiTypes.PERSON)
                data_db.append([ent.label_, ent.text, ent.start_char, ent.end_char, ref])

            if ent.label_ == 'GPE':
                types.add(PiiTypes.LOCATION)
                data_db.append([ent.label_, ent.text, ent.start_char, ent.end_char, ref])

        logging.debug("PiiTypes are {}".format(list(types)))

        # look for medical terms
        doc = self.nlp2(text)
        for ent in doc.ents:
            if ent.label_ == 'DISEASE':
                types.add(PiiTypes.DISEASE)
                data_db.append([ent.label_, ent.text, ent.start_char, ent.end_char, ref])
        doc = self.nlp3(text)
        for ent in doc.ents:
            if ent.label_ == 'CANCER' or 'ORGAN' or 'TISSUE' or 'CELL' or 'ANATOMICAL_SYSTEM':
                types.add(PiiTypes.CANCER)
                data_db.append([ent.label_, ent.text, ent.start_char, ent.end_char, ref])
            # print(ent, ent.label_)
        return list(types)


class ColumnNameScanner(Scanner):
    regex = {
        PiiTypes.PERSON: re.compile("^.*(firstname|fname|lastname|lname|"
                                    "fullname|fname|maidenname|_name|"
                                    "nickname|name_suffix|name).*$", re.IGNORECASE),
        PiiTypes.EMAIL: re.compile("^.*(email|e-mail|mail).*$", re.IGNORECASE),
        PiiTypes.BIRTH_DATE: re.compile("^.*(date_of_birth|dateofbirth|dob|"
                                        "birthday|date_of_death|dateofdeath).*$", re.IGNORECASE),
        PiiTypes.GENDER: re.compile("^.*(gender).*$", re.IGNORECASE),
        PiiTypes.NATIONALITY: re.compile("^.*(nationality).*$", re.IGNORECASE),
        PiiTypes.ADDRESS: re.compile("^.*(address|city|state|county|country|"
                                     "zipcode|postal|zone|borough).*$", re.IGNORECASE),
        PiiTypes.USER_NAME: re.compile("^.*user(id|name|).*$", re.IGNORECASE),
        PiiTypes.PASSWORD: re.compile("^.*pass.*$", re.IGNORECASE),
        PiiTypes.SSN: re.compile("^.*(ssn|social).*$", re.IGNORECASE)
    }

    def scan(self, text):
        types = set()
        for pii_type in self.regex.keys():
            if self.regex[pii_type].match(text) is not None:
                types.add(pii_type)

        print("PiiTypes are {}".format(list(types)))
        return list(types)
