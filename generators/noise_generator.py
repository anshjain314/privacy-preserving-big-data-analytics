import random
import re

# -------------------------------------------------------
# Common abbreviations
# -------------------------------------------------------

ABBREVIATIONS = {
    "Customer": "Cust",
    "Number": "No",
    "Account": "Acct",
    "Employee": "Emp",
    "Department": "Dept",
    "Application": "App",
    "Transaction": "Txn",
    "Information": "Info",
    "Management": "Mgmt",
    "Contact": "Cntct",
    "Phone": "Ph",
    "Mobile": "Mob",
    "Address": "Addr",
    "Identifier": "ID"
}


# -------------------------------------------------------
# snake_case
# -------------------------------------------------------

def snake_case(name):
    return name.lower()


# -------------------------------------------------------
# UPPER_CASE
# -------------------------------------------------------

def upper_case(name):
    return name.upper()


# -------------------------------------------------------
# Title Case With Spaces
# -------------------------------------------------------

def title_case(name):
    return name.replace("_", " ")


# -------------------------------------------------------
# kebab-case
# -------------------------------------------------------

def kebab_case(name):
    return name.lower().replace("_", "-")


# -------------------------------------------------------
# PascalCase
# -------------------------------------------------------

def pascal_case(name):

    words = re.split(r"[_\s]+", name)

    return "".join(word.capitalize() for word in words)


# -------------------------------------------------------
# camelCase
# -------------------------------------------------------

def camel_case(name):

    words = re.split(r"[_\s]+", name)

    if len(words) == 1:
        return words[0].lower()

    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


# -------------------------------------------------------
# Abbreviation
# -------------------------------------------------------

def abbreviate(name):

    words = name.split("_")

    new_words = []

    for word in words:

        if word in ABBREVIATIONS:
            new_words.append(ABBREVIATIONS[word])

        else:
            new_words.append(word)

    return "_".join(new_words)


# -------------------------------------------------------
# Random Variation Generator
# -------------------------------------------------------

def generate_variations(name):

    variations = {

        name,

        snake_case(name),

        upper_case(name),

        title_case(name),

        kebab_case(name),

        camel_case(name),

        pascal_case(name),

        abbreviate(name),

        snake_case(abbreviate(name)),

        camel_case(abbreviate(name)),

        pascal_case(abbreviate(name))

    }

    return list(variations)


# -------------------------------------------------------
# Return One Random Variant
# -------------------------------------------------------

def random_variation(name):

    return random.choice(generate_variations(name))