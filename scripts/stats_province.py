
import sys
import json
import argparse
from math import ceil
from pprint import pprint
from matplotlib import pyplot as plt

# Path of the .json dataset by provincia
DATA_FPATH = "../dati-json/dpc-covid19-ita-province.json"



def main():

	# Parses arguments from cmd line
	args, provinces_input = get_args()

	# Load .json province data
	with open(DATA_FPATH, encoding="utf-8-sig") as f:
	    data = json.load(f)

	# Create a set of available provinces
	provinces = set([x["sigla_provincia"].upper() for x in data])

	# Check if the requested provinces are in the data, otherwise throw an error
	for prov in provinces_input:
		if not prov in provinces:
			print(f"Error: province {prov} not found")
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
		N_XTICKS = 9  #ticks on x-axis to plot
		date_step = ceil(len(dates) / N_XTICKS)  #on x-axis plot only one date every date_step
		offset = (len(dates)-1) % date_step  #offset of the x-axis ticks so that the last data point has its tick on x-axis
		xticks = dates[offset::date_step]

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

	# Finally show the data, or save it if it was passed --save argument
	plt.show()


	#plt.savefig("MI_BG.png", dpi=300)



def get_args():
	""" Parses input arguments, returns tuple (args, province) """
	usage = f"""
[ITA] Grafica l'andamento e l'incremento dei casi positivi per le provincie specificate
[ENG] Plots the number and the increment of positive cases for the requested provices
\tUsage: {sys.argv[0]} provincia1 provincia2 ...
\texample: {sys.argv[0]} MI RM VE
"""
	parser = argparse.ArgumentParser(description="Covid-19, statistiche per province")
	parser.usage = usage
	parser.add_argument('--save', help='Saves the image as png image', action='store_true', default=False)
	args, province = parser.parse_known_args()
	if len(province) == 0:
		parser.error("Need at least one provincia")
	return args, province


if __name__ == '__main__':
	main()