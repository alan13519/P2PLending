import random
import string
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def generate_hex_color():
    '''
    Desc: Generate a random hexidecimal color 
    Param: N/A
    Return: A 6 digit randomized hexidecimal in format '#------'
    Return Type: String
    '''
    
    hex_color = '#'
    for _ in np.arange(0,6):
        hex_color += random.choice(string.hexdigits)
    return hex_color

def ecdf(data):
    """
    Desc: Compute ECDF for a one-dimensional array of measurements.
    Param: data : Series of numerical data
    Return: x and y coordinates for cumulative distribution function
    Return Type: Tuple
    """
    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n

    return x, y

def plot_ecdf(datas, name=' ', width=15, height=10):
    '''
    Desc: Calculate and plot the ecdf of a given dataset
    Params: datas  : Tuple of Split DataFrame along with the selected label for the dataset
            name   : String name of the dependant variable
            width  : Int width of the figure
            height : Int height of the figure
            
    Return: None
    Return Type: N/A
    '''
    plt.figure(figsize=(width,height))
    
    for _, data in enumerate(datas):   
        # Generate a random six digit hex character
        color = generate_hex_color()

        x, y = ecdf(data[0])
        plt.plot(x, y, marker='.', linestyle='none', color=color, label=data[1][0])
        lgd = plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.0), shadow=True, prop={'size': 16})
        
        # Increase the sizes of the markers inside the legend
        for handle in lgd.legendHandles:
            handle._legmarker.set_markersize(25)

    # Label the axes
    _ = plt.xlabel(name)
    _ = plt.ylabel('ECDF')
    _ = plt.title('ECDF of {}'.format(name))

    # Display the plot
    plt.show()

def fill_nas(df, to_fill_na):
    """
    Desc: Fills in the NaN values of each column listed in to_fill_na 
    Param: df : Dataframe that we are performing the operations on
           to_fill_na: List of Tuples of column name and value we want NaNs to be replaced with (col_name, value)
    Return: N/A
    Return Type: N/A
    """
    # Fill in all NaN values with respective values
    for col_name, value in to_fill_na:
        # replace value if MAX keyword is used with max of the column
        if value == 'MAX':
            value = df[col_name].max()
        df[col_name].fillna(value, inplace=True)


def percentage_na(col):
    """
    Desc: Shows percentage NaNs in a column
    Param: col: Series a column of a dataframe
    Return: Percentage of NaNs 0-100%
    Return Type: Float
    """
    num_null = col.isna().sum()
    num_tot = len(col)
    return (num_null/num_tot)*100

def show_drop_cols(df, show = 0, drop=50):
    """
    Desc: Show and Drop columns in a dataframe based on two thresholds
    Param: df : Dataframe that we are performing the operations on
           show: Integer threshold that we want to show
           drop: Integer threshold that we want to drop
    Return: N/A
    Return Type: N/A
    """
    for col in df.columns:
        perc = percentage_na(df[col])
        if perc > show:
            print("Column: {} has {}% values NaN".format(col, percentage_na(df[col])))
            if perc > drop:
                # If percentage of values is greater than the threshold, drop the column
                df.drop(col, axis=1, inplace=True)
                