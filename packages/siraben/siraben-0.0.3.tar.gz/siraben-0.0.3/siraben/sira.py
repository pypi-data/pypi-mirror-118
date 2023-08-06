class Siraben:
    def __init__(self):
        self.name = 'Sira'
        self.lastname = 'Benchapoowanon'
        self.nickname = 'Tum'

    def WhoIAm(self):
        '''
        This is function to show who I am
        '''
        print('My name is: {}'.format(self.name))
        print('My lastname is: {}'.format(self.lastname))
        print('My nickname is: {}'.format(self.nickname))

    @property
    def email(self):
        '''
        This is function to show email
        '''
        return '{}.{}@gmail.com'.format(self.name.lower(), self.lastname.lower())

    def __str__(self):
        return 'This is Siraben class and Viewben class'

class Viewben:
    def __init__(self):
        self.name = 'Siriporn'
        self.lastname = 'Khongkharat'
        self.nickname = 'View'

if __name__ == '__main__':        
    '''
    test Siraben()
    '''
    x = Siraben()
    print(help(x.WhoIAm))

    '''
    test Viewben()
    '''
    y = Viewben()
    print(y.name)
    print(y.lastname)
    print(y.nickname)
    
