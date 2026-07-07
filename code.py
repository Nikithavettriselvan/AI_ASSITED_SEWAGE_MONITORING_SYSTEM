from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
data = pd.read_csv("/content/drive/MyDrive/sewage.csv")
data.head()

X = data[['Distance','ChangeRate','MQ4','MQ135']]
y = data['OverflowHours']

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = DecisionTreeRegressor()
model.fit(X_train, y_train)

from sklearn.tree import DecisionTreeClassifier

X_gas = data[['MQ4','MQ135']]
y_gas = data['GasCondition']

gas_model = DecisionTreeClassifier()
gas_model.fit(X_gas, y_gas)

import requests
import pandas as pd


CHANNEL_ID = "XXXXXXX"
READ_API_KEY = "XXXXXXXXXXXXXXXX"

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

response = requests.get(url)
data_json = response.json()

feeds = data_json['feeds']


latest = feeds[0]

distance = float(latest['field1'])
mq4 = float(latest['field2'])
mq135 = float(latest['field3'])


changerate = 0


new_data = pd.DataFrame([[distance, changerate, mq4, mq135]],
columns=['Distance','ChangeRate','MQ4','MQ135'])


overflow_pred = model.predict(new_data)

gas_data = pd.DataFrame([[mq4, mq135]], columns=['MQ4','MQ135'])
gas_pred = gas_model.predict(gas_data)

print("Distance:", distance)
print("ChangeRate:", changerate)
print("MQ4:", mq4)
print("MQ135:", mq135)
print("Gas Condition:", gas_pred[0])
print("Predicted Overflow Hours:", int(overflow_pred[0]))
