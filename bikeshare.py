import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = input("Please name the city you want to analyze. Is it Chicago, New York City, or Washington? ").lower()


    while city not in ['chicago', 'new york city', 'washington']:
        print("\n It appears that you named an invalid city")
        city = input("Please name the city you want to analyze. Is it Chicago, New York City, or Washington? ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please name the month you want to analyze (january, february, ... , june) or type 'all' if you don't want to filter by month? ").lower()

    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print("\n It appears that you named an invalid month")
        month = input("Please name the month you want to analyze (january, february, ... , june) or type 'all' if you don't want to filter by month? ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Please name the day of the week you want to analyze (monday, tuesday, ... sunday) or type 'all' if you don't want to filter by day of the week? ").lower()

    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print("\n It appears that you named an invalid day of the week")
        day = input("Please name the day of thr week you want to analyze (monday, tuesday, ... sunday) or type 'all' if you don't want to filter by day of the week? ").lower()

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('{} is the most popular day of the week'.format(popular_day))


    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    popular_combination = df['Start and End Station'].mode()[0]
    print('Most frequent combination of start station and end station trip:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average travel time: ', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print(user_types)

    except KeyError:
        print('No user type information')



    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(gender)

    except KeyError:
        print('No gender information')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = df['Birth Year'].min().astype('int64')
        recent_year_of_birth = df['Birth Year'].max().astype('int64')
        common_year_of_birth = df['Birth Year'].mode()[0].astype('int64')

        print('Earliest year of birth: ', earliest_year_of_birth)
        print('Recent year of birth: ', recent_year_of_birth)
        print('Most common year of birth: ', common_year_of_birth)

    except KeyError:
        print('No birth date information')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data = input('\nWould you like to see the specific rides? Enter yes or no.\n')
        start_row = 0
        end_row = start_row + 5
        total_rows = df.shape[0] + 1
        while raw_data == 'yes':
            if start_row >= total_rows:
                break
            else:
                print(df[start_row:end_row])
                start_row +=5
                end_row +=5
                raw_data = input('\nWould you like to see the specific rides? Enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
