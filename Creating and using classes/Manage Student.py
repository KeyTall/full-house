import doctest
from typing import List, Tuple, Dict, TextIO
from student import Student

ID    = 0
GRADE = 1

def get_students(filename: TextIO) -> List[Student]:
    '''
    Returns a list of student data as a function of Student.
    
    Precondition: file has to be formatted as each line of file has a student 
                  id and grade separated by a comma.
    
    >>> get_students('EmptyFile.csv')
    []
    >>> get_students('student_data.csv')
    [Student('V00123456', 89), Student('V00123457', 99), Student('V00123458', 30), Student('V00123459', 78)]
    '''
    #opens file and converts data to list
    file_handle = open(filename)
    student_data_list = file_handle.readlines()
    file_handle.close()
    
    #if there is no student data then remove trailing space from student_data_list 
    if len(student_data_list) == 1:
        student_data_list = []
        
    student_data = []
    
    #for each set of data
    for data in student_data_list:
        
        #remove trailing space and convert data set to list
        clean_data = data.rstrip()
        data_list  = clean_data.split(',')
        
        #get id and grade from data set
        student_id    = data_list[ID]
        student_grade = int(data_list[GRADE])
        
        #get Student instance
        student = Student(student_id, student_grade)
        
        #add Student instance to list (student_data)
        student_data.append(student)
    
    return student_data

def get_classlist(student_instances: List[Student]) -> List[str]:
    '''
    Returns a list of student ids taken from a list of Student instances.
    
    Precondition: Function ids (a student instance) have to be unique.
    
    >>> data = [Student('V00123456', 89), Student('V00123457', 99), \
    Student('V00123458', 30), Student('V00123459', 78)]
    
    >>> get_classlist([])
    []
    >>> get_classlist(data)
    ['V00123456', 'V00123457', 'V00123458', 'V00123459']
    '''
    students_ids = []
    
    #gets each student instance
    for student in student_instances:
        stdnt_id = student.get_sid()  #gets student id
        students_ids.append(stdnt_id) #adds student id to list (students_ids)
        
    return students_ids

def count_above(student_instances: List[Student], threshold_grade: int) -> List[Student]:
    '''
    Returns a list of student instances of student instances with a grade above
    the threshold grade.
    
    >>> data = [Student('V00123456', 89), Student('V00123457', 99), \
    Student('V00123458', 30), Student('V00123459', 78)]
    
    >>> count_above([], 0)
    []
    >>> count_above(data, 20)
    [Student('V00123456', 89), Student('V00123457', 99), Student('V00123458', 30), Student('V00123459', 78)]
    >>> count_above(data, 78)
    [Student('V00123456', 89), Student('V00123457', 99)]
    >>> count_above(data, 99)
    []
    '''
    students_w_grade_above = []
    
    #gets each student instance
    for student in student_instances:
        student_grade = student.get_grade() #gets grade of instance
        
        #if student grade is above thresh age then add to list (students_w_grade_above)
        if student_grade > threshold_grade: 
            students_w_grade_above.append(student)
            
    return students_w_grade_above
    
def get_average_grade(student_instaces: List[Student]) -> float:
    '''
    Returns the average grade of all students listed in student_instances.
    
    Precondition: student_instaces list cannot be empty
    
    >>> data = [Student('V00123456', 89), Student('V00123457', 99), \
    Student('V00123458', 30), Student('V00123459', 78)]
    
    >>> get_average_grade(data)
    74.0
    '''
    #sets variables
    total_grade = 0
    avg_grade   = 0
    num_grades  = 0
    
    #gets each student instance
    for student in student_instaces:
        total_grade += student.get_grade() #adds student's grade to total_grade
        num_grades  += 1 #add 1 to the number of grades
    
    #get avg grade
    avg_grade = total_grade / num_grades
    
    return avg_grade