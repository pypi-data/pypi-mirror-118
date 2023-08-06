from scraper.OQMD_new_version import CompoundScraper
from scraper.periodic_table_new import PeriodicTableScraper
import argparse

'''

This is a script to execute a specific scraper instance based
on a selected url. For this scraper, there are only two choices of url;

(1) OQMD website - "http://oqmd.org/api/search#apisearchresult"
(2) Periodic table webiste -"https://pubchem.ncbi.nlm.nih.gov/periodic-table/#view=list"

This code can be executed by making use of the flags -r and '--root'
Example: python example.py -r [insert url]


'''

# parser = argparse.ArgumentParser()
# parser.add_argument("-r", "--root", dest="root", help="webpage url", type=str)
# args = parser.parse_args()


root = input()

if root == "http://oqmd.org/api/search#apisearchresult":
    features = {'Name':[], 'Spacegroup':[], 'Volume':[], 'Band_gap':[]}
    scraper = CompoundScraper(n=1, root=root, list=[], features=features)
    scraper.extract_data()

elif args.root == "https://pubchem.ncbi.nlm.nih.gov/periodic-table/#view=list":
    features = {'Element_Name':[], 'Atomic_Number':[], 'Electronegativity':[], 'Boiling_Point':[]}
    scraper = PeriodicTableScraper(n=5, root=root, list=[], features=features)
    scraper.extract_data(to_DF=True)
else:
    print(f"Enter a valid URL")


