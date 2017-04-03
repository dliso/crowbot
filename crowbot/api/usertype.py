def beep():
    return 'Student'

class USERTYPE:
    bot        = 'Bot'
    instructor = 'Instructor'
    student    = 'Student'
    anonymous  = 'Anonymous'

    @classmethod
    def from_profile_role(cls, role):
        if role == 1:
            return cls.student
        elif role == 2:
            return cls.instructor
        else:
            return cls.anonymous

