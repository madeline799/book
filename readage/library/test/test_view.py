from django.contrib.auth.models import User
from django.core import urlresolvers
from library.models import MyUser
from django.test import TestCase
from django.test.client import RequestFactory
from library.views import ajax_comment, comment

class SimpleTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.myuser = MyUser()
        self.myuser.register('shabi','shabi','aza@gmail.com','shabi')
        self.user = self.myuser.user


    def test_nonInteger(self):
        # Create an instance of a GET request.
        request = self.factory.get(urlresolvers.reverse_lazy('library:ajax_comment', args=(6, )), {'page':'abc'})
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = ajax_comment(request, 6)
        self.assertEqual(response.status_code, 200)
        
    def test_EmptyPage(self):
        # Create an instance of a GET request.
        request = self.factory.get(urlresolvers.reverse_lazy('library:ajax_comment', args=(6, )), {'page':'9999'})
        request.user = self.user
        response = ajax_comment(request, 6)
        self.assertEqual(response.status_code, 200)


    def test_Http404(self):
        request = self.factory.post(urlresolvers.reverse_lazy('library:comment', args=(9999, )), {'title':'a', 'content':'b', 'rate':'2', 'spoiler':'true'})
        request.user = self.user
        response = comment(request, 9999)


    def test_OutRange(self):
        request = self.factory.post(urlresolvers.reverse_lazy('library:comment', args=(6, )), {'title':'a', 'content':'b', 'rate':'18', 'spoiler':'true'})
        request.user = self.user
        response = comment(request, 6)
        
        
    def test_PostError(self):
        request = self.factory.post(urlresolvers.reverse_lazy('library:comment', args=(6, )), {'title':'a', 'content':'b', 'rate':'2'})
        request.user = self.user
        response = comment(request, 6)


    def test_MethodError(self):
        request = self.factory.get(urlresolvers.reverse_lazy('library:comment', args=(6, )), {'title':'a', 'content':'b', 'rate':'2', 'spoiler':'true'})
        request.user = self.user
        response = comment(request, 6)

