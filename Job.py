class Job():
	""" Represents a job on the WCFMC website """
	def __init__(self, job_id, date, service, registration, make_model, registration_year, city, postcode, comments):
		self.job_id = job_id
		self.date = date
		self.service = service
		self.registration = registration
		self.make_model = make_model
		self.registration_year = registration_year
		self.city = city
		self.postcode = postcode
		self.comments = comments

	def __str__(self):
		return str(self.job_id) + ': ' + self.service + ' on ' + self.registration + ' in ' + self.city + ', ' + self.postcode
