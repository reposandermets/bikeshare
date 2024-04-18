import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = None
    while city == None:
        user_input = input(
            """Please type the name of the city:
            Chicago
            New York City
            Washington\n""")
        try:
            city = CITY_DATA[user_input.lower()]
        except KeyError:
            print("Not a valid choice! Please try again ...")

    # get user input for month (all, january, february, ... , june)
    month = None
    month_options = {'January': 1,
                     'February': 2,
                     'March': 3,
                     'April': 4,
                     'May': 5,
                     'June': 6,
                     'All': 0, }
    while month == None:
        user_input = input(
            """Please enter number to filter by month:
            January
            February
            March
            April
            May
            June

            All - Include all months\n""")
        try:
            month = month_options[user_input.title()]
        except KeyError:
            print("Not a valid choice! Please try again ...")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    day_options = {'All': 'All',
                   'Monday': 'Monday',
                   'Tuesday': 'Tuesday',
                   'Wednesday': 'Wednesday',
                   'Thursday': 'Thursday',
                   'Friday': 'Friday',
                   'Saturday': 'Saturday',
                   'Sunday': 'Sunday'}

    while day == None:
        user_input = input(
            """Please type a day to filter by:
            Monday
            Tuesday
            Wednesday
            Thursday
            Friday
            Saturday
            Sunday

            All - Include all months\n""")
        try:
            day = day_options[user_input.title()]
        except KeyError:
            print("Not a valid choice! Please try again ...")

    print('-'*40)

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

    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()

    if month != 0:
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = {1: 'January',
              2: 'February',
              3: 'March',
              4: 'April',
              5: 'May',
              6: 'June'}

    if month == 0:
        # display the most common month if not already filtered by month
        popular_month = df['month'].mode()[0]
        print('Most common month:', months[popular_month])

    if day == 'All':
        # display the most common day of week if not already filtered by day
        popular_day = df['day'].mode()[0]
        print('Most common day:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('\nMost most commonly used start station:',
          df['Start Station'].mode()[0])

    print('\nMost most commonly used end station:',
          df['End Station'].mode()[0])

    print('\nMost frequent combination of start station and end station trip:\n\n',
          df[['Start Station', 'End Station']].mode().iloc[0], '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    start_time = time.time()
    df['travel_time'] = (df['End Time'] - df['Start Time'])

    print('\nTotal travel time in hours:',
          round((df['travel_time'] / pd.Timedelta(hours=1)).sum()))

    print('\nAverage travel time in minutes:',
          round((df['travel_time'] / pd.Timedelta(minutes=1)).mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of user types:\n',
          df['User Type'].value_counts())

    df = df.dropna(axis=0)

    if 'Gender' in df:
        print('\nCounts of gender:\n',
              df['Gender'].value_counts())
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')

    if 'Birth Year' in df:
        df_by_sorted = df.sort_values('Birth Year')['Birth Year']
        print('\nThe earliest Birth Year:',
              int(df_by_sorted.iloc[0]))

        print('The most recent Birth Year:',
              int(df_by_sorted.iloc[-1]))

        print('The most common Birth Year:',
              int(df_by_sorted.mode().iloc[0]))

        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')

    print('-'*40)


def display_raw_data(df):
    view_display = input(
        "Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while view_display == 'yes' or view_display == 'y':
        print(df.iloc[start_loc: (start_loc + 5)])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter (y)es or (n)o.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()