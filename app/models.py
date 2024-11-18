from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    schedule_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Keyword(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class ScrapedResult(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    url = models.URLField()
    page_number = models.IntegerField()
    position = models.IntegerField()
    scrape_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.keyword.name} - {self.url}'
