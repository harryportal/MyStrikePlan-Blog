from random import randint
def edit_google_username(firstname):
    random_int = randint(1,10000)
    result = firstname + str(random_int)
    return result
