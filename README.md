# BMI Calculator

## Overview
The BMI Calculator application helps users calculate their Body Mass Index (BMI) based on their weight and height measurements. By providing users with an easy-to-use graphical interface, this application allows them to monitor their health by calculating BMI, viewing their history, and analyzing trends over time. The application securely stores user data in an SQLite database, ensuring that their information is organized and easily accessible.

## Features
- **Calculate BMI**: Users can input their weight in kilograms and height in feet and inches to calculate their BMI.
- **Data Storage**: The application saves user data, including their BMI calculations, to an SQLite database for future reference.
- **BMI History**: Users can view their BMI history, allowing them to track changes over time and observe trends.
- **Delete BMI History**: Users have the option to delete their BMI history from the database, ensuring they can manage their records as needed.
- **Data Visualization**: Utilize Matplotlib to visualize BMI trends, making it easy for users to see their progress.
- **BMI Classification**: The application classifies the calculated BMI into categories such as Underweight, Normal weight, Overweight, and Obese, helping users understand their health status.

## Technologies Used
- **Python**: The primary programming language used for developing the application.
- **Tkinter**: A built-in library used to create the graphical user interface (GUI).
- **SQLite**: A lightweight database engine used for storing user data and BMI calculations.
- **Matplotlib**: A library used for creating static, animated, and interactive visualizations in Python, which is used to visualize BMI trends.
- **Pandas**: A powerful data manipulation library used for handling and analyzing user data efficiently.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd bmi-calculator
