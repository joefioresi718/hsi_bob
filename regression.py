import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error


# Load dataframe.
df = pd.read_csv('clean_data/master.csv')

# NaN stats.
# for col in df.columns:
#     nan_sum = df[col].isna().sum()
#     if nan_sum > 0:
#         print(f'{col}: {nan_sum}')

df.fillna(0, inplace=True)

# Separate the data into features and target variable.
x = df.drop(['zcta', 'mhlth_pov_index', 'mhlth_crudeprev', 'teethlost_crudeprev'], axis=1)  # Features
y = df['mhlth_pov_index']*1000  # Target variable

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize the model
model = Lasso(alpha=1.0)  # You can adjust the alpha parameter as needed

# Fit the model to the training data
history = model.fit(x_train, y_train)

# Make predictions
y_pred = model.predict(x_test)

# Compute Mean Squared Error (MSE) for evaluation
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')
# rmse

print(history.coef_)

# Assuming 'df' is the original dataframe and 'X' contains features used for the model
for feature_name, weight in zip(x.columns, model.coef_):
    if weight != 0:
        print(f"{feature_name}: {weight}")
