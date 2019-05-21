from django.db import models

# Create your models here.
class Publisher(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    city=models.CharField(max_length=60)
    state_province=models.CharField(max_length=30)
    country=models.CharField(max_length=50)
    website=models.URLField()

    def __str__(self):
        return self.name

    '''
    指定排序的关键字
    '''
    class Meta:
        ordering=['name']

class Author(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=40)
    email=models.EmailField(blank=True,verbose_name='e-mail')#verbose_name是自定义的在网页显示的字段名称

    def __str__(self):
        return u'%s %s' %(self.first_name,self.last_name)

class Book(models.Model):
    title=models.CharField(max_length=100)
    authors=models.ManyToManyField(Author)
    publisher=models.ForeignKey(Publisher)
    publication_date=models.DateField(blank=True,null=True)

    def __str__(self):
        return self.title
