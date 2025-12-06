class Student:
    def __init__(self,MISIS,stdname,mark):
        self.__MISIS = MISIS
        self.__stdname = stdname
        self.__mark = mark

    def __init__(self):
        self.__MISIS ="M0101"
        self.__stdname = "Ali"
        self.__mark = 0

    
    def __str__(self):
        return f'Student info: MISIS={self.__MISIS}, Name={self.__stdname}, Mark={self.__mark}'
    def result(self):
        if self.mark > 40:
            return (f'{self.stdname} passed!!:)')
    
#std1 = Student('M0101','Ali',79)
#std2 = Student('M0102','Veli',89)
std3 = Student()
print(std3)

