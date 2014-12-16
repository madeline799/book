from datetime import datetime
from random import choice

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import HttpResponse

from library.models import Book, Info, MyUser, BookCopy, Borrowing, Comment, Rank
from library.models import change_model
from library.forms import RegisterForm, LoginForm
from library.views_helper import FC, render_JSON_OK, render_JSON_Error, \
    POST_required, login_required_JSON, catch_404_JSON, get_page, \
    catch_PermException_JSON, catch_Assertion_JSON


COMMENT_PAGE_SIZE_0 = 0
COMMENT_PAGE_SIZE = 2


def index(request):
    """Show index page.

    GET:

    Renders library/index.html with:
    rank  -- latest rank list by rate
    news  -- latest 5 pieces of news
    guide -- latest 5 pieces of guide
    """
    return render(request, 'library/index.html', {
        'rank': Rank.get_top(),
        'news': Info.get_all('news')[:5],
        'guide': Info.get_all('guide')[:5],
        })


def search(request):
    """Search for books.

    GET:
    q     -- the query string
    lucky -- whether the lucky button is clicked

    Renders library/searchResult.html with:
    q      -- the query string
    result -- search result, as a list of books
    """
    q = request.GET.get('q', '')
    lucky = 'lucky' in request.GET
    if lucky:
        try:
            book = choice(Book.objects.all())
            return redirect('library:book', book.id)
        except IndexError as err:
            pass
    return render(request, 'library/searchResult.html', {
        'q': q,
        'result': Book.search(q),
        })


def book(request, book_id):
    """Show the detail page for a certain book.

    GET:

    Renders library/book-detail.html with:
    book             -- the book object
    copy             -- a list of all copies of this book
    comment_count    -- number of comments on this book
    comment & range5 -- latest comment list, and template helper
    """
    book = get_object_or_404(Book, pk=book_id)
    copy = book.bookcopy_set.all()
    comment = book.comment_set.all()[:COMMENT_PAGE_SIZE_0]
    '''    is_book_admin = request.user.is_authenticated()
    if is_book_admin:
        try:
            myuser = request.user.myuser
            is_book_admin = myuser.get_admin_type() == 'book manager'
        except MyUser.DoesNotExists as err:
            is_book_admin = False
    '''
    return render(request, 'library/book-detail.html', {
        'book': book,
        'copy': copy,
        'comment_count': book.comment_set.all().count(),
        'comment': comment,
        'range5': range(1, 6),
        'is_book_admin': False,
        })


@POST_required('title', 'content', 'rate', 'spoiler')
@login_required_JSON()
@catch_404_JSON
def comment(request, book_id):
    """Add a comment for the book specified by book_id.

    POST:
    title   -- the title of the comment
    content -- the content of the comment
    rate    -- the rate associated with the comment
    spoiler -- whether this comment is a spoiler

    Renders JSON: (besides 'status' or 'err')

    User is derived from the session.
    """
    myuser = request.user.myuser
    book = get_object_or_404(Book, pk=book_id)
    title = request.POST['title']
    content = request.POST['content']
    rate = request.POST['rate']
    if rate not in {str(i) for i in range(1, 6)}:
        return render_JSON_Error('Invalid rate.')
    rate = int(rate)
    spoiler = request.POST['spoiler'] == 'true'
    Comment.add(myuser, book, title, content, rate, spoiler)
    return render_JSON_OK({})


def ajax_comment(request, book_id):
    """Fetch comments for the book specified by book_id.

    GET:
    page -- the desired page. 0 is reserved for the default ones returned on
            the book page. The first load operation should use 1 (default).
            Large page numbers exceeds the total number returns empty list.
    Other parameters may be used such as 'last_date' or 'last_id', so it's not
    a good idea to put them into URL.

    Renders library/fetch_comment.html for AJAX load with:
    comment & range5 -- (on 'OK') a list of comments, and template helper

    Everyone can view comments.
    """
    book = get_object_or_404(Book, pk=book_id)
    page = request.GET.get('page', 1)
    comment_list = book.comment_set.all()[COMMENT_PAGE_SIZE_0:]
    paginator = Paginator(comment_list, COMMENT_PAGE_SIZE)
    comment = get_page(paginator, page)
    return render(request, 'library/fetch_comment.html', {
        'comment': comment,
        'range5': range(1, 6),
        })


