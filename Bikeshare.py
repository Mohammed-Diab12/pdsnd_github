import time
import pandas as pd
import numpy as np

# Dictionary containing file paths for the data of each city
CITY_DATA = {
    'chicago': '/mnt/data/chicago.csv',
    'new york city': '/mnt/data/new_york_city.csv',
    'washington': '/mnt/data/washington.csv'
}

def get_user_input(prompt, valid_inputs):
    """
    Prompts the user for input and validates it against a list of valid inputs.

    Args:
        prompt (str): The prompt message for the user input.
        valid_inputs (list): List of valid input strings.

    Returns:
        str: The validated user input.
    """
    while True:
        response = input(prompt).strip().lower()
        if response in valid_inputs:
            return response
        print("Invalid input. Please try again.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_user_input('Would you like to see data for Chicago, New York City, or Washington? ', CITY_DATA.keys())
    month = get_user_input('Which month? January, February, March, April, May, June, or "all"? ', 
                           ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    day = get_user_input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all"? ', 
                         ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])
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
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_statistics(df, column, stat_name):
    """
    Displays the most common value of a specified column.

    Args:
        df (DataFrame): The DataFrame containing the data.
        column (str): The column name for which to find the most common value.
        stat_name (str): The name of the statistic to display.
    """
    most_common = df[column].mode()[0]
    print(f'Most Common {stat_name}: {most_common}')

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame): The DataFrame containing the data.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    display_statistics(df, 'month', 'Month')
    display_statistics(df, 'day_of_week', 'Day of Week')
    display_statistics(df, 'hour', 'Start Hour')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df (DataFrame): The DataFrame containing the data.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    display_statistics(df, 'Start Station', 'Start Station')
    display_statistics(df, 'End Station', 'End Station')
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    display_statistics(df, 'Start-End Combination', 'Trip')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (DataFrame): The DataFrame containing the data.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_duration} seconds')

    mean_duration = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_duration} seconds')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df (DataFrame): The DataFrame containing the data.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(f'User Types:\n{df["User Type"].value_counts()}')

    if 'Gender' in df.columns:
        print(f'\nGender Distribution:\n{df["Gender"].value_counts()}')
    if 'Birth Year' in df.columns:
        print(f'\nEarliest Year of Birth: {int(df["Birth Year"].min())}')
        print(f'Most Recent Year of Birth: {int(df["Birth Year"].max())}')
        print(f'Most Common Year of Birth: {int(df["Birth Year"].mode()[0])}')

    print(f"\nThis took {time.time() - start_time} seconds.")
    print('-' * 40)

def display_raw_data(df, batch_size=5):
    """
    Displays raw data upon request by the user.

    Args:
        df (DataFrame): The DataFrame containing the data.
    """
    row_index = 0
    while get_user_input('Would you like to see 5 lines of raw data? Enter yes or no: ', ['yes', 'no']) == 'yes':
        print(df.iloc[row_index:row_index + batch_size])
        row_index += batch_size


def main():
    """
    The main function to run the bikeshare data analysis script.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = get_user_input('\nWould you like to restart? Enter yes or no: ', ['yes', 'no'])
        if restart == 'no':
            break

if __name__ == "__main__":
    main()
