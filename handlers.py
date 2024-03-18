import pandas as pd
import random
import numpy as np


class FileHandler:
    """
    Class that handle CSV file
    It takes in the CSV file/s path, read the file and return 30 consecutive DP from a random TimeStamp
    """
    def __init__(self, filePath: str):
        self.filePath = filePath
        self.data = []

    def __str__(self):
        return "Class which handle .CSV file."

    # Method that read CSV file
    def read_file(self) -> None:
        try:
            self.data = pd.read_csv(self.filePath)
            if self.data.empty:
                 raise ValueError('The CSV file is empty.')
        except FileNotFoundError:
            raise "The specified CSV file does not exist."
        except pd.errors.ParserError:
            raise "Invalid CSV format."
        except Exception as e:
            raise f"An unexpected error occurred: {e}"


    # Method that read file and return 30 consecutive data points (from a random TS)
    def extract_dp(self) -> pd.DataFrame:
        self.read_file()

        if len(self.data) < 30:
            raise ValueError("File contains less than 30 data points")

        start_index = random.randint(0, len(self.data) - 30)
        sample_data = self.data.iloc[start_index:start_index + 30]
        
        fileName = self.filePath.split("/")[1]
        
        return sample_data, fileName

class OutlierHandler:
    """
    Class that detects outliers
    It takes in 30 data points and return outliers
    Outlier definition (Threshold): Any datapoint that is over 2 standard deviations beyond the mean of the 30 sampled data points.
    Mean definition: 
    Standard deviation:
    """
    def __init__(self, df, fileName):
        self.df = df
        self.prices = []
        self.timestamps = []
        self.outliers = []
        self.fileName = fileName

    def __str__(self):
        return "Class which Handle outliers"

    # Method that extract DF timestamps,prices into List
    def extract_data(self) -> None:
        self.timestamps = self.df.iloc[:, 1].tolist()
        self.prices = self.df.iloc[:, 2].tolist()

    # Method that write CSV file with detected outliers
    def write_outlier_csv(self):
            outliers_df = pd.DataFrame(self.outliers, columns=['Stock-ID', 'Timestamp', 'Actual Price', 'Mean', 'Price - Mean', '% Deviation'])

            try:
                outliers_df.to_csv(f"output_files/outliers_{self.fileName}", index=False)
                print(f"Outliers written to 'outliers_{self.fileName}' file successfully.")
            except Exception as e:
                raise f"An error occurred while writing outliers to CSV file: {e}" 

    # Method that detects outliers
    def detect_outliers(self) -> list:
        self.extract_data()
        prices = [float(price) for price in self.prices]

        mean = np.mean(self.prices)
        std_dev = np.std(self.prices)
        threshold = mean + (2 * std_dev)

        # Detect outliers, calculate deviation & append data to outliers[]
        for i in range(len(prices)):
            if prices[i] > threshold:
                deviation = (prices[i] - mean) / mean * 100
                self.outliers.append([self.df.iloc[i, 0], self.timestamps[i], prices[i], mean, prices[i] - mean, deviation])

        # If there are any outliers, write new CSV file
        if self.outliers:
            self.write_outlier_csv()
            return f"Outliers written to 'outliers_{self.fileName}' file successfully." 
        else:
            return f"No outliers detected in {self.fileName}"