@POST_required()
def login(request):
    """Backend for AJAX login.

    POST:
    username -- username to login
    password -- password of the username

    Renders JSON: (besides 'status' or 'err')
    username -- (on 'OK') username of the logged in user
    name     -- (on 'OK') name of the logged in user
    detail   -- (on 'Error') error list from form validation

    POST data will be validated by LoginForm.
    """
    form = LoginForm(request.POST)
    if form.is_valid():
        user = auth.authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            )
        if user is not None:
            if user.is_active:
                try:
                    user.myuser
                except MyUser.DoesNotExist as err:
                    return render_JSON_Error('Root cannot login here.')
                auth.login(request, user)
                return render_JSON_OK({
                    'username': user.username,
                    'name': user.myuser.name,
                    })
        return render_JSON_Error('Login failed.')
    return render_JSON_Error('Login syntax error.', {
        'detail': form.errors,
        })


@POST_required()
def register(request):
    """Backend for AJAX register.

    POST:
    username  -- username of the new user
    password  -- password of the new user
    password2 -- password confirm
    email     -- email of the new user
    name      -- name of the new user

    Renders JSON: (besides 'status' or 'err')
    username -- (on 'OK') username of the logged in user
    name     -- (on 'OK') name of the logged in user
    detail   -- (on 'Error') error list from form validation

    POST data will be validated by RegisterForm.
    """
    form = RegisterForm(request.POST)
    if form.is_valid():
        u = MyUser()
        try:
            u.register(
                form.cleaned_data['username'],
                form.cleaned_data['password'],
                form.cleaned_data['email'],
                form.cleaned_data['name'],
                )
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                )
            assert user is not None
            auth.login(request, user)
            return render_JSON_OK({
                'username': user.username,
                'name': user.myuser.name,
                })
        except IntegrityError as err:
            return render_JSON_Error('Username taken.')
    return render_JSON_Error('Register syntax error.', {
        'detail': form.errors,
        })


def logout(request):
    """Backend for AJAX logout.

    GET or POST:

    Renders JSON: (besides 'status' or 'err')

    Always returns OK.
    """
    auth.logout(request)
    return render_JSON_OK({})


@login_required(login_url=reverse_lazy('library:index'))
def user(request):
    """Show the user panel page.

    GET:

    Renders library/user-panel.html with:
    profile          -- myuser object of the current user
    book_borrowing   -- list of all borrowing copies
    book_queue       -- list of all queuing copies
    book_borrowed    -- list of all borrowed copies
    comment & range5 -- list of all comments posted, and template helper

    Redirect to library:index if not logged in.
    Redirect to library:ad_book if book admin logged in.
    Redirect to library:ad_user if user admin logged in.
    Redirect to admin:index if root.
    """
    try:
        myuser = request.user.myuser
    except MyUser.DoesNotExist as err:
        return redirect('admin:index')
    if myuser.get_admin_type() == 'book manager':
        return redirect('library:ad_book')
    elif myuser.get_admin_type() == 'user manager':
        return redirect('library:ad_user')
    return render(request, 'library/user-panel.html', {
        'profile': myuser,
        'book_borrowing': myuser.get_all_borrowing(),
        'book_queue': myuser.get_all_queue(),
        'book_borrowed': myuser.get_all_borrowed(),
        'comment': myuser.comment_set.all(),
        'range5': range(1, 6),
        })


@POST_required('email')
@login_required_JSON()
@catch_Assertion_JSON
def user_edit(request):
    """Backend for AJAX modification of user's email and password.

    POST:
    email  -- new email address
    pass0  -- (optional) old password
    pass1  -- (optional) new password
    pass2  -- (optional) new password repeated

    Renders JSON: (besides 'status' or 'err')
    """
    pass_mod = map(
        lambda f: f in request.POST and request.POST[f] != '',
        ['pass0', 'pass1', 'pass2'],
        )
    pass_none = not reduce(bool.__or__, pass_mod)
    pass_all = reduce(bool.__and__, pass_mod)
    myuser = request.user.myuser
    fake_register = {
        'username': 'fake_user',
        'password': 'fake_pass',
        'password2': 'fake_pass',
        'email': request.POST['email'],
        'name': 'Fake User',
        }
    if pass_none:
        f = RegisterForm(fake_register)
        if f.is_valid():
            myuser.update_user(request.POST['email'])
        else:
            return render_JSON_Error('Invalid email address.')
    elif pass_all:
        fake_register['password'] = request.POST['pass1']
        fake_register['password2'] = request.POST['pass2']
        f = RegisterForm(fake_register)
        if f.is_valid():
            myuser.update_user(
                request.POST['email'],
                request.POST['pass0'],
                request.POST['pass1'],
                )
        else:
            if 'email' in f.errors:
                return render_JSON_Error('Invalid email address.')
            elif 'password' in f.errors:
                return render_JSON_Error('New password is too short.')
            elif 'password2' in f.errors:
                return render_JSON_Error('New passwords do not match.')
            else:
                return render_JSON_Error('Syntax error.', {'detail': f.errors})
    else:
        return render_JSON_Error('Password fields incomplete.')
    return render_JSON_OK({})


