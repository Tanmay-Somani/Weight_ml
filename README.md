# Weight Dashboard

**Author**: Tanmay Somani  
**Date**: October 6, 2024  
**Description**: The Weight Dashboard is a Python-based application that allows users to track their weight over time while setting and monitoring goals. 

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Future Plans](#Futureplans)

## Features

- **Weight Logging**: Users can input and store their weight data over time.
- **Goal Setting**: Set and monitor weight loss/gain goals with specific deadlines.
- **Data Visualization**: Interactive graphs display weight changes over time, including goal indicators.
- **Data Persistence**: Weight and goal data are saved to a local text file, allowing users to track their progress.
- **User-Friendly Interface**: Intuitive design for easy navigation and usability.
- **Error Handling**: Robust error handling for invalid inputs and file operations.
- **Tooltips**: Helpful tooltips provide context for menu options and functionalities.

## Installation

To run the application, you need to have Python installed on your system. You can download Python from the official website: [python.org](https://www.python.org/downloads/).

### Step-by-Step Installation

1. **Clone the Repository**:
   Open your terminal or command prompt and run the following command to clone the repository:

   ```bash
   git clone https://github.com/yourusername/weight-dashboard.git
   cd weight-dashboard
   ```
2. **Install the neccessary Libraries**:
   Install the required libraries using pip. Run the following command:
   ```bash
   pip install matplotlib
   ```
3. **Run the following application**:
   Execute the following command to run the application:
   ```bash
   python weight_dashboard.py
   ```

## Usage

1. **Launch the Application**: Open the Weight Dashboard by executing the Python script.
2. **Add Weight Data**: Input your current weight in the provided field and click the "Add Data" button.
3. **Set a Weight Goal**: Use the "Goal" menu to set a weight goal by specifying your target weight and the number of weeks to achieve it.
4. **Visualize Progress**: The dashboard will display a graph of your weight over time, along with indicators for your set goals.
5. **View Current Goal**: Access the "Goal" menu to view your current weight goal or to remove it.
6. **Access Help**: Use the "Help" menu for information about the application.

## Future Plans
- **Integrate Machine Learning**: Implement machine learning algorithms to provide personalized weight loss suggestions and predictions based on user data. This may include regression models to forecast weight changes or classification models to identify factors affecting goal management

