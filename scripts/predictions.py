
import json
import numpy as np
from matplotlib import pyplot as plt

# Path of the dataset in JSON
DATA_FPATH = "../dati-json/dpc-covid19-ita-andamento-nazionale.json"

def load_data():
    with open(DATA_FPATH, encoding="utf-8-sig") as f:
        return json.load(f)

# Given a date in ISO standard return it in format MM-DD
def date_format(date_original):
    return date_original[5:10]


# Returns the index of the dataset corresponding to the given date.
# Date must be in MM-DD format
def get_index_date(date, dataset):
    for i, v in enumerate(dataset):
        if date == date_format(v["data"]):
            return i
    raise Exception(f"Date {date} not found")


# Returns a list having as values the key in the dataset for each element
def extract_dataset_key(key, dataset):
    return [x[key] for x in dataset]


# Given any list of values, returns a new list having increases as values
# e.g.: if data = [3,8,16], it returns [3,5,8]
def get_increases(data):
    res = [0] * len(data)
    prev = 0
    for i, v in enumerate(data):
        res[i] = v - prev
        prev = v
    return res


# Applies a constant second derivative dd to tot_cases, returns a list with its going
def predict_tot_cases(tot_cases, d, dd):
    res = list(tot_cases)
    current_increase = d
    while current_increase > 0:
        res.append(res[-1] + current_increase)
        current_increase += dd
    return res


def main():
    # Load dataset
    dataset = load_data()
    PEAK_DATE = "03-22"  #so it seems from data
    i_start = get_index_date(PEAK_DATE, dataset)
    dates_mm_dd = [date_format(x["data"]) for x in dataset]

    # Extract data
    total_cases = extract_dataset_key("totale_casi", dataset)
    recovered = extract_dataset_key("dimessi_guariti", dataset)
    deaths = extract_dataset_key("deceduti", dataset)

    # Compute increases
    d_total_cases = get_increases(total_cases)
    dd_total_cases = get_increases(d_total_cases)
    D_WINDOW = 3
    mean_d_total_cases = np.mean(d_total_cases[i_start:i_start+D_WINDOW])  #mean of increase of D_WINDOW days window from peak date
    mean_dd_total_cases = np.mean(dd_total_cases[i_start:])  #mean dd from peak date
    stddev_dd_total_cases = np.std(dd_total_cases[i_start:]) #std of dd from peak date
    print(f"Mean derivative of {D_WINDOW} days from peak date:", mean_d_total_cases)
    print("Mean second derivative from peak date until now:", mean_dd_total_cases)
    print("Std. dev. second derivative from peak date until now:", stddev_dd_total_cases)

    pred = predict_tot_cases(
        total_cases,
        mean_d_total_cases,
        mean_dd_total_cases
    )

    fig, ax = plt.subplots()
    ax.plot(pred, 'r--')
    ax.plot(dates_mm_dd, pred[:len(dataset)])
    plt.show()

    #plt.plot(dates_mm_dd, dd_total_cases)
    #plt.show()



if __name__ == "__main__":
    main()



