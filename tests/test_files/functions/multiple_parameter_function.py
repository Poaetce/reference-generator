def hello(name: str, shout: bool = False) -> None:
    '''
    greets the user

    prints "hello" to a person

    === parameters
    * _str_ *name*  - name of the person to greet
    * _bool_ *shout* (optional) - whether or not the greeting is a shout
    '''

    greeting: str = f"hello, {name}"
    if shout:
        print(greeting.upper()+'!')
    else:
        print(greeting)