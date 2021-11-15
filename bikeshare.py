#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function


# In[2]:


import time
import pandas as pd
import numpy as np
if hasattr(__builtins__, 'raw_input'):
    input=raw_input


# In[3]:


import warnings
warnings.simplefilter("ignore")


# In[4]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Monthes = ['All', 'January','February','March','April','May','June']
Days    = ['All', 'Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
city, month, day = "chicago", "January", "Saturday"


# In[5]:


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
    while(True):
        print("Which city do you want to filter:")
        for index, key in enumerate(CITY_DATA,1):
            print("({}) {}".format(index, key), end = "\t")
        try:
            user_choice = int(input("\nuser choice: "))
            if user_choice in range(1,len(CITY_DATA)+1):
                city = list(CITY_DATA.keys())[user_choice-1]
                break
        except ValueError:
            print("Wrong Answer")
    # get user input for month (all, january, february, ... , june)
    print("Which month do you want to filter:")
    while(True):
        for index, m in enumerate(Monthes):
            print("({}) {}".format(index, m), end = "\t")
        try:
            user_choice = int(input("\nuser choice: "))
            if user_choice in range(0,len(Monthes)):
                month = Monthes[user_choice]
                break
        except ValueError:
            print("Wrong Answer")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Which day do you want to filter:")
    while(True):
        for index, m in enumerate(Days):
            print("({}) {}".format(index, m), end = "\t")
        try:
            user_choice = int(input("\nuser choice: "))
            if user_choice in range(0,len(Days)):
                day = Days[user_choice]
                break
        except ValueError:
            print("Wrong Answer")
    
    print('-'*40)    
    print("Your choices are: ")
    print("- City :", city )
    print("- Month:", month )
    print("- Day  :", day )
    print('-'*40)
    return city, month, day


# In[6]:


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
    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])
    df[(df["Start Time"].dt.month_name() == month) & (df["Start Time"].dt.day_name() == day)]
    #df['Trip Duration'] = pd.to_datetime(df['Trip Duration'], dayfirst=True, unit = 's')
    if month == 'All' and day == "All":
        return df
    elif month == 'All':
        return df[(df["Start Time"].dt.day_name() == day)]
    elif day == "All":
        return df[(df["Start Time"].dt.month_name() == month)]
    else:
        return df[(df["Start Time"].dt.month_name() == month) & (df["Start Time"].dt.day_name() == day)]


# In[7]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month: ", df["Start Time"].dt.month_name().value_counts(sort=True, ascending=False).index[0])
    #print("The most common month: ", df["Start Time"].dt.month_name().value_counts(sort=True, ascending=False).idxmax())

    # display the most common day of week
    print("The most common day  : ", df["Start Time"].dt.day_name().value_counts(sort=True, ascending=False).index[0])
    #print("The most common day  : ", df["Start Time"].dt.day_name().value_counts(sort=True, ascending=False).idxmax())

    # display the most common start hour
    print("The most common hour : ", df["Start Time"].dt.hour.value_counts(sort=True, ascending=False).index[0])
    #print("The most common hour : ", df["Start Time"].dt.hour.value_counts(sort=True, ascending=False).idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station: {} with count: {}".format(df["Start Station"].value_counts().index[0], df["Start Station"].value_counts()[0]))

    # display most commonly used end station
    print("The most commonly used end station  : {} with count: {}".format(df["End Station"].value_counts().index[0], df["End Station"].value_counts()[0]))

    # display most frequent combination of start station and end station trip
    print("\nThe most frequent combination of start station and end station trip is:")
    print(("Start Station: " + df["Start Station"] + " \nEnd Station  : " + df["End Station"]).value_counts().index[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time: ", (df["End Time"] - df["Start Time"]).sum())


    # display mean travel time
    print("Mean Travel Time: ", (df["End Time"] - df["Start Time"]).mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[10]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_count = df["User Type"].value_counts()
        print("The count of User Types is: ", end="")
        for index, count in enumerate(user_count):
            print("{}: {}".format(user_count.index[index], count), end=";\t")
        #print("The count of user types is")
        #print(df["User Type"].value_counts().to_frame())
    
    # Display counts of gender
    if 'Gender' in df.columns:     
        gender_count = df["Gender"].value_counts()
        print("\nThe count of Gender is: ", end="")
        for index, count in enumerate(gender_count):
            print("{}: {}".format(gender_count.index[index], count), end=";\t")
        
        #print("\nThe count of Gender is")
        #print(df["Gender"].value_counts().to_frame())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\n")
        print("The earliest year of birth   : ", int(df["Birth Year"].min()))
        print("The most recent year of birth: ", int(df["Birth Year"].max()))
        print("The most common year of birth: ", int(df["Birth Year"].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[11]:


def print_dataframe(df):
    """Display the dataset information"""
    print("The rows in dataframe are:")
    for i, record in enumerate(df.to_dict(orient='records')):
        print(str(record).replace(",","\n"))
        if i % 5 == 0:
            print("_"*100)
            print("Do you want to print 5 more rows?")
            raw_input = str(input("Press y to continue..."))
            if raw_input.lower() != "y":
                break;


# In[12]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_dataframe(df)
        restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
        if restart.lower() != 'yes':
            break


# In[13]:


if __name__ == "__main__":
    main()

