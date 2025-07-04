from rest_framework.permissions import BasePermission


# Basic single-flag permissions
class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


# AND combinator permission: all must be True
class AndPermission(BasePermission):
    def __init__(self, *perms):
        self.perms = perms

    def has_permission(self, request, view):
        return all(perm().has_permission(request, view) for perm in self.perms)


# OR combinator permission: at least one must be True
class OrPermission(BasePermission):
    def __init__(self, *perms):
        self.perms = perms

    def has_permission(self, request, view):
        return any(perm().has_permission(request, view) for perm in self.perms)


# Convenience pre-built permissions for common AND combos
class IsActiveStaffUser(AndPermission):
    def __init__(self):
        super().__init__(IsActiveUser, IsStaffUser)


class IsActiveSuperUser(AndPermission):
    def __init__(self):
        super().__init__(IsActiveUser, IsSuperUser)


class IsStaffSuperUser(AndPermission):
    def __init__(self):
        super().__init__(IsStaffUser, IsSuperUser)


class IsActiveStaffSuperUser(AndPermission):
    def __init__(self):
        super().__init__(IsActiveUser, IsStaffUser, IsSuperUser)


# Convenience pre-built permissions for common OR combos
class IsActiveOrStaffUser(OrPermission):
    def __init__(self):
        super().__init__(IsActiveUser, IsStaffUser)


class IsActiveOrSuperUser(OrPermission):
    def __init__(self):
        super().__init__(IsActiveUser, IsSuperUser)


class IsStaffOrSuperUser(OrPermission):
    def __init__(self):
        super().__init__(IsStaffUser, IsSuperUser)


class IsActiveOrStaffOrSuperUser(OrPermission):
    def __init__(self):
        super().__init__(IsActiveUser, IsStaffUser, IsSuperUser)


# --- Usage examples ---

# Use any of these as your ViewSet permission_classes, for example:

# 1) Allow only users who are both active AND staff:
# permission_classes = [IsActiveStaffUser]

# 2) Allow users who are active OR staff:
# permission_classes = [IsActiveOrStaffUser]

# 3) Allow users who are active AND staff AND superuser:
# permission_classes = [IsActiveStaffSuperUser]

# 4) Allow users who are active OR staff OR superuser:
# permission_classes = [IsActiveOrStaffOrSuperUser]

# 5) Or combine dynamically inline (for advanced use cases):
# permission_classes = [AndPermission(IsActiveUser, IsStaffUser)]
# permission_classes = [OrPermission(IsActiveUser, IsSuperUser)]
