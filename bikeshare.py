# US Bikeshare Data Analysis
# This script allows users to explore and analyze bikeshare data for three cities: Chicago, New York City, and Washington.

import time
import pandas as pd
import numpy as np

SEPARATOR = '-' * 40

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input("Please enter the city name (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        elif city == 'new york' or city == 'nyc':
            city = 'new york city'
            break
        else:
            print("Invalid city name. Please try again.")

    # Ask if the user wants to filter by month, day, both, or not at all
    while True:
        time_filter = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter: ").lower()
        if time_filter in ['month', 'day', 'both', 'none']:
            break
        else:
            print("Invalid input. Please try again.")

    # Get user input for month
    if time_filter in ['month', 'both']:
        month = input("Please enter the month (January, February, ... , June): ").lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input("Invalid month name. Please enter a valid month: ").lower()
    else:
        month = 'all'

    # Get user input for day of the week
    if time_filter in ['day', 'both']:
        day = input("Please enter the day of the week (Monday, Tuesday, ... Sunday): ").lower()
        while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input("Invalid day name. Please enter a valid day of the week: ").lower()
    else:
        day = 'all'

    print(SEPARATOR)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Day of Week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day of Week'] == day]

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['Month'].mode()[0]
    print(f"The most common month is: {common_month}")

    common_day = df['Day of Week'].mode()[0]
    print(f"The most common day of the week is: {common_day}")

    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f"The most common start hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start station and end station trip is:\n{frequent_combination}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time is: {total_travel_time} seconds")

    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types_counts = df['User Type'].value_counts()
    print("Counts of user types:\n", user_types_counts)

    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:\n", gender_counts)
    else:
        print("\nGender data is not available for this city.")

    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest birth year:", earliest_birth_year)
        print("Most recent birth year:", most_recent_birth_year)
        print("Most common birth year:", most_common_birth_year)
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(SEPARATOR)


def display_data(df):
    i = 0
    while True:
        display_data = input('\nDo you want to see 5 rows of data? Enter yes or no.\n').lower()
        if display_data == 'yes':
            print(df.iloc[i:i+5])
            i += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
