from django.urls import path, re_path

from auths.models import Staff
from . import web


urlpatterns = [
    path("TEST0109", web.ChangePassword.as_view(), name="test"),
    path("login", web.LoginView1.as_view(), name="login"),

    path("login", web.LoginView1.as_view(), name="login_user"),

    path("mob-login-code", web.LoginCode.as_view(), name="mob_login_code"),
    path("mob-auth-code", web.LoginAuthCode.as_view(), name="mob_auth_code"),

    path("login", web.LoginView1.as_view(), name="login-user"),
    path("logout", web.Auths.logout, name="logout"),
    path("logout", web.Auths.logout, name="logout_user"),

    path(
        "add-default-password",
        web.Auths.set_default_password,
        name="add-default-password",
    ),
    re_path(
        r"^(?P<pk>[\w-]+)/change-password",
        web.UpdateUserChangePassword.as_view(),
        name="change_password",
    ),

    path("add-staff", web.Staff.create_staff, name="add-staff"),
    path("add-user", web.Staff.create_user, name="add-user"),

    path("staff-members", web.Staff.get_staffs, name="staff-members"),
    path("inactive-staff-members", web.Staff.get_staffs_inactive, name="inactive-staff-members"),
    re_path(r"^(?P<pk>[\w-]+)/user-edit$",web.UpdateUserCvB.as_view(),name="update_user"),
    re_path(
        r"^edit-staff/(?P<staff_id>[\w-]+)/$",
        web.Staff.edit_staff,
        name="edit-staff",
    ),
    re_path(
        r"^delete-staff/(?P<staff_id>[\w-]+)/$",
        web.Staff.delete_staff,
        name="delete-staff",
    ),
    path("roles", web.Role.get_roles, name="roles"),
    #path("roles", web.CreateRole.as_view(), name="roles"),

    path("inactiveroles", web.Role.get_roles_inactive, name="inactiveroles"),
    #path("add-role", web.Role.add_role, name="add-role"),
    path("add-role", web.CreateRole.as_view(), name="add-role"),
    re_path(r"^edit-role/(?P<role_id>[\w-]+)/$",
        web.Role.edit_role,
        name="edit-role1",
    ),
    re_path(r"^detail-role/(?P<role_id>[\w-]+)/$",
            web.Role.get_role_details,
            name="role-details",
        ),

    re_path(
        r"^delete-role/(?P<role_id>[\w-]+)/$",
        web.Role.delete_role,
        name="delete-role",
    ),
    re_path(r'^perm-required$', web.PermissionRequired.as_view(), name='permission_required'),
    re_path(r'^no-permission$',web.NoPermission.as_view(),name='no_permission'),
    re_path(r'^permissions$', web.PermissionsList.as_view(), name='permissions'),
    re_path(r'^new-permission$', web.CreatePermission.as_view(), name='new_permission'),
    re_path(r'^editrole/(?P<pk>[0-9]+)/update$', web.UpdateRole.as_view(), name='edit-role'),
    re_path(r'^permission/(?P<pk>[0-9]+)/update$', web.UpdatePermission.as_view(), name='update_permission'),
    re_path(r'^permission/(?P<pk>[0-9]+)/delete$', web.PermissionDelete.as_view(), name='delete_permission'),
]