@POST_required()
@login_required_JSON()
@catch_Assertion_JSON
def user_upward(request):
    """Backend for AJAX user upward request.

    POST:

    Renders JSON: (besides 'status' or 'err')
    """
    myuser = request.user.myuser
    myuser.upward_request()
    return render_JSON_OK({})


@POST_required('username')
@catch_404_JSON
def user_forget(request):
    """Backend for AJAX password reset.

    POST:
    username  -- username of the user whose password will be reset

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404
                (on 'OK') readable success message
    """
    myuser = get_object_or_404(MyUser, user__username=request.POST['username'])
    myuser.reset_password()
    return render_JSON_OK({
        'message': 'Your new password has been sent to your email.',
        })


@POST_required('title', 'content')
@login_required_JSON()
def feedback(request):
    """Backend for AJAX feedback. Sends an email to all admins.

    POST:
    title    -- title of the feedback email
    content  -- content of the feedback email

    Renders JSON: (besides 'status' or 'err')
    """
    send_mail(
        '[ReadTogether] Feedback: ' + request.POST['title'],
        request.POST['content'] +
        '\n\n Sent from ' + request.META.get('HTTP_REFERER', 'unknown page.'),
        request.user.email,
        MyUser.get_admin_email(),  # Which admin to send to?
        fail_silently=False,
        )
    return render_JSON_OK({})


@POST_required()
@login_required_JSON()
@catch_404_JSON
@catch_PermException_JSON
def queue(request, copy_id):
    """Backend for AJAX copy queueing.

    POST:

    Renders JSON: (besides 'status' or 'err')
    username -- (on 'OK') username of the queuing user
    copy_id  -- (on 'OK') copy_id of the queued copy
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Queuing is done by myuser itself.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.queue(request.user.myuser, copy)
    return render_JSON_OK({
        'username': request.user.username,
        'copy_id': copy_id,
        })


@POST_required()
@login_required_JSON()
@catch_404_JSON
@catch_PermException_JSON
def reborrow(request, copy_id):
    """Backend for AJAX copy reborrow.

    POST:

    Renders JSON: (besides 'status' or 'err')
    username -- (on 'OK') username of the reborrowing user
    copy_id  -- (on 'OK') copy_id of the reborrowed copy
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Reborrowing is done by myuser itself.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.reborrow(request.user.myuser, copy)
    return render_JSON_OK({
        'username': request.user.username,
        'copy_id': copy_id,
        })


