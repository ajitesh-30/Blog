from django.test import TestCase
from django.core.urlresolvers import reverse

class HomesTests(TestCase):
	def test_home_view_status_code(self):
		url = reverse('home')
		response = self.client.get(url)
		self.assertEquals(response.status_code,200)

	def test_home_url_resolvers_home_views(self):
		view = resolve('/')
		self.assertEquals(view.func,home)
# Create your tests here.
