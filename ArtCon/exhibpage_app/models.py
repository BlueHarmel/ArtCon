from django.db import models

# Create your models here.

class Exhibit(models.Model):
    E_name = models.CharField(max_length=200)
    L_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.CharField(max_length=100, null=True)
    fee = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=500, null=True)
    img = models.CharField(max_length=500, null=True)
    summary = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str({'E_name': self.E_name,
                    'L_name': self.L_name,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'time': self.time,
                    'fee': self.fee,
                    'url': self.url,
                    'img': self.img,
                    'summary': self.summary
                    })

class Location(models.Model):
    L_name = models.CharField(max_length=50)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return str({'L_name': self.L_name,
                    'x': self.x,
                    'y': self.y})