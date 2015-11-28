from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string


from lists.views import home_page
from lists.models import Item
# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() # Create an HttpRequest object, which is what Django will see when a user's browser asks for a page
        response = home_page(request) # We pass it to our home_page view, which gives us a response. You won't be surprised to hear that this object is an instance of a class called HttpResponse. Then, we assert that the .content of the response, which is the HTML that we send to the user-- has certain properties.
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
    	request = HttpRequest()
    	request.method = 'POST'
    	request.POST['item_text'] = 'A new list item'

    	response = home_page(request)

    	self.assertIn('A new list item', response.content.decode())
    	#When we run the unit test, render_to_string will substitue {{ new_item_text }} for
    	#a new list item inside the <td>
    	expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
    	self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

