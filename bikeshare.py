#Yahia El-Naggar
#python ver: 3.10.8



import time
import numpy as np  #ver 1.23.5
import pandas as pd #ver 1.5.1



def get_filters():
    """
    Asks the user to specify a city, month and day to analyze.
    
    Returns: the valid filters we need to start our analysis
    """    
    print("\nWelcome to U.S bike share, let's explore some data.")
    print('\n'+'-'*40+'\n')


    print("Choose a city from (Chicago, New York and Washington) to start exploring.")
    city = str(input("Name of the city: "))

    while city.title().strip() not in cities:
        print("\nI can't understand \"{}\" make sure that the spelling is correct.".format(city))
        city = str(input("Name of the city: "))
    city=city.title().strip()

    print("\nWhich month you need to explore?\nJanuary, February, March, April, May, June or all?")
    month = str(input('Name of the month: ')).title().strip()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    
    if month not in months:
        print('\nPlease make sure you are typing the full month name or type "all" for all months.\n')
    while month not in months:
        month = str(input('Name of the month: ')).title().strip()
    
    print("\nWhich day of the week you want to explore?\nSaturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or all?")
    day=str(input("Name of the day: ")).title().strip()
    days=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'All']

    if day not in days:
        print('\nPlease make sure you are typing the correct full name of the chosen day\n')
    while day not in days:
        day=str(input("Name of the day: ")).title().strip()

    
    print('\n'+'-'*40+'\n')

    return city, month, day



def filter_data(city,month,day):
    """
    Makes a PanDas DataFrame from the csv files according to filters -basically the arguments-
    
    Arguments:
        str-city the name of the city to load its csv.
        str-month for filtering according to months "January, February ..., June"
        str-day for filtering according to specefic day of the week "Saturday, Monday ..., Friday"
        
    Returns:
        Filterd PanDas DataFrame ready to get statistics from.
    """
    
    df = pd.read_csv(cities[city])
    
    #Converting the dtype of time columns to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Extracting months and days to new columns.
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()

    #Filtering data according to specified month and day -if specified!-
    if month != 'All':
        df = df[df['month'] == month]
    
    if day != 'All':
        df = df[df['day'] == day]

    return df



def time_stats(df):
    """Disblays statistics on the most frequent times of travel for a given PanDas DataFrame"""
    print('Most Frequent Times of Travel...\n\n')
    start_time =time.time()

    start_hour=df['Start Time'].dt.hour
    #Displaying the most common month, day and start hour.
    if month == 'All':
        print('The most common month is {}.'.format(df['month'].mode()[0]))
    
    if day == 'All':
        print('The most common day of week is {}.'.format(df['day'].mode()[0]))
    
    print('The most frequent start hour is {}:00.'.format(start_hour.mode()[0]))
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'-'*40+'\n')



def station_stats(df):
    """Displays the statistics on the most populer stations for a given DataFrame."""
    print('Calculating The Most popular stations...\n\n')
    start_time =time.time()

    print('The most used start station is {}.'.format(df['Start Station'].mode()[0]))
    print('The most used end station is {}.'.format(df['End Station'].mode()[0]))
    
    start_to_end = df['Start Station'] +" to "+ df['End Station']
    print('The most frequant trip was from {}.'.format(start_to_end.mode()[0]))
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'-'*40+'\n')



def convert_seconds(seconds):
    """
    Converts the time unit from seconds to the format to other units 
    Arguments:int seconds, to be converted.
    Returns: ts 'Time String' discribes that number by more understandable string.

    Example: give it 10,000,000 seconds as intger it will return the string: ~= 3 months, 25 days, 17:46:40
    """
    
    yy=int(seconds//(60*60*24*365.25)) #converts seconds to the maximun possible natural number of years.
    seconds =seconds%(60*60*24*365.25) #assigns the reminder from the last mathimatical operation '//' to seconds.
    
    mm = int(seconds//(60*60*24*30))
    seconds =seconds%(60*60*24*30)

    dd = int(seconds//(60*60*24))
    seconds =seconds%(60*60*24)

    hh = int(seconds//(60*60))
    seconds=seconds%(60*60)

    mins = int(seconds//60)
    seconds=int(seconds%60)
    
    #Making the string readable and as short as possible.
    ts='~= '      
    if yy == 1:
        ts+='1 year, '
    elif yy != 0:
        ts+= str(yy)+ ' years, '
    if mm == 1:
        ts+='1 month, '
    elif mm != 0:
        ts+= str(mm)+ ' months, '
    if dd == 1:
        ts+='1 day, '
    elif dd != 0:
        ts+= str(dd)+ ' days, '

    ts = ts + ('{}:{}:{}').format(hh,mins,seconds)
    
    return ts



def travel_time_stats(df):
    """Displays the total traveled time and the average trip duration."""
    print('Travel Time Statistics...\n\n')
    start_time = time.time()

    trip_sum=df['Trip Duration'].sum()
    trip_mean=df['Trip Duration'].mean()
    
    print("The total travel time for all trips was {} seconds ({}).".format(trip_sum,convert_seconds(trip_sum)))
    print("The average trip duration was {} seconds ({}).".format(trip_mean,convert_seconds(trip_mean)))
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'-'*40+'\n')
 


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('User Informations....\n\n')
    start_time = time.time()
    
    print(df.value_counts('User Type'),'\n')
    
    if city != 'Washington':
        print(df.value_counts('Gender'))
    
        earliest = int(df['Birth Year'].min())
        most_recent= int(df['Birth Year'].max())
        most_common= int(df['Birth Year'].mode()[0])
        print('\nYear of birth statistics.\nThe earliest was',earliest,
              '\nThe most recent was',most_recent,
              '\nThe most common was',most_common)
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'-'*40+'\n')



def view_more(df):
    v=str(input("Now after we finished do you wish to see the first 5 lines of raw data? [Y/n] ")).lower().strip()
    i= 0
    while (v=='y' or v=='yes' or v==''):
        print('\n')
        print(df.iloc[i:i+5])
        v=str(input('veiw another 5 lines? [Y/n] ')).lower().strip()
        i += 5

    print('\n'+'-'*40+'\n')
    print('\nWe have finished exploring bikeshare data for {} with the filters, month: "{}", day: "{}".'.format(city,month,day))
    y=str(input('\nDo you wish to try the exploration again with another filters? [Y/n] ')).lower().strip()
    return y





cities = { 'Chicago': 'chicago.csv',
           'New York': 'new_york_city.csv',
           'Washington': 'washington.csv' }

y='y'
while (__name__ =='__main__') and (y =='y' or y =='yes'  or y ==''):
    city,month,day=get_filters()

    df=filter_data(city,month,day)

    time_stats(df)
    station_stats(df)
    travel_time_stats(df)
    user_stats(df)
    y=view_more(df)
