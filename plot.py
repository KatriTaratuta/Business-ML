import pandas as pd
import matplotlib.pyplot as plt
import time

LOG_FILE = './logs/metric_log.csv'
OUTPUT_IMAGE = './logs/error_distribution.png'

while True:
    try:
        data = pd.read_csv(LOG_FILE)
        plt.figure(figsize=(10, 6))
        plt.hist(data['absolute_error'], bins=20, color='blue', alpha=0.7)
        plt.title('Distribution of Absolute Errors')
        plt.xlabel('Absolute Error')
        plt.ylabel('Frequency')
        plt.savefig(OUTPUT_IMAGE)
        plt.close()
        print("Updated histogram.")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(10)
