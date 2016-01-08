from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None
	form = ItemForm()
	if request.method == 'POST':
		form = ItemForm(data=request.POST)
		if form.is_valid():
			Item.objects.create(text=request.POST['text'], list=list_)
			return redirect(list_)
	return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
	#1 We pass the request.POST data into the form's constructor
	form = ItemForm(data=request.POST)
	#2 We use form.is_valid() to determine whether this is a good or bad submission
	if form.is_valid():
		list_ = List.objects.create()
		Item.objects.create(text=request.POST['text'], list=list_)
		return redirect(list_)
	else:
		#3 In the invalid case, we pass the form down to the template, instead of our hardcoded
		#error string
		return render(request, 'home.html', {"form": form})
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	return redirect(list_)

	''' Old request method
	item = Item()
	item.text = request.POST.get('item_text', '')
	item.save()
	return render(request, 'home.html', {
		'new_item_text': item.text
	})
	'''
