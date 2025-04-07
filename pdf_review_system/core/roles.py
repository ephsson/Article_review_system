class RoleBase:
    """Tüm rollerin ortak soyut sınıfı"""
    def __init__(self, user):
        self.user = user

    def can_access_submission(self, submission):
        raise NotImplementedError("Bu method alt sınıflarda tanımlanmalı.")
    
class Editor(RoleBase):
    def can_access_submission(self, submission):
        # Editor her submission'a erişebilir
        return True

    def can_assign_judge(self):
        return True

    def can_edit_notes(self):
        return True
    
class Judge(RoleBase):
    def can_access_submission(self, submission):
        # Hakem sadece kendisine atanmış dosyaları görebilir
        return submission.assigned_judge == self.user

    def can_edit_notes(self):
        return True

    def can_assign_judge(self):
        return False
    
    
def get_role_for_user(user):
    if user.role == "editor":
        return Editor(user)
    elif user.role == "judge":
        return Judge(user)
    else:
        return None  # writer veya anonim kullanıcılar
