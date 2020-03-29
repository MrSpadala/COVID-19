
import sys
import json
from pprint import pprint
from matplotlib import pyplot as plt

# Path of the .json dataset by provincia
DATA_FPATH = "../dati-json/dpc-covid19-ita-province.json"



if len(sys.argv) <= 1:
	print(" [ITA] Grafica l'andamento e l'incremento dei casi positivi per le provincie specificate")
	print(" [ENG] Plots the number and the increment of positive cases for the requested provices")
	print(f"\tUsage: {sys.argv[0]} provincia1 provincia2 ...")
	print(f"\texample: {sys.argv[0]} MI RM VE")
	exit(1)

# Retrieve the input provinces as args, transform to uppercase 
provinces_input = list(
	map(str.upper, sys.argv[1:])
)



# Load .json province data
with open(DATA_FPATH, encoding="utf-8-sig") as f:
    data = json.load(f)

# Create a set of available provinces
provinces = set([x["sigla_provincia"].upper() for x in data])

# Check if the requested provinces are in the data, otherwise throw an error
for prov in provinces_input:
	if not prov in provinces:
		print(f"Error: bad province {prov}")
		exit(1)



# Loop over requested provinces and plot positive cases and increment
for prov in provinces_input:
	# Filter only requested area
	data_prov = list(
	    filter(lambda x: x["sigla_provincia"]==prov, data)
	)

	# Extract the positive cases
	positives = [x["totale_casi"] for x in data_prov]
	# Remove null elements if present
	#positives = [x if x != None else 0 for x in positives]

	# Calculate the increment of positive cases day by day
	increments = [positives[0]]
	for i in range(1, len(positives)):
	    increments.append(positives[i] - positives[i-1])

	# Transform dates from ISO format YYYY-MM-DDTHH:MM:SS to MM-DD
	dates = [x["data"][5:10] for x in data_prov]


	# Now for the plots, we have too much datapoints to have all of them on the x-axis
	# So we calculate how many ticks on x-axis we have to put
	DATE_STEP = 4  #on x-axis plot only one date every DATE_STEP
	offset = (len(dates)-1) % DATE_STEP  #offset of the x-axis ticks so that the last data point has its tick on x-axis
	xticks = dates[offset::DATE_STEP]

	# Plot positive cases
	positives_plot = plt.figure(1)
	plt.title("Casi Positivi")
	plt.plot(dates, positives, label=prov)
	plt.xticks(xticks)
	plt.legend()
	# horizontal line on the highest value if there are different provinces
	if len(provinces_input) > 1:
		plt.hlines(max(positives), 0, len(dates)-1, "darkred", "--", linewidth=1)

	# Plot increments
	increments_plot = plt.figure(2)
	plt.title("Incremento Giornaliero Positivi")
	plt.plot(dates, increments, label=prov)
	plt.xticks(xticks)
	plt.legend()

# Finally show the data
plt.show()
