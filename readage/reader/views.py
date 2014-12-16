from django.shortcuts import render

# Create your views here.

def reader(request, book_id):
    """Show reading page.

    GET:

    Renders library/index.html with:
    book_id  
    """
    return render(request, 'reader/reader.html', {

        })

