from datetime import datetime 


def month():
    x = datetime.now()

    y = (x.month + 30)

    print(x)

    print(y)