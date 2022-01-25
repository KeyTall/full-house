import doctest

class Student:
    """ Student with unique id (sid) and current grade (grade)"""

    def __init__(self, sid: str, grade: int) -> None:
        """ initializes an instance of a Student with sid and grade
        >>> stdnt = Student('V00123456', 89)
        """
        self.__sid = sid
        self.__grade = grade

    def __str__(self) -> str:
        """ return a formatted string with sid and grade of self Student
        >>> stdnt = Student('V00123456', 89)
        >>> str(stdnt)
        'V00123456: 89/100'
        """
        return '{}: {}/100'.format(self.__sid, self.__grade)

    def __repr__(self) -> str:
        """ return a formatted string  with student attributes
        >>> stdnt = Student('V00123456', 89)
        >>> repr(stdnt)
        "Student('V00123456', 89)"
        """        
        return "Student('{}', {})".format(self.__sid, self.__grade)
    
    def __eq__(self, other: 'Student') -> bool:
        '''
        >>> stdnt_1 = Student('V00123456', 89)
        >>> stdnt_2 = Student('V00123456', 89)
        >>> stdnt_3 = Student('V00654321', 70)
        >>> stdnt_1 == stdnt_1
        True
        >>> stdnt_1 == stdnt_2
        True
        >>> stdnt_2 == stdnt_3
        False
        '''
        return self.__grade == other.__grade and self.__sid == other.__sid
    
    # TODO: add documentation for these instance methods
    def get_sid(self) -> str:
        '''
        >>> stdnt = Student('V00123456', 89)
        >>> stdnt.get_sid()
        'V00123456'
        '''
        return self.__sid

    def get_grade(self) -> int:
        '''
        >>> stdnt = Student('V00123456', 89)
        >>> stdnt.get_grade()
        89
        '''
        return self.__grade

    def set_grade(self, grade) -> None:
        '''
        >>> stdnt = Student('V00123456', 89)
        >>> stdnt.set_grade(10)
        '''
        self.__grade = grade
    
    def is_grade_above(self, threshold: int) -> bool:
        '''
        >>> stdnt = Student('V00123456', 89)
        >>> stdnt.is_grade_above(80)
        True
        >>> stdnt.is_grade_above(89)
        False
        >>> stdnt.is_grade_above(95)
        False
        '''
        return self.__grade > threshold
