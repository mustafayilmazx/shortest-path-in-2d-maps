from psd_tools import PSDImage

# save as png
PSDImage.open('ev.psd').composite().save('ev.png')
