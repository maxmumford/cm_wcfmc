import argparse

from WhoCanFixMyCar import WhoCanFixMyCar

parser = argparse.ArgumentParser(description='Pass the email and password for wcfmc')
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
args = parser.parse_args()

jobs = WhoCanFixMyCar(args.email, args.password).get_jobs()
for job in jobs:
	print job
