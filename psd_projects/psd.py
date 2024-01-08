from psd_tools import PSDImage
from dot_finder import find_black_dot

# Load the PSD file
psd = PSDImage.open('ev.psd')

# save as png file each smart object
for layer in psd.descendants():
    layer.composite().save(layer.name + '.png')


# Function to list smart objects
def list_smart_objects(psd):
    smart_objects = []
    for layer in psd.descendants():
        print(layer.bbox)
        data = {}
        data['name'] = layer.name
        data['bbox'] = layer.bbox
        data['door'] = find_black_dot(layer.name + '.png')
        smart_objects.append(data)
    return smart_objects



# save as png
psd.composite().save('ev.png')

# List the smart objects
smart_objects = list_smart_objects(psd)
print("Smart Objects:", smart_objects)
