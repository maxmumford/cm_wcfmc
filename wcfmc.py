import argparse

from WhoCanFixMyCar import WhoCanFixMyCar

parser = argparse.ArgumentParser(description='Pass the email and password for wcfmc')
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)
args = parser.parse_args()

wcfmc = WhoCanFixMyCar(args.email, args.password)
job_ids = wcfmc.get_find_job_ids()
for job_id in job_ids:
	print wcfmc.get_job(job_id)
