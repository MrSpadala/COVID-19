# Generate new images for the README when there are new updates

python stats_province.py BG --save
python stats_province.py BG MI RM --save

rm generated/*
mv *.png generated/

echo "Images updated"
