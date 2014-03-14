from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from custom_user_auth.models import MyUser,Article,Category
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput)

    class Meta:
        model = MyUser
        fields = ('email','first_name', 'last_name', 'uid')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'uid', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name','last_name','email', 'uid', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Credential', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('uid','first_name','last_name','profile_pic_url','short_desc','twitter_link','facebook_link','google_link','cover_photo','country','loginwith','gender')}),
        ('Permissions', {'fields': ('is_admin','is_deleted',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name', 'uid', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class ArticleAdd(forms.ModelForm):
    article_content = forms.CharField(label='Article content',widget=forms.TextInput)
    article_date = forms.DateTimeField(label='Article Date',widget=forms.SplitDateTimeField)
    total_view = forms.IntegerField(label='Total Views')

     class Meta:
        model = Article
        fields = ('article_user_id','article_content','article_date','time_to_read','total_views','article_category')

    def save(self, commit=True):
        # Save the provided password in hashed format
        article = super(ArticleAdd, self).save()
        return article


# Now register the new UserAdmin...
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Article)
admin.site.register(Category)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)