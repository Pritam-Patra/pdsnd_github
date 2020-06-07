import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
    (str) city - name of the city to analyz
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('\n'+'='*10+'CITY FILTER'+'='*29)
        city = input('Please enter one of the following cities:\n1. Chicago,\n2. New York City,\n3. Washington \n=> ').title()
        if city == 'Chicago' or city == 'New York City' or city == 'Washington' :
            break
        else:
            print('\nInvalid Input\nPlease input among Chicago, New York City or Washington only!!\n\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        print('\n'+'='*10+'MONTH FILTER'+'='*28)
        month = input('Please enter a month between January to June: \n[Select \'all\' to apply filter for all the months]\n=> ').title()
        if (month == 'January' or month == 'February' or month == 'March' or month == 'April' or month == 'May' or month == 'June' or month == 'All'):
            break
        else:
            print("\nIt's not a valid month!!\nPlease write the full name of the month!!\n\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('\n'+'='*10+'DAY FILTER'+'='*30)
        day = input('Please enter day of the week \n[Select \'all\' to apply filter for all the days]\n=> ').title()
        if  (day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday' or day == 'Saturday' or day == 'Sunday' or day == 'All'):
            break
        else:
            print("\nIt's not a valid Day!!\n\nPlease write the full name of the day!!\n\n")

    print('\n'+'=========='*5 + '=')
    print(' '*17 + 'CALCULATING...')
    print('=========='*5 + '=\n')
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
    
    df['month'] = df['Start Time'].dt.strftime('%B')
    if month.title() != 'All':
        df = df[df['month'] == month]

    df['day'] = df['Start Time'].dt.strftime('%A')
    if day.title() != 'All':
        df = df[df['day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is : {}'.format(df['month'].mode()[0]))

    # display the most common day of week:
    print('The most common day of the week is : {}'.format(df['day'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour is : {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'x========='*5 + 'x\n')

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station \t: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station \t: {}'.format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip
    combined = df[['Start Station', 'End Station']].mode()
    print('The most frequent combination of start station and end station \t:')
    print('Start Station : {} ,\t End Station : {}'.format(
            combined['Start Station'][0],
            combined['End Station'][0])
         )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'x========='*5 + 'x\n')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    dd = int(total_duration//86400)
    hh = int((total_duration % 86400)//3600)
    mm = int(((total_duration % 86400) % 3600)//60)
    ss = int(((total_duration % 86400) % 3600) // 60)
    print('Total travel time \t: {} days  {} hrs  {} mins  {} sec'.format(dd, hh, mm, ss))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    mins = int(((mean_duration % 86400) % 3600)//60)
    sec = int(((mean_duration % 86400) % 3600) // 60)
    print('Mean travel time \t: {}mins {}sec'.format(mins, sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'x========='*5 + 'x\n')

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    
    if 'Gender' in df.columns:
        # Display counts of gender
        print(df['Gender'].value_counts())
    else:
        print("Sorry!! No Gender related information is available for this city!")
    
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print("Most earliest year of birth\t: {}".format(df['Birth Year'].min()))
        print("Most most recent year of birth: {}".format(df['Birth Year'].max()))
        print("Most most common year of birth: {}".format(df['Birth Year'].mode()[0]))
    else:
        print("Sorry!! No Birth Year information is available for this city!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'x========='*5 + 'x\n')


def raw_data(df):
    """Displays first 5 lines of Raw Data."""
    
    see_data = input("\nDo you want to see first 5 lines of raw data? Type 'yes' to view first 5 lines : ").lower()
    if see_data == 'yes':
        print('\n'+'=========='*11 + '=')
        print(' '*50 + 'RAW DATA...')
        print('=========='*11 + '=\n')
        start = 0
        end = 5
        print(df[start : end])
        start = end
        end += 5
        while True:   
            see_data2 = input("\nDo you want to see the next 5 lines? Type 'yes' or 'no' : ").lower()
            if see_data2 == 'yes':
                print(df[start : end])
                start = end
                end += 5
            elif see_data2 == 'no':
                see_data2 = 'no'
                break
            else:
                print("\nWRONG INPUT!\nPlease type either 'yes' or 'no' only!")
                
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data(df)

        restart = input("\nWould you like to restart? Type 'yes' or 'y' to restart.\n")
        if restart.lower() != 'yes' or restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()