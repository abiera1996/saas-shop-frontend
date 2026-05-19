from django.shortcuts import redirect, reverse
from django.contrib.auth.models import User

 

def require_not_logged(function):
    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated: 
            return redirect(reverse('user:dashboard'))

        return function(request, *args, **kwargs) 

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


class require_logged(object):

    """
        Role Codes
        - patient = PTNT_1
        - admin = DMN_1
        - clinic branch = CLNCBRNCH_1
        - employee = MPLY_1
        - system user = SYSTMSR_1

        view is available to all roles, if roles is empty array.
    """
    def __init__(self, roles=[], permission_code=None):
        self.roles = roles
        self.permission_code = permission_code
        
    def __call__(self, original_func):
        def wrap(request, *args, **kwargs): 
            if request.user.is_authenticated:
                if hasattr(request.user, 'profile'):
                    permissions = request.user.profile.get_user_has_permission()  
                    if self.permission_code:
                        if self.permission_code not in permissions:
                            return redirect('user:dashboard') 
                        
                    # role_code = request.user.profile.role.role_code
                    # if self.roles:
                    #     if role_code not in self.roles:
                    #         return redirect('user:dashboard') 
                    return original_func(request, *args, **kwargs)
            return redirect('main:logout') 
        return wrap