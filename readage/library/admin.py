from django.contrib import admin
from django.contrib.auth.models import User

from library.models import Book, BookCopy, MyUser, Borrowing, Info, Comment, Rank


class BookCopyInline(admin.StackedInline):
    model = BookCopy
    extra = 3


class BookAdmin(admin.ModelAdmin):
    inlines = [BookCopyInline]


class MyUserInline(admin.StackedInline):
    model = MyUser


class UserAdmin(admin.ModelAdmin):
    inlines = [MyUserInline]


admin.site.register(Book, BookAdmin)
# admin.site.register(BookCopy)
# admin.site.register(MyUser)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Borrowing)
admin.site.register(Info)
admin.site.register(Comment)
admin.site.register(Rank)
