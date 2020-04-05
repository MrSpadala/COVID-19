
import json
from math import ceil
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
    return np.array([x[key] for x in dataset])


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


"""
# Mean suqared error of two numpy vectors (with same length)
def MSE(x1, x2):
    return np.sum((x1-x2)**2) / x1.shape[0]


# Given two vectors finds the optimal offset in days ( x1[t] ~= x2[t-offset] ) such that the MSE is minimized
def find_opt_offset(x_toshift, x_target):
    assert(len(x_toshift) == len(x_target))
    # We can do this by exhaustive search with a fixed step
    #STEP = 1  #days   TODO: maybe use also real numbers like 0.1, the curve in every point can be translated proportionally
    
    # We try to translate the last WINDOW days of x1 to try to match data on x_target
    WINDOW = 5
    x_tomatch = x_toshift[-WINDOW:].copy()   #get last WINDOW elements

    MSEs = []  #MSEs[i] := mean squared error with i days of offset
    for i in reversed(range(len(x_toshift) - WINDOW + 1)):
        MSEs.append( MSE(x_target[i:i+WINDOW], x_tomatch) )

    plt.plot(MSEs, 'r^')
    plt.title("MSE vs shift of recovered curve")
    plt.show()


# Same as find_opt_offset but on two dimensions
def find_opt_offset_2(x1_toshift, x2_toshift, x_target):
    assert(len(x1_toshift) == len(x_target))
    assert(len(x2_toshift) == len(x_target))

    WINDOW = 5
    x1_tomatch = x1_toshift[-WINDOW:].copy()   #get last WINDOW elements
    x2_tomatch = x2_toshift[-WINDOW:].copy()   #get last WINDOW elements

    iterations = range(len(x1_toshift) - WINDOW + 1)
    MSEs = np.zeros((iterations, iterations))
    for i_x1 in reversed(iterations):
        for i_x2 in reversed(iterations):
            #MSEs.append( MSE(x_target[i:i+WINDOW], x_tomatch) )
            MSEs[i_x1, i_x2] = MSE(x_target[i:i+WINDOW], )

    plt.plot(MSEs, 'r^')
    plt.show()
"""




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
    D_WINDOW = 10
    mean_d_total_cases = np.mean(d_total_cases[i_start:i_start+D_WINDOW])  #mean of increase of D_WINDOW days window from peak date
    mean_dd_total_cases = np.mean(dd_total_cases[i_start:])  #mean dd from peak date
    stddev_dd_total_cases = np.std(dd_total_cases[i_start:]) #std of dd from peak date
    print(f"Mean derivative of {D_WINDOW} days from peak date:", mean_d_total_cases)
    print("Mean second derivative from peak date until now:", mean_dd_total_cases)
    print("Std. dev. second derivative from peak date until now:", stddev_dd_total_cases)

    # Show prediction of total cases, applying a variation with constant second derivative `mean_dd_total_cases`
    pred = predict_tot_cases(
        total_cases,
        mean_d_total_cases,
        mean_dd_total_cases
    )

    # Set xticks. TODO set a tick for days of the predicted curve
    N_XTICKS = 5  #ticks on x-axis to plot
    date_step = ceil(len(dates_mm_dd) / N_XTICKS)  #on x-axis plot only one date every date_step
    offset = (len(dates_mm_dd)-1) % date_step  #offset of the x-axis ticks so that the last data point has its tick on x-axis
    xticks = dates_mm_dd[offset::date_step]

    plt.plot(pred, 'r--', label="Prediction")
    plt.plot(dates_mm_dd, pred[:len(dataset)], label="Available data")
    plt.legend()
    plt.xticks(xticks)
    plt.show()
    #plt.savefig("peak_prediction.png", dpi=150)

    """
       # THIS ASSUMPTION DOESN'T WORK
    # We asume that the total cases curve is (nearly) a forward translation of deaths + recovered curves
    # In other words total_cases[t - offset] =~ deaths[t] + recovered[t]. We now find this offset
    find_opt_offset(deaths+recovered, total_cases)

    plt.plot(range(len(total_cases)), total_cases)
    offset = 15
    curve = deaths + recovered
    plt.plot(range(len(curve)-offset), curve[offset:])
    plt.show()
    """


if __name__ == "__main__":
    main()



