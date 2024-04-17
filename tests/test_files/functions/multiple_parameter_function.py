def hello(name: str, shout: bool = False) -> None:
    greeting: str = f"hello, {name}"
    if shout:
        print(greeting.upper()+'!')
    else:
        print(greeting)