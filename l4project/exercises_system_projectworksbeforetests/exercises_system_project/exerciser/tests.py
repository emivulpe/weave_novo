from django.test import TestCase
from django.core.urlresolvers import reverse

from exerciser.models import Step, Application 

class StepMethodTests(TestCase):
	"""
	def test_ensure_step_number_is_valid(self):
		app = Application.objects.get_or_create(name = 'test app')[]
		step = Step(application = app,order=-1)
		step.save()
		self.assertEqual((step.order >= 0), True)
		
	"""


class IndexViewTests(TestCase):

	def test_index_view_with_no_applications(self):
		"""
		If no applications exist, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no applications present!")
		self.assertQuerysetEqual(response.context['applications'], [])
		
	def test_index_view_with_applications(self):
		"""
		If no applications exist, an appropriate message should be displayed.
		"""
		app1 = Application.objects.get_or_create(name = 'app1')[0]
		app2 = Application.objects.get_or_create(name = 'app2')[0]
		app3 = Application.objects.get_or_create(name = 'app3')[0]
		app4 = Application.objects.get_or_create(name = 'app4')[0]


		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "app1")

		num_apps =len(response.context['applications'])
		self.assertEqual(num_apps , 4)