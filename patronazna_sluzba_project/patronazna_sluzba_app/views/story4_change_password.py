from . import story2_create_pacient
from patronazna_sluzba_app.models import *

#OLD: SPREMEMBA GESLA
def change_password(pass1, pass2, id):
    if story2_create_pacient.check_passwords(pass1, pass2):
        user = User.objects.get(username=id)
        user.set_password(pass1)
        user.save()
        return 1
    return 0

