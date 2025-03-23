from auths.models import User

def _can_update_payment_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_update_payment_request').exists():
                return True
    return False

def _can_review_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_review_payment_request').exists():
                return True
    return False

def _can_approve_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_approve_payment_request').exists():
                return True
    return False

def _can_authorize_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_authorize_payment_request').exists():
                return True
    return False

def _action_on_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__in=['can_approve_payment_request','can_authorize_payment_request']).exists():
                return True
    return False

def _can_manage_account(user):

    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='manage_account').exists():
                return True
    return False

def _can_manage_institution(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='manage_institution').exists():
                return True
    return False

def _can_create_payment_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_create_payment_request').exists():
                return True
    return False

def _can_update_payment_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_update_payment_request').exists():
                return True
    return False

def _can_delete_payment_request(user):
    if user.role:
        if user.role.perm:
            if user.role.perm.filter(perm_name__iexact='can_delete_payment_request').exists():
                return True
    return False

