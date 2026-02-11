def can_manage_translations(member):
    return bool(member and member.is_staff)
