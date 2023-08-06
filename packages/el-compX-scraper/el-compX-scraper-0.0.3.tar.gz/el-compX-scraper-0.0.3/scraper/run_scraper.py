from OQMD_new_version import CompoundScraper
from periodic_table_new import PeriodicTableScraper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--root", dest="root", help="webpage url", type=str)
args = parser.parse_args()



if __name__ == '__main__':
    if args.root == "http://oqmd.org/api/search#apisearchresult":
        features = {'Name':[], 'Spacegroup':[], 'Volume':[], 'Band_gap':[]}
        scraper = CompoundScraper(n=1, root=args.root, list=[], features=features)
        scraper.extract_data()
    
    elif args.root == "https://pubchem.ncbi.nlm.nih.gov/periodic-table/#view=list":
        features = {'Element_Name':[], 'Atomic_Number':[], 'Electronegativity':[], 'Boiling_Point':[]}
        scraper = PeriodicTableScraper(n=5, root=args.root, list=[], features=features)
        scraper.extract_data(to_DF=True)
    else:
        print(f"Enter a valid URL")
    

