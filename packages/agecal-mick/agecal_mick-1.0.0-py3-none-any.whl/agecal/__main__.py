import agecal
from agecal import greeting
import datetime

def main():
    greeting.sayHi()
    
    my_birth_date = datetime.datetime(2000, 8, 18)
    present_date = datetime.datetime.now()

    duration = (present_date - my_birth_date)
    duration_in_s = duration.total_seconds()
    my_age = divmod(duration_in_s, 31536000)[0]

    
    your_age = int(input('Enter Your Age\n'))

    statement = 'You are a little baby' if my_age >= your_age else 'You are older'
    print(statement)


if __name__ == '__main__':
    main()