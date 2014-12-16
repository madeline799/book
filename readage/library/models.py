from __future__ import unicode_literals
import datetime
from textwrap import dedent

from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate
from django.db.models.query import QuerySet
from django.core.mail import send_mail


class PermException(Exception):
    """define Exception reporting permission Exceprtion"""
    pass


def get_field_changeable(obj):
    """get all field that can be changed in models"""
    return [
        name for name in obj.__dict__.keys()
        if not (name.startswith('_') or name.endswith('id'))
        ]


@transaction.atomic
def change_model(obj, dic):
    """update model by dict"""
    field_changeable = get_field_changeable(obj)
    for key, value in dic.iteritems():
        if key not in field_changeable:
            raise PermException('field '+key+' is not changeable')
        obj.__dict__[key] = value
    obj.save()


class Book(models.Model):
    """
    the Book Model
    info to identify a Book.
    
    Field:

    title           -- name of the book
    author          -- authors of the book, separatr by ','
    press           -- the press of the book
    pub_year        -- the publish year of the book
    revision        -- the newest version of the book
    ISBN            -- the ISBN-13 code of the book
    RABOOKCODE      -- unique code to indeify a book/document when ISBN is empty.
    derivedfrom     -- refer to original book, based on which this book is derived.
    """

    title = models.CharField(max_length=200, default="")
    author = models.CharField(max_length=300)
    press = models.CharField(max_length=200)
    pub_year = models.SmallIntegerField(default=0)
    revision = models.SmallIntegerField(default=0)
    ISBN = models.CharField(max_length=64)
    RABOOKCODE = models.CharField(max_length=256, blank=True)
    derivedfrom = models.CharField(max_length=256,blank=True)

    @staticmethod
    def _search_part(string):
        """search for string in title, author or press"""
        re1 = Book.objects.filter(title__icontains=string)
        re3 = Book.objects.filter(author__icontains=string)
        re4 = Book.objects.filter(press__icontains=string)
        return re1 | re3 | re4

    @staticmethod
    def search(string):
        """
        make the word split with whitespace
        and get their search result union.
        """
        s = string.split()
        re = Book.objects.none()
        for ss in s:
            re = re | Book._search_part(ss)
        return re

    def simple_name(self):
        """return a simple name"""
        return self.title

    def simple_version(self):
        """return a simple version"""
        return 'ver %d, %d' % (
            self.revision, self.pub_year,
            )

    def __unicode__(self):
        """only for debug"""
        return self.title+" "+self.author+" "+self.ISBN


class BookCopy(models.Model):

    """the BookCopy model
    saved information of BookCopy. as a foreign key of book.

    Field:
    book     -- the book
    location -- the location where is the bookcopy
    """

    book = models.ForeignKey(Book)
    location = models.CharField(max_length=100)

    def get_status(self):
        """
        Do get the book status, return a dict.

        dict:
        text               : one of ['borrowing', 'arranging',
                                'disappear', 'on shelf']
        expire             : the expire time of the book
        reborrow_count  : reborrowing time of the book
        queue              : the number of the persion who has queued
        outdated           : whether the book is expired

        the key "expire","reborrowing_count","queue","outdated" is visible
            only when text is "borrowing"
        """
        re = {}
        all_borrowing = self.borrowing_set.filter(is_active=True)
        if all_borrowing.filter(status__in=[0, 1, 2]).exists():
            borr = all_borrowing.get(status__in=[0, 1, 2])
            k = borr.myuser.get_perm('borrowing_coefficient') * \
                borr.book_copy.book.duartion
            re = {'text': 'borrowing'}
            re['expire'] = borr.datetime.date() + datetime.timedelta(days=k)
            re['reborrow_count'] = borr.status
            re['queue'] = all_borrowing.filter(status=4).count()
            re['outdated'] = (timezone.now().date() > re['expire'])
        elif all_borrowing.filter(status=3).exists():
            re = {
                'text': 'arranging',
                'queue': all_borrowing.filter(status=4).count(),
                }
        elif all_borrowing.filter(status=5).exists():
            re = {'text': 'disappear'}
        elif all_borrowing.filter(status=6).exists():
            re = {'text': 'dead'}
        else:
            re = {'text': 'on shelf'}
        return re

    def get_expire(self):
        """get the time of expired"""
        s = self.get_status()
        if 'expire' not in s:
            return None
        else:
            return s['expire']

    def set_dead(self, myuser):
        """the copy is disappeared."""
        text = self.get_status()['text']
        assert text in {"on shelf", "arranging"}, "Copy not here."
        if text == "arranging":
            Borrowing.readify(self)
        Borrowing.objects.create(
            status=6,
            book_copy=self,
            myuser=myuser,
            )

    def __unicode__(self):
        """only for debug"""
        return str(self.id) + ": " + self.book.simple_name()


class MyUser(models.Model):

    """the myuser model.
    extend Django.User model, as a one-to-one relationship with Django.User.
    add group and permission.

    Field:
    user            -- django user
    name            -- the user's name, can be Chinese
    grouplist       -- groups that the user can be
    permission_list -- Boolearn, perssions that the user may have
                        'can_manage' includes
                        ('can_midify_book', 'can_change_perm',
                        'can_generate_tempuser', 'can_manage_blacklist',
                        'can_delete_user')
    permission_num_list -- Int, perssions that the user may have
    permission_num  -- the permissions of different group
    admin_type      -- the type of admin,
                        can only be user, book manager or user manager
    """

    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    group_list = ['NormalUser', 'AdvancedUser', 'Blacklist', 'Admin']  # guest
    permission_list = ['can_search', 'can_comment', 'can_manage']
    permission_num_list = [
        'borrowing_num', 'borrowing_coefficient', 'queue_book_num'
        ]

    def _permission_num_generate(*args):
        """generate permission number list"""
        permission_num_list = [
            'borrowing_num', 'borrowing_coefficient', 'queue_book_num'
            ]  # TODO: Remove this dumplicated definition!
        return dict(zip(permission_num_list, args))

    permission_num = {
        'NormalUser': _permission_num_generate(10, 1, 1),
        'AdvancedUser': _permission_num_generate(20, 2, 3),
        'Blacklist': _permission_num_generate(0, 0, 0),
        'Admin': _permission_num_generate(0, 0, 0),
        }
    species_admin = (
        (0, 'user'),
        (1, 'book manager'),
        (2, 'user manager'),
        )

    admin_type = models.IntegerField(choices=species_admin, default=0)
    species_pending = (
        (0, 'Normal'),
        (1, 'register'),
        (2, 'upward'),
    )
    pending = models.IntegerField(choices=species_pending, default=1)

    @transaction.atomic
    def reg_pass(self):
        """pass the register"""
        assert self.pending == 1, "User is not pending."
        self.pending = 0
        self.save()
        self.set_group("NormalUser")

    @transaction.atomic
    def upward(self):
        """upward the permission."""
        assert self.pending == 2, "No upward request."
        self.pending = 0
        self.save()
        group = self.get_group_name()
        if group == "Blacklist":
            self.set_group("NormalUser")
        elif group == "NormalUser":
            self.set_group('AdvancedUser')
        else:
            assert 0, "User can't be upward."

    @transaction.atomic
    def downward(self):
        """downward the permission"""
        group = self.get_group_name()
        if group == "AdvancedUser":
            self.set_group("NormalUser")
        elif group == "NormalUser":
            self.set_group("Blacklist")
        else:
            assert 0, "User can't be downward."

    def upward_request(self):
        """request to upward permission"""
        assert self.pending == 0, "You can't be upward."
        group = self.get_group_name()
        assert group in ["NormalUser", "Blacklist"], "You can't be upward."
        self.pending = 2
        self.save()

    def get_admin_type(self):
        """Do get admin type, return string"""
        if self.get_group_name() != "Admin":
            return 'user'
        return self.get_admin_type_display()

    @transaction.atomic
    def register(self, username, password, email, name):
        """
        user register,
        Usage():
            >>> myuser = MyUser()
            >>> myuser.register(username, password, email, name, group)
        """
        group = 'Blacklist'
        u = User.objects.create_user(username, email, password)
        self.user = u
        self.name = name
        self.set_group(group)
        self.save()

    @transaction.atomic
    def update_user(self, email, pass_old=None, pass_new=None):
        """update user information"""
        self.user.email = email
        if pass_old is not None:
            assert self.user.check_password(pass_old), "Wrong password."
            assert pass_new is not None, "Parameter doesn't not match."
            self.user.set_password(pass_new)
        self.user.save()

    def set_group(self, group):
        """set user group"""
        g = Group.objects.get(name=group)
        self.user.groups = [g]
        self.user.save()

    def get_group_name(self):
        """get my group name"""
        return self.user.groups.all()[0].name

    def has_perm(self, perm):
        """return whether has the permission"""
        return self.user.has_perm('rt.'+perm)

    def get_perm(self, perm):
        """return the permission number"""
        return (self.permission_num[self.get_group_name()])[perm]

    def has_borrowing_num(self):
        """return the number of book which you have borrowed."""
        return Borrowing.objects.filter(
            myuser=self, status__in=[0, 1, 2], is_active=True
            ).count()

    def remain_borrowing_num(self):
        """the number of the book you can borrow now."""
        return self.get_perm('borrowing_num')-self.has_borrowing_num()

    def has_queue_num(self):
        """return the number of book wich you have queued."""
        return Borrowing.objects.filter(
            myuser=self, status=4, is_active=True
            ).count()

    def get_all_borrowing(self):
        """
        get all the book that the user borrowed now.
        sort by expired date.
        """
        bo = Borrowing.objects.filter(
            myuser=self, status__in=[0, 1, 2], is_active=True
            )
        re = [borr.book_copy for borr in bo]
        re.sort(cmp=lambda x, y: (x.get_expire()-y.get_expire()).days)
        return re

    def get_all_queue(self):
        """get all the book that the user queued"""
        bo = Borrowing.objects.filter(
            myuser=self, status=4, is_active=True
            ).order_by('datetime')
        re = [borr.book_copy for borr in bo]
        return re

    def get_all_borrowed(self):
        """get all the book that the user had been borrowed"""
        bo = Borrowing.objects.filter(
            myuser=self, status=0, is_active=False
            ).order_by('datetime')
        re = [
            borr.book_copy for borr in bo if not Borrowing.objects.filter(
                myuser=self, status__in=[1, 2], is_active=True,
                book_copy=borr.book_copy
                ).exists()
            ]
        return re

    @staticmethod
    def get_admin_email():
        ad = Group.objects.get(name='Admin')
        mu = MyUser.objects.filter(
            user__groups=ad,
            admin_type__in=[1, 2]
            ).values('user__email').distinct()
        return [x['user__email'] for x in mu]

    @transaction.atomic
    def reset_password(self):
        p = self.user.password[34:42]
        self.user.set_password(p)
        self.user.save()
        send_mail(
            u'[ReadTogether] Passward Reset',
            dedent(u'''\
            Dear reader {},

            Your passward has been reset successfully.
            Please change it after you login in.

            New Passward: {}

            Sent from ReadTogether.
            ''').format(self.name, p),
            'ReadTogether NoReply <rt_noreply@int01.com>',
            [self.user.email],
            fail_silently=False,
            )

    @staticmethod
    def search(s):
        """search for string in name, nameuser, email, userid"""
        re1 = MyUser.objects.filter(name__contains=s)
        re2 = MyUser.objects.filter(user__username__contains=s)
        re3 = MyUser.objects.filter(user__email__contains=s)
        re4 = MyUser.objects.filter(id__contains=s)
        return (re1 | re2 | re3 | re4).exclude(admin_type__in=[1, 2])

    def __unicode__(self):
        """only for debug"""
        return self.name


class Borrowing(models.Model):

    """the borrowing model
    saves the user borrowing information

    Field:
    status      -- the status of book, the choice is in status_choice
    datetime    -- the time when the borrowing is added
    book_copy   -- the bookcopy which is related to borrowing
    myuser      -- the user who borrows the book
    is_active   -- lazy delete, whether the item is active
    """

    status_choice = (
        (0, 'borrowing'),
        (1, 'reborrowing 1'),
        (2, 'reborrowing 2'),
        (3, 'arranging'),
        (4, 'queue'),
        (5, 'disappear'),
        (6, 'dead'),
        )

    status = models.IntegerField(choices=status_choice)
    datetime = models.DateTimeField(auto_now_add=True)
    book_copy = models.ForeignKey(BookCopy)
    myuser = models.ForeignKey(MyUser)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def borrow(myuser, book_copy):
        """
        User myuser borrow a book_copy.
        the book must on shelf, and the user must has permission that borrows
        """
        if (book_copy.get_status()['text'] != 'on shelf'):
            raise PermException("the book is not on shelf")
        elif (myuser.has_borrowing_num() >= myuser.get_perm('borrowing_num')):
            raise PermException("you can't borrow so many book~")
        else:
            Borrowing.objects.create(
                status=0,
                book_copy=book_copy,
                myuser=myuser,
                )

    @staticmethod
    def reborrow(myuser, book_copy):
        """
        User myuser reborrow the book again.
        the book must be borrowed,
        no one queues the book,
        you can't reborrow again.
        """
        if (not Borrowing.objects.filter(
                myuser=myuser, book_copy=book_copy, is_active=True,
                status__in=[0, 1, 2]
                ).exists()):
            raise PermException("you don't borrow this book!")
        elif (book_copy.get_status()['queue'] > 0):
            raise PermException("there is someone queuing, you can't reborrow")
        elif (Borrowing.objects.get(
                is_active=True, myuser=myuser, book_copy=book_copy
                ).status == 2):
            raise PermException("you have reborrowed twice!")
        b = Borrowing.objects.get(
            is_active=True, myuser=myuser, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        Borrowing.objects.create(
            status=b.status+1,
            book_copy=book_copy,
            myuser=myuser,
            )

    @staticmethod
    @transaction.atomic
    def return_book(book_copy):
        """
        User myuser return the book
        the book must be borrowed by someone.
        if someone queues the book, send a email to him.
        """
        if (not Borrowing.objects.filter(
                book_copy=book_copy, is_active=True,
                status__in=[0, 1, 2]
                ).exists()):
            raise PermException("no one borrows this book!")
        b = Borrowing.objects.get(
            is_active=True, status__in=[0, 1, 2], book_copy=book_copy
            )
        myuser = b.myuser
        b.is_active = False
        b.save()
        Borrowing.objects.create(
            status=3,
            book_copy=book_copy,
            myuser=myuser,
            )
        queue_log_list = Borrowing.objects.filter(
            is_active=True, status=4, book_copy=book_copy
            ).order_by('datetime')
        if queue_log_list:
            myuser = queue_log_list[0].myuser
            book_title = book_copy.book.simple_name()
            send_mail(
                u'[ReadTogether] Book Ready: {}'.format(book_title),
                dedent(u'''\
                Dear reader {},

                The book you queued is ready now. Come and get it.

                Title: {}
                Copy ID: {}

                Sent from ReadTogether.
                ''').format(myuser.name, book_title, book_copy.id),
                'ReadTogether NoReply <rt_noreply@int01.com>',
                [myuser.user.email],
                fail_silently=False,
                )

    @staticmethod
    @transaction.atomic
    def queue_next(myuser, book_copy):
        """
        the admin gives the returned book to the one who queue first.
        the book must be arraging,
        someone queues the book,
        the user must be the first one queues the book.
        """
        if (not Borrowing.objects.filter(
                is_active=True, status=3, book_copy=book_copy
                ).exists()):
            raise PermException("the book is not arranging")
        elif (not Borrowing.objects.filter(
                is_active=True, status=4, book_copy=book_copy
                ).exists()):
            raise PermException("no one queue")
        u = Borrowing.objects.filter(
            is_active=True, status=4, book_copy=book_copy
            ).order_by('datetime')[0]
        if u.myuser.id != myuser.id:
            raise PermException("you are not the first one who have queued")
        u.is_active = False
        u.save()
        b = Borrowing.objects.get(
            is_active=True, status=3, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        Borrowing.objects.create(
            status=0,
            book_copy=book_copy,
            myuser=u.myuser,
            )

    @staticmethod
    def readify(book_copy):
        """
        the admin moves the returned book to shelf.
        the book must be arraging.
        """
        if (not Borrowing.objects.filter(
                is_active=True, status=3, book_copy=book_copy
                ).exists()):
            raise PermException("the book is not arranging")
        b = Borrowing.objects.get(
            is_active=True, status=3, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        Borrowing.objects.filter(
            is_active=True, status=4, book_copy=book_copy
            ).update(is_active=False)

    @staticmethod
    def queue(myuser, book_copy):
        """
        queue  a book.
        the book must be borrowed, be not you,
        you must not queue the book,
        you must has perssion that queue the book.
        """
        if (Borrowing.objects.filter(
                myuser=myuser, book_copy=book_copy, is_active=True, status=0
                ).exists()):
            raise PermException("you have been borrowing this book!")
        elif (Borrowing.objects.filter(
                myuser=myuser, book_copy=book_copy, is_active=True, status=4
                ).exists()):
            raise PermException("you have been queuing this book!")
        elif (myuser.get_perm("queue_book_num") <= myuser.has_queue_num()):
            raise PermException("you can't queue so many books.")
        if (
            Borrowing.objects.filter(
                is_active=True, status__in=[0, 1, 2], book_copy=book_copy
                ).exists()):
            Borrowing.objects.create(
                status=4,
                book_copy=book_copy,
                myuser=myuser,
                )

    @staticmethod
    def queue_del(myuser, book_copy):
        """delete the queue"""
        bo = Borrowing.objects.filter(
            is_active=True, myuser=myuser, book_copy=book_copy, status=4
            )
        assert bo.exists(), "You don't queue this copy."
        bo.update(is_active=False)

    @staticmethod
    def disappear(book_copy):
        """
        the book which myuser borrowed has disappeared.
        the book must be borrowed.
        """
        if (not Borrowing.objects.filter(
                book_copy=book_copy, is_active=True,
                status__in=[0, 1, 2]
                ).exists()):
            raise PermException("no one borrows this book!")
        b = Borrowing.objects.get(
            is_active=True, status__in=[0, 1, 2], book_copy=book_copy
            )
        myuser = b.myuser
        bs = Borrowing.objects.filter(
            is_active=True, book_copy=book_copy
            )
        bs.update(is_active=False)
        Borrowing.objects.create(
            status=5,
            book_copy=book_copy,
            myuser=myuser,
            )

    @staticmethod
    def notify():
        """
        the function will be called every day.
        if the book will expire tomorrow,
        send a mail to him.
        if the book expired over 5 days,
        set the user to Blacklist.
        """
        bs = Borrowing.objects.filter(
            is_active=True, status__in=[0, 1, 2]
            )
        for b in bs:
            date = b.book_copy.get_expire()
            if timezone.now().date() == date+datetime.timedelta(days=1):
                book_title = b.book_copy.book.simple_name()
                send_mail(
                    u'[ReadTogether] Time Out: {}'.format(book_title),
                    dedent(u'''\
                    Dear reader {},

                    The book you borrowed will expire tomorrow.
                    Come and return it.

                    Title: {}
                    Copy ID: {}

                    Sent from ReadTogether.
                    ''').format(b.myuser.name, book_title, b.book_copy.id),
                    'ReadTogether NoReply <rt_noreply@int01.com>',
                    [b.myuser.user.email],
                    fail_silently=False,
                    )
            elif timezone.now().date() >= date+datetime.timedelta(days=5):
                b.myuser.set_group('Blacklist')

    def __unicode__(self):
        """only for debug"""
        return self.myuser.name + " " + str(self.book_copy.id) + ":" + \
            self.book_copy.book.simple_name() + \
            " " + self.get_status_display()


class Info(models.Model):

    """the model info
    saved the info in home page.

    Field:
    title       -- the title of the info
    content     -- the content of the info
    date        -- the time when the info is published.
    species     -- the species of the info
    """

    species_choice = (
        (0, 'news'),
        (1, 'guide'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=10000)
    date = models.DateTimeField(auto_now=True)
    species = models.IntegerField(choices=species_choice, default=0)

    class Meta:
        """auto order by date"""
        ordering = ['-date']

    @staticmethod
    def get_all(sp=None):
        """get all info with species sp."""
        if sp is None:
            return Info.objects.all()
        str2id = {sp_name: sp_id for sp_id, sp_name in Info.species_choice}
        return Info.objects.filter(species=str2id[sp])

    def local_time(self):
        """get local time of publish the info"""
        return timezone.localtime(self.date)

    def __unicode__(self):
        """only for debug"""
        return self.title+" "+str(self.date)


class Comment(models.Model):
    """the comment of book"""

    species_rate = (
        (1, 'perfect'),
        (2, 'good'),
        (3, 'normal'),
        (4, 'bad'),
        (5, 'terrible'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    datetime = models.DateTimeField(auto_now=True)
    rate = models.IntegerField(choices=species_rate, default=3)
    spoiler = models.BooleanField(default=False)
    myuser = models.ForeignKey(MyUser)
    book = models.ForeignKey(Book)

    def _update(self):
        """update the rate of the book after comment"""
        self.book.rate = (self.book.rate*self.book.rate_num+self.rate) / \
            (self.book.rate_num+1)
        self.book.rate_num = self.book.rate_num+1
        self.book.save()

    @staticmethod
    def add(myuser, book, title, content, rate=3, spoiler=False):
        """add a new comment"""
        c = Comment.objects.create(
            myuser=myuser,
            book=book,
            title=title,
            content=content,
            rate=rate,
            spoiler=spoiler,
            )
        c._update()

    @transaction.atomic
    def remove(self):
        """reomve comment"""
        if self.book.rate_num == 1:
            self.book.rate = 0.0
        else:
            self.book.rate = (self.book.rate*self.book.rate_num-self.rate) / \
                (self.book.rate_num-1)
        self.book.rate_num = self.book.rate_num-1
        self.book.save()
        self.delete()

    def __unicode__(self):
        return self.myuser.name+" "+self.book.simple_name()+" " + \
            self.title+" : "+self.content+" "+str(self.rate)


class Rank(models.Model):
    """
    save range every month.

    Field:
    RANK_NUM        -- the max number of rank
    version         -- the version of the rank
    book            -- the book in rank
    value           -- the value which the sort based on
    sort_method     -- the method that the sort based on
    rank            -- the rank of the book
    """

    RANK_NUM = 10
    version = models.IntegerField()
    book = models.ForeignKey(Book)
    value = models.FloatField()
    species_sort_method = (
        (0, 'borrowing time'),
        (1, 'comment number'),
        (2, 'rate')
    )
    sort_method = models.IntegerField(choices=species_sort_method)
    rank = models.IntegerField()

    @staticmethod
    def get_maxversion():
        """get the newest version, if None it's 0."""
        agg = Rank.objects.all().aggregate(models.Max('version'))
        n = agg['version__max']
        if agg['version__max'] is None:
            n = 0
        return n

    @staticmethod
    def _cal_value(books, species):
        """cal the value of all books by sepcies."""
        re = []
        for book in books:
            if species == 0:
                n = 0
                for bookcopy in book.bookcopy_set.all():
                    n += Borrowing.objects.filter(
                        book_copy=bookcopy, status__in=[0, 1, 2]
                        ).count()
                re.append(n)
            elif species == 1:
                re.append(book.rate_num)
            elif species == 2:
                re.append(book.rate)
        return re

    @staticmethod
    @transaction.atomic
    def _top10(species, version):
        """get top 10 by species_sort_method"""
        books = list(Book.objects.all())
        values = Rank._cal_value(books, species)
        l = zip(books, values)
        l.sort(key=lambda a: a[1], reverse=True)
        l = l[:Rank.RANK_NUM]
        for index, i in enumerate(l):
            Rank.objects.create(
                version=version,
                book=i[0],
                value=i[1],
                sort_method=species,
                rank=index,
                )

    @staticmethod
    def update():
        """update the rank every week!"""
        version = Rank.get_maxversion()+1
        for i in range(len(Rank.species_sort_method)):
            Rank._top10(i, version)

    @staticmethod
    def get_top(species=2, v=0):
        """get the rank by species and version."""
        if v == 0:
            v = Rank.get_maxversion()
        return Rank.objects.filter(
            version=v, sort_method=species
            ).order_by('rank')

    def __unicode__(self):
        """only for debug"""
        return self.book.simple_name()+" "+str(self.value)+" " + \
            str(self.sort_method)+" "+str(self.rank)
