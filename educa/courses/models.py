from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

###
#   owner: 강의를 가르치는 사람
#   subject: 강의가 소속된 주제
#   title: 강의 이름
#   slug: 강의 URL
#   overview: 강의 개요
#   created: 강의 생성일, 자동으로 생성됨 (auto_now_add)
###
class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created')
    subject = models.ForeignKey(Subject,related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

###
#   course: 강의는 여러개의 모듈로 나뉘어 지는데, 모듈마다 소속된 강의를 외부키로 가지게 된다.
#   title: 모듈 이름
#   description: 모듈 개요
###
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order,self.title)

###
#   content_type:
#   object_id: 관련 객체의 primary key
#   item: 앞의 2개를 합쳐 놓은 키
###
class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents')
    #content_type = models.ForeignKey(ContentType)
    content_type = models.ForeignKey(ContentType,
                    limit_choices_to={
                    'model__in': ('text','video','image','file')
                    })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()



