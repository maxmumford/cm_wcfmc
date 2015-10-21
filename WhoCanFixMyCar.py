import requests
from bs4 import BeautifulSoup
from datetime import date

from Job import Job

WCFMC_LOGIN_URL = 'https://www.whocanfixmycar.com/login'
WCFMC_GET_JOBS_URL = 'https://www.whocanfixmycar.com/find-jobs?page='
WCFMC_JOB_URL = 'https://www.whocanfixmycar.com/mechanic/jobs/'

class WhoCanFixMyCar():
	""" Data scraper for whocanfixmycar.com """

	def __init__(self, email, password):
		self.session = requests.Session()
		self.login(email, password)

	def login(self, email, password):
		login = self.session.post(WCFMC_LOGIN_URL, data={'email': email, 'password': password})
		if 'Wrong user email or password' in login.content:
			raise ValueError('Could not log in')

	def get_jobs(self):
		# get job ids
		page = 1
		jobs_request = self.session.get(WCFMC_GET_JOBS_URL + str(page))
		soup = BeautifulSoup(jobs_request.text)
		jobs = []
		job_elements = soup.findAll('div', attrs={'class': 'card_job'})

		for job_element in job_elements:
			job_id = job_element.find('a', attrs={'class': 'card__title'}).get('href').split('/')[3]
			job_date_raw = job_element.find('div', attrs={'class': 'card__date'}).text
			if ':' in job_date_raw:
				job_date = date.today()
			else:
				job_date = date(*map(lambda date_part: int(date_part), reversed(job_date_raw.split('/'))))
			
			job_service = job_element.find(text='service').parent.nextSibling.nextSibling.text
			job_registration = job_element.find(text='registration').parent.nextSibling.nextSibling.text
			job_make_model = job_element.find(text='make & model').parent.nextSibling.nextSibling.text
			job_registration_year = job_element.find(text='registration year').parent.nextSibling.nextSibling.text

			job_location_raw = job_element.find(text='location').parent.nextSibling.nextSibling.text
			job_city, job_postcode = job_location_raw.split(', ')

			# load job page to get comment
			job_request = self.session.get(WCFMC_JOB_URL + str(job_id))
			soup = BeautifulSoup(job_request.text)
			comments = soup.find('div', attrs={'class': 'card'}).findAll('div', attrs={'class': 'col-sm-6'})[1].findAll('p')
			if len(comments):
				job_comment = [comment.text for comment in comments]
			else:
				job_comment = []

			job = Job(job_id, job_date, job_service, job_registration, job_make_model, job_registration_year, job_city, job_postcode, job_comment)
			jobs.append(job)

		return jobs