@POST_required()
@login_required_JSON()
@catch_404_JSON
@catch_Assertion_JSON
def queue_del(request, copy_id):
    """Backend for AJAX queue deletion.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404

    Queue deletion is done by myuser itself.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.queue_del(request.user.myuser, copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def borrow(request, copy_id, myuser_id):
    """Backend for AJAX book borrow.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Can only be called by book admin.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    myuser = get_object_or_404(MyUser, pk=myuser_id)
    Borrowing.borrow(myuser, copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def back(request, copy_id):
    """Backend for AJAX book return.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Can only be called by book admin.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.return_book(copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def queue_next(request, copy_id, myuser_id):
    """Backend for AJAX book queue_next.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Can only be called by book admin.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    myuser = get_object_or_404(MyUser, pk=myuser_id)
    Borrowing.queue_next(myuser, copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def readify(request, copy_id):
    """Backend for AJAX book readify.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Can only be called by book admin.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.readify(copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def disappear(request, copy_id):
    """Backend for AJAX book disappear.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404 or Permission Error

    Can only be called by book admin.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.disappear(copy)
    return render_JSON_OK({})


BOOK_FIELDS = [
    'duration', 'title', 'author', 'press', 'pub_year', 'revision', 'ISBN',
    'title_other', 'translator', 'pub_year_origin', 'revision_origin',
    ]


def book_fields_clean(post_data):
    """Helper function to verify book field data."""
    clean_data = {}
    for field in BOOK_FIELDS:
        try:
            if field in [
                    'duration', 'pub_year', 'revision', 'pub_year_origin',
                    'revision_origin',
                    ]:
                if post_data[field] != '':
                    clean_data[field] = int(post_data[field])
                    if not (0 <= clean_data[field] <= 32767):
                        return render_JSON_Error(
                            'Field not in range: {}'.format(field),
                            )
            else:
                clean_data[field] = post_data[field]
        except ValueError as err:
            return render_JSON_Error('Field not int: {}.'.format(field))
    if clean_data['title'] == '' and clean_data['title_other'] == '':
        return render_JSON_Error('At least one of title or title_other.')
    if 'duration' in clean_data:
        clean_data['duartion'] = clean_data['duration']
        del clean_data['duration']
    return clean_data


@POST_required(*BOOK_FIELDS)
@login_required_JSON('book manager')
def book_add(request):
    """Backend for AJAX book add.

    POST:
    duration, title, author, press, pub_year, revision, ISBN,
    title_other, translator, pub_year_origin, revision_origin

    Renders JSON: (besides 'status' or 'err')
    permalink  -- (on 'OK') URL to the newly added book

    Can only be called by book admin.
    """
    clean_data = book_fields_clean(request.POST)
    if isinstance(clean_data, HttpResponse):
        return clean_data
    book = Book.objects.create(**clean_data)
    permalink = reverse_lazy('library:book', args=(book.id, ))
    return render_JSON_OK({'permalink': str(permalink)})


@POST_required(*BOOK_FIELDS)
@login_required_JSON('book manager')
@catch_404_JSON
def book_edit(request, book_id):
    """Backend for AJAX book edit.

    POST:
    duration, title, author, press, pub_year, revision, ISBN,
    title_other, translator, pub_year_origin, revision_origin

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404

    Can only be called by book admin.
    """
    book = get_object_or_404(Book, pk=book_id)
    clean_data = book_fields_clean(request.POST)
    if isinstance(clean_data, HttpResponse):
        return clean_data
    change_model(book, clean_data)
    return render_JSON_OK({})


@POST_required('location')
@login_required_JSON('book manager')
@catch_404_JSON
def copy_add(request, book_id):
    """Backend for AJAX copy add for the specified book.

    POST:
    location  -- location of the new copy

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404

    Can only be called by book admin.
    """
    book = get_object_or_404(Book, pk=book_id)
    BookCopy.objects.create(book=book, location=request.POST['location'])
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_Assertion_JSON
def copy_del(request, copy_id):
    """Backend for AJAX copy deletion for the specified copy.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404

    Can only be called by book admin.
    """
    copy = get_object_or_404(BookCopy, pk=copy_id)
    copy.set_dead(request.user.myuser)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
def comment_del(request, comment_id):
    """Backend for AJAX comment deletion.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404

    Can only be called by book admin.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.remove()
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('user manager')
@catch_404_JSON
@catch_Assertion_JSON
def updown(request, action, myuser_id):
    """Backend for AJAX user registration pass, upward and downward.

    POST:

    Renders JSON: (besides 'status' or 'err')
    message  -- (on 'Error') detailed message for 404

    Can only be called by user admin.
    """
    myuser = get_object_or_404(MyUser, pk=myuser_id)
    if action == 'reg_pass':
        myuser.reg_pass()
    elif action == 'upward':
        myuser.upward()
    else:
        assert action == 'downward'
        myuser.downward()
    return render_JSON_OK({})


@login_required(login_url=reverse_lazy('library:index'))
def ad_book(request):
    """Show the book admin panel page.

    GET:

    Renders library/book-manager-panel.html with:

    Redirect to library:index if not logged in.
    Redirect to library:user if not book admin.
    Redirect to admin:index if root.
    """
    try:
        myuser = request.user.myuser
    except MyUser.DoesNotExist as err:
        return redirect('admin:index')
    if myuser.get_admin_type() != 'book manager':
        return redirect('library:user')
    return render(request, 'library/book-manager-panel.html', {})


@login_required(login_url=reverse_lazy('library:index'))
def ad_user(request):
    """Show the user admin panel page.

    GET:

    Renders library/user-manager-panel.html with:
    user_register  -- list of MyUser objects waiting for reg_pass
    user_advance   -- list of MyUser objects waiting for upward

    Redirect to library:index if not logged in.
    Redirect to library:user if not user admin.
    Redirect to admin:index if root.
    """
    try:
        myuser = request.user.myuser
    except MyUser.DoesNotExist as err:
        return redirect('admin:index')
    if myuser.get_admin_type() != 'user manager':
        return redirect('library:user')
    return render(request, 'library/user-manager-panel.html', {
        'user_register': MyUser.objects.filter(pending=1),
        'user_advance': MyUser.objects.filter(pending=2),
        })


def ajax_myuser(request):
    """Search myuser according to query string.

    GET:
    q      -- the query string, default ''
    admin  -- (optional) parameter that determines which template to render

    if admin == 'user':
        library/fetch_myuser_down.html
    else:
        library/fetch_myuser.html

    Renders template for AJAX load with:
    myuser_list -- (on 'OK') a list of matched myuser

    No error check whether called by book admin.
    """
    q_myuser = request.GET.get('q', '')
    context = {'myuser_list': MyUser.search(q_myuser)}
    admin = request.GET.get('admin', None)
    if admin == 'user':
        return render(request, 'library/fetch_myuser_down.html', context)
    return render(request, 'library/fetch_myuser.html', context)


def info(request):
    """Show news and guide list.

    GET:

    Renders library/info.html with:
    news  -- list of all news
    guide -- list of all guide
    """
    return render(request, 'library/info.html', {
        'news': Info.get_all('news'),
        'guide': Info.get_all('guide'),
        })


def info_detail(request, info_id):
    """Show the content of the specific news or guide.

    GET:

    Renders library/info.html with:
    info  -- current info object
    news  -- list of all news
    guide -- list of all guide
    """
    info = get_object_or_404(Info, pk=info_id)
    return render(request, 'library/info.html', {
        'info': info,
        'news': Info.get_all('news'),
        'guide': Info.get_all('guide'),
        })


@POST_required('title', 'content', 'species')
@login_required_JSON('user manager')
def info_add(request):
    """Backend for AJAX info add.

    POST:
    title    -- title of the news or guide
    content  -- content of the news or guide
    species  -- 'news' or 'guide'

    Renders JSON: (besides 'status' or 'err')

    Can only be called by user admin.
    """
    name2id = {name: id for id, name in Info.species_choice}
    if request.POST['species'] not in name2id:
        return render_JSON_Error('Neither news nor guide: {}.'.format(
            request.POST['species'],
            ))
    Info.objects.create(
        title=request.POST['title'],
        content=request.POST['content'],
        species=name2id[request.POST['species']],
        )
    return render_JSON_OK({})


def rank(request, ver=0):
    """Show the rank page.

    GET:

    Renders library/rank.html with:
    ver             -- version of the rank, 0 (default) for latest
    rank_by_borrow  -- rank list by borrow count
    rank_by_comment -- rank list by comment count
    rank_by_rate    -- rank list by rate
    range5          -- template helper
    """
    ver_max = Rank.get_maxversion()
    if ver == '0' or int(ver) > ver_max:
        return redirect('library:rank')
    ver_real = int(ver) or ver_max
    link_old = link_new = ''
    if ver_real > 1:
        link_old = str(reverse_lazy('library:rank_old', args=(ver_real - 1, )))
    if ver_real < ver_max:
        link_new = str(reverse_lazy('library:rank_old', args=(ver_real + 1, )))
    return render(request, 'library/rank.html', {
        'ver': ver_real,
        'rank_by_borrow': Rank.get_top(0, ver_real),
        'rank_by_comment': Rank.get_top(1, ver_real),
        'rank_by_rate': Rank.get_top(2, ver_real),
        'range5': range(1, 6),
        'link_old': link_old,
        'link_new': link_new,
        })


# def test(request):
#     """Dummy page for various on-hand snippets."""
#     comment = Comment.objects.all()
#     return render(request, 'library/fetch_comment.html', {
#         'comment': comment,
#         'range5': range(1, 6),
#         })
