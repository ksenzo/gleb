import datetime
import random
from faker import Faker


def randomizer(winning_percent):
    fake = Faker()
    start_date = datetime.date(year=1001, month=1, day=1)
    end_date = datetime.date(year=2999, month=12, day=31)
    random_date_1 = fake.date_between(start_date=start_date, end_date=end_date)
    random_date_2 = fake.date_between(start_date=start_date, end_date=end_date)
    int_random_date_1 = random_date_1.day * random_date_1.month * random_date_1.year
    int_random_date_2 = random_date_2.day * random_date_2.month * random_date_2.year
    random_time = fake.unix_time()

    random_int = int_random_date_1 * int_random_date_2 + random_time
    winning_range_start = random.randint(1, random_int)
    count_winning_combinations = int((random_int * (winning_percent / 100)).__round__(0))

    players_number = random.randint(1, random_int)

    x = winning_range_start + int(count_winning_combinations)
    if x < random_int:
        winning_combinations = range(winning_range_start, x + 1)
        if players_number in winning_combinations:
            return True
        else:
            return False
    else:
        winning_combinations_1 = range(winning_range_start, random_int + 1)
        if players_number in winning_combinations_1:
            return True
        len_of_second_part = int(count_winning_combinations) - len(winning_combinations_1)
        winning_combinations_2 = range(1, len_of_second_part + 1)
        if players_number in winning_combinations_2:
            return True
        else:
            return False
