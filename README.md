# HSI Battle of the Brains 2023 Repository
##### *Created by the University of Central Florida Team:*
##### *Alejandra Alas, Ashley Smith, Joseph Fioresi, Kenneth Colón, Meleah Chase Malcolm, Quinn Barber, Ralph Balderamos III, and Sydney Damas*

# File Documentation
#### 1. `mental_heath_corr.py`
##### This file is responsible for using `pandas` and `numpy` to clean and process CDC and ACS data together. The overall goal was to locate regions to initially launch our solution initiative. We were able to do this by conglomerating region data where all population, mental health problems, and poverty information is available/collected. We then used min-max scaling in order to normalize this data relative to all other regions. With these values we used exponential weighting to calculate our overall weighted score of locations to launch our initiative. We then min-max scaled this resulting score and display the results. Our findings for the best places to launch are the following:
###### 1. Tallahassee, Florida 32304
###### 2. Bronx, New York 10456
###### 3. Brownsville, Texas 78521
###### 4. Tampa, Florida 33620
###### 5. Brooklyn, New York 11212
<br>

#### 2. `cdc_analysis.py`
##### This file is responsible for cleaning up the CDC data from `CDC Places 2020 Health Outcomes.csv` and `CDC Places Data Dictionary.xlsx`. It maps all the abbreviated data names to their corresponding names in the dictionary. Then we form a new data frame to represent locations based off of their City/State, Population, and Mental Health statistics. We sort this data by the most mental health issues for >= 14 days per 1000 adults >= 18 years old. This data is printed and stored in the `clean_data` folder.
<br>

#### 3. `initial_analysis.py`
##### Thie file is responsible for cleaning all the ACS data that we were given. This is done by attributing the abbreviated data names to their dictionary values in `ACS Data Dictionary.xlsx`. All this cleaned data is then stored in the `clean_data` folder to be used by other programs.
<br>

#### 4. `clean_data` & `data` folders
##### The `data` folder encompasses all of the data that was provided by HSI. The only change made to the data was a conversion of the `Zip Code Index.csv` file to `Zip Code Index.xlsx`.
##### The `clean_data` folder encompasses processed, cleaned, and resulting data from the above files.

# Running Yourself
#### 1. Make sure to have Python 3.9.X or 3.10.X installed on your system along with `npm` and `pip`
#### 2. Run `pip install pandas openpyxl` in your command line (command prompt on Windows and terminal on MAC)
#### 3. `cd` into your directory where you would like to clone our repository.
#### 4. Use `git clone https://github.com/joefioresi718/hsi_bob.git` to clone our repository
#### 5. Run the python files using compiler of your choice, see printed results and saved results