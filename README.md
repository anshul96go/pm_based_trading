# Prediction Market Based Trading

## Aim

Employ PM concepts to create trading strategies (using estimize data)

The goal is to get the list of stocks with the past mean returns, std dev of returns, optimal entry-exit pints, sharpe ratio, max and min return for each stock in estimize (fr which estimize and market date is available, as well as the earning dates)


## File structure (with the order of running the files)

- 0. [discontinued] get_data_each_stock.py : helper function to get the estimize table for each stock

0. helper_get_final_sheet.py : helper functions to create the final_sheet

0. helper_2.py : helper functions to create the final_sheet

1. [discontinued] get_stock_est_files.py : code to get the list of stocks and save the list in stock_list.csv file + save the estimize table for each stock in output folder

1. get_data_each_stock_new.py : code to get the list of stocks and save the list in stock_list.csv file + save the estimize table for each stock in output folder + include the upcoming earning dates, timings (AMC/ BMO) & day 

2. check_pattern.py : used to create stock_hit_rate.csv file which provides some stats based on the estimize data only

3. save_earning_dates.py : 
    1. complete code to get the past earning dates files for each stock. Files are saved in the earning_dates_data folder

    2. the code needs to be run multiple times as it breaks after sometime

    3. Frequency: The code should be run after each quarter to account for the earning dates updates

3. save_hist_data.py : 
    1. complete code to extract historical price data for each stock and store it in hist_data folder

    2. Freuency: run the code as frequent as possible, atleast after each earning quarter

4. final_get_final_sheet.py : code to get the final excel sheet containing the statistics for each stock



