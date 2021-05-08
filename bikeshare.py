import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

city_names = list(CITY_DATA.keys())
month_names = [ 'january', 'february', 'march', 'april', 'may', 'june' ]
weekday_names = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]


# created function to check existance of related column (I added after the review.)
def printSafe(dataframe, name, explanation, getter):
    if name in dataframe:
        value = getter(dataframe[ name ])
        print('{} {}'.format(explanation, value))
    else:
        print('There is no {} column in dataframe.'.format(name))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    city = input("Enter city name: ").lower()
    while city not in city_names:
        print('This city data does not exist.Please choose one of these: {}'.format(city_names))
        city = input("Enter city name: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Enter month: ").lower()
    # "all" is valid input so we don't have to control that from the list.
    while month not in month_names and month != 'all':
        print('This month data does not exist.Please choose one of these: {}'.format(month_names))
        month = input("Enter month: ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day of week: ").lower()
    # "all" is valid input so we don't have to control that from the list.
    while day not in weekday_names and day != 'all':
        print('This day data does not exist.Please choose one of these: {}'.format(weekday_names))
        day = input("Enter day of week: ").lower()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # defined all columns which will be used in next ToDos.
    df = pd.read_csv(CITY_DATA[ city ])
    df[ 'Start Time' ] = pd.to_datetime(df[ 'Start Time' ])
    df[ 'End Time' ] = pd.to_datetime(df[ 'End Time' ])
    df[ 'month' ] = df[ 'Start Time' ].dt.month
    df[ 'day' ] = df[ 'Start Time' ].dt.day_name()
    df[ 'hour' ] = df[ 'Start Time' ].dt.hour
    df[ 'station_combination' ] = df[ 'Start Station' ] + df[ 'End Station' ]
    df[ 'travel_time' ] = df[ 'End Time' ] - df[ 'Start Time' ]

    if month != 'all':
        month = month_names.index(month) + 1
        df = df[ df[ 'month' ] == month ]
    if day != 'all':
        df = df[ df[ 'day' ] == day.title() ]

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[ start_loc: start_loc + 5 ])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    printSafe(df, 'month', 'Most common month is', lambda column: column.value_counts().idxmax())

    # TO DO: display the most common day of week
    printSafe(df, 'day', 'Most common day is', lambda column: column.value_counts().idxmax())

    # TO DO: display the most common start hour
    printSafe(df, 'hour', 'Most common hour is', lambda column: column.value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    printSafe(df, 'Start Station', 'Most common Start Station is', lambda column: column.value_counts().idxmax())

    # TO DO: display most commonly used end station
    printSafe(df, 'End Station', 'Most common End Station is', lambda column: column.value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    printSafe(df, 'station_combination', 'Most common station_combination is',
              lambda column: column.value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    printSafe(df, 'travel_time', 'Total travel time is', lambda column: column.sum())

    # TO DO: display mean travel time
    printSafe(df, 'travel_time', 'Mean travel time is', lambda column: column.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    printSafe(df, 'User Type', 'Counts of User Type is', lambda column: len(column.unique()))

    # TO DO: Display counts of gender
    printSafe(df, 'Gender', 'Counts of Gender is', lambda column: len(column.unique()))

    # TO DO: Display earliest, most recent, and most common year of birth
    printSafe(df, 'Birth Year', 'Earliest birth year is', lambda column: column.min())
    printSafe(df, 'Birth Year', 'Recent birth year is', lambda column: column.max())
    printSafe(df, 'Birth Year', 'Common birth year is', lambda column: column.mode()[ 0 ])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
