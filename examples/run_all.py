# examples/run_all.py
from ntf.core import NTF


if __name__ == '__main__':
	ntf = NTF('inventory.yaml')
	results = ntf.run_all()
	print("Done. Wrote reports/report.json")