
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

# Return the dataset indexes corresponding to stop and start dates specified
# dates must be in MM-DD format. The stop index is incremented by one.
def filter_date(dataset, date_start=None, date_stop=None):
    i_start = 0 if date_start == None else -1
    i_stop = len(dataset)-1 if date_stop == None else -1

    for i, v in enumerate(dataset):
        date = date_format(v["data"])
        if date == date_start:
            i_start = i
        if date == date_stop:
            i_stop = i

    if i_stop == -1 or i_start == -1:
        raise Exception("One of the dates not found")

    return i_start, i_stop+1





# Returns a list of the total cases given the dataset
def get_total_cases(dataset):
    return [x["totale_casi"] for x in dataset]

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
    dataset = load_data()
    PEAK_DATE = "03-22"  #so it seems from data
    i1, i2 = filter_date(dataset, date_start=PEAK_DATE)
    #i1, i2 = filter_date(dataset, date_stop="03-21")
    xticks = [date_format(x["data"]) for x in dataset]

    total_cases = get_total_cases(dataset)
    d_total_cases = get_increases(total_cases)
    dd_total_cases = get_increases(d_total_cases)
    mean_dd_total_cases = np.mean(dd_total_cases[i1:i2])  #mean dd from peak date
    stddev_dd_total_cases = np.std(dd_total_cases[i1:i2]) #std of dd from peak date
    print("Mean second derivative from peak date until now::", mean_dd_total_cases)
    print("Std. dev. second derivative from peak date until now:", stddev_dd_total_cases)

    pred = predict_tot_cases(
        total_cases,
        np.mean(d_total_cases[i1:i2]),
        mean_dd_total_cases
    )

    plt.plot(pred, 'r--')
    plt.plot(pred[:len(dataset)])
    plt.show()

    #plt.plot(xticks, dd_total_cases)
    #plt.show()

    """
    total_cases = get_total_cases(dataset)
    plt.plot(xticks[i1:i2], total_cases[i1:i2])
    plt.title("Casi totali")
    plt.show()

    increases = get_increases(total_cases)
    plt.plot(xticks[i1:i2], increases[i1:i2])
    plt.title("Increases casi totali")
    plt.show()

    increases_2 = get_increases(increases)
    print("Mean second derivative: ", np.mean(increases_2[i1:i2]))
    plt.plot(xticks[i1:i2], increases_2[i1:i2])
    plt.title("Increases of increases casi totali")
    plt.show()
    """



if __name__ == "__main__":
    main()



