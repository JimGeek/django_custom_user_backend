from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, uid, first_name, last_name, password=None, profile_pic_url='', facebook_link='', google_link=''):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        elif not uid:
            raise ValueError('Users must have an UID')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            uid=uid,
            profile_pic_url = profile_pic_url,
            facebook_link = facebook_link,
            google_link = google_link,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, uid, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            uid=uid
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.TextField(max_length=15,verbose_name='first name')
    last_name = models.TextField(max_length=15,verbose_name='last name')
    uid = models.TextField(max_length=15,verbose_name='oauth key')
    profile_pic_url = models.CharField(blank=True,max_length=100,verbose_name='profile pic')
    short_desc = models.CharField(blank=True,max_length=140,verbose_name='short description')
    twitter_link = models.CharField(blank=True,max_length=140,verbose_name='twitter connect')
    facebook_link = models.CharField(blank=True,max_length=140,verbose_name='facebook connect')
    google_link = models.CharField(blank=True,max_length=140,verbose_name='google connect')
    cover_photo = models.CharField(blank=True,max_length=200,verbose_name='cover photo')
    country = models.CharField(blank=True,max_length=50,verbose_name='country')
    is_deleted = models.BooleanField(default=False,verbose_name='account status')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid','first_name','last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.last_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Category(models.Model):
    category_name = models.CharField(max_length=50,blank=True,verbose_name='category name')
    category_image = models.CharField(max_length=140,blank=True,verbose_name='category image')
    category_short_desc = models.CharField(max_length=140,blank=True,verbose_name='category desc')
    is_deleted = models.BooleanField(default=False,verbose_name='category status')

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_user_id = models.ForeignKey(MyUser)
    article_content = models.TextField(verbose_name="article content",blank=True)
    article_date = models.DateTimeField(auto_now_add=True,verbose_name="article creation date")
    last_updated = models.DateTimeField(auto_now=True, verbose_name='article update date')
    time_to_read = models.IntegerField(verbose_name="time to read")
    total_views = models.IntegerField(verbose_name="total views")
    article_category = models.ForeignKey(Category)
    is_deleted = models.BooleanField(default=False,verbose_name='article status')

class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    bookmark_user_id = models.ForeignKey(MyUser)
    article_link = models.ForeignKey(Article)

class UserArticle(models.Model):
    article_connect_user_id = models.ForeignKey(MyUser)
    user_connect_article_id = models.ForeignKey(Article)

class CategoryFollow(models.Model):
    category_follow_user_id = models.ForeignKey(MyUser)
    user_category_id = models.ForeignKey(Category)

class AuthorFollow(models.Model):
    follow_user_id = models.ForeignKey(MyUser,related_name='user_user_connect')
    follow_author_id = models.ForeignKey(MyUser,related_name='author_user_connect')

class CategoryArticle(models.Model):
    category_article_id = models.ForeignKey(Article)
    article_category_id = models.ForeignKey(Category)

class SocialMediaSettings(models.Model):
    social_user_id = models.ForeignKey(MyUser)
    facebook_status = models.BooleanField(default=False)
    google_status = models.BooleanField(default=False)
    twitter_status = models.BooleanField(default=False)
    facebook_link = models.URLField(blank=True,verbose_name='facebook link')
    google_link = models.URLField(blank=True,verbose_name='google link')
    twitter_link = models.URLField(blank=True,verbose_name='twitter link')