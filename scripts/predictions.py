
import json
import numpy as np
from matplotlib import pyplot as plt

# Path of the dataset in JSON
DATA_FPATH = "../dati-json/dpc-covid19-ita-andamento-nazionale.json"

def load_data():
    with open(DATA_FPATH, encoding="utf-8-sig") as f:
        return json.load(f)

def transform_date(date_original):
    return date_original[5:10]  #extract from date MM-DD

def filter_date(dataset, date_start=None, date_stop=None):
    i_start = 0 if date_start == None else -1
    i_stop = len(dataset)-1 if date_stop == None else -1

    for i, v in enumerate(dataset):
        date = transform_date(v["data"])
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



def main():
    dataset = load_data()
    i1, i2 = filter_date(dataset, date_start="03-22")
    xticks = [transform_date(x["data"]) for x in dataset]

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



if __name__ == "__main__":
    main()



