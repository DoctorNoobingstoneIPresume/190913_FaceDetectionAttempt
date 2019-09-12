import glob
import sys
from getFacesAndAlign import saveFaceFromImage

# pentru fiecare imagine din folder se va identifica fata => va fi salvata
# intr-un folder separat cu un id (cel cu care incepe numerotarea folderului).
# id-ul va corespunde cu persoana
print ("Save Faces....")
saveFaceFromImage()
