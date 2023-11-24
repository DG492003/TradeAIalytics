
# TradeAIalytics

This web application, developed using Dash (a Python framework) and machine learning models, allows users to input a stock code. Based on this code, the application fetches and displays stock plots. The machine learning component predicts stock prices for a specific date provided by the user.  
+ index_app.py contains web layout and server function. We will be referring to it as our main file.
+ model.py is where we will implement a machine learning model for forecasting the stock price.
+ style.css is the css file for styling the web app.
+ requirements.txt is correct versions of the required Python packages to run the Python code.


## Screenshots
+ Interface of a Website
![App Screenshot](https://github.com/DG492003/TradeAIalytics/assets/113435632/30d2196e-38b5-4626-94c8-044ecabe249f)  
  
+ Inputting a stock code  
![App Screenshot](https://github.com/DG492003/TradeAIalytics/assets/113435632/45673979-cd9b-480d-95e6-87d91602d65f)  
  
+ Inputting a start-date and end-date
![App Screenshot](https://github.com/DG492003/TradeAIalytics/assets/113435632/308b13e4-c4e5-4820-bd97-7b5dad5e017b)  

+ Getting Moving Average by clicking Indicator button
![App Screenshot](https://github.com/DG492003/TradeAIalytics/assets/113435632/0acb453c-c5b5-450b-9576-534b915f01b6)

+ Applying model.py         
![SS5](https://github.com/DG492003/TradeAIalytics/assets/113435632/773f9beb-7e8f-4a99-a680-8559f0a2e1e5)





## 🛠 Skills
Python, Dash, HTML, CSS, Scikit-learn, pandas.....


## API Reference

#### Get all items
##### Here we use Financialmodelprep api to fetch the all data
#### 
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |


