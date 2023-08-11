from django.db import models

# Create your models here.

# class Exhibit(models.Model):
#     E_name = models.CharField(max_length=200)
#     L_name = models.CharField(max_length=50)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     time = models.CharField(max_length=100, null=True)
#     fee = models.CharField(max_length=50, null=True)
#     url = models.CharField(max_length=500, null=True)
#     img = models.CharField(max_length=500, null=True)
#     summary = models.CharField(max_length=1000, null=True)

#     def __str__(self):
#         return str({'E_name': self.E_name,
#                     'L_name': self.L_name,
#                     'start_date': self.start_date,
#                     'end_date': self.end_date,
#                     'time': self.time,
#                     'fee': self.fee,
#                     'url': self.url,
#                     'img': self.img,
#                     'summary': self.summary
#                     })
    
# class Location(models.Model):
#     L_name = models.CharField(max_length=50)
#     x = models.FloatField()
#     y = models.FloatField()

#     def __str__(self):
#         return str({'L_name': self.L_name,
#                     'x': self.x,
#                     'y': self.y})
    
class Performance(models.Model):
    P_id = models.CharField(max_length=20)
    P_name = models.CharField(max_length=100)
    P_startdate = models.DateField()
    P_enddate = models.DateField()
    L_name = models.CharField(max_length=100)
    P_Img = models.CharField(max_length=500)
    P_genre = models.CharField(max_length=20)
    P_state = models.CharField(max_length=10)
    P_summary = models.CharField(max_length=5000)

    def __str__(self):
        return str({'P_id': self.P_id,
                    'P_name': self.P_name,
                    'P_startdate': self.P_startdate,
                    'P_enddate': self.P_enddate,
                    'L_name': self.L_name,
                    'P_Img': self.P_Img,
                    'P_genre': self.P_genre,
                    'P_state': self.P_state,
                    'P_summary': self.P_summary
                    })
    
class Location(models.Model):
    L_name = models.CharField(max_length=100)
    L_id = models.CharField(max_length=20)
    L_telnum = models.CharField(max_length=20)
    L_address = models.CharField(max_length=500)
    L_la = models.FloatField()
    L_lo = models.FloatField()
    L_url = models.CharField(max_length=500)

    def __str__(self):
        return str({'L_name': self.L_name,
                    'L_id': self.L_id,
                    'L_telnum': self.L_telnum,
                    'L_address': self.L_address,
                    'L_la': self.L_la,
                    'L_lo': self.L_lo,
                    'L_url': self.L_url
                    })