class Cat:
    '''
    cat class
    
    class for a cat 'object'
    
    === attributes
    * _str_ *name* - name of the cat
    * _int_ *age* - age of the cat
    * _str_ *breed* - breed of the cat
    '''

    def __init__(self, name: str, age: int, breed: str | None = None) -> None:
        '''
        ==== parameters
        * _str_ *name* - name of the cat
        * _int_ *age* - age of the cat
        * _str_ *breed* (optional) - breed of the cat
        '''

        self.name: str = name
        self.age: int = age
        self.breed: str = breed or 'mystery'

    def rename(self, name: str) -> None:
        '''
        renames the cat

        ==== parameters
        * _str_ *name*  - new name of the cat
        '''

        self.name = name

    def age_human_years(self) -> int:
        '''
        age of cat in human years

        calculates and returns age of cat in human years

        ==== returns
        _int_ - age in human years
        '''

        if self.age >= 6:
            return (self.age - 6 + 4) * 40
        else:
            return (self.age * 19) // 3 + 1

    def introduce(self) -> None:
        '''
        introduces the cat

        prints an introduction of the cat
        '''

        print(f"{self.age} year old {self.breed} cat named {self.name}")

    def call(cls) -> None:
        '''
        meows

        prints meow!
        '''

        print("meow!")