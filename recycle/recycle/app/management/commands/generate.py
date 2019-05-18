from django.core.management.base import BaseCommand, CommandError
from app.models import *
import json
from random import randint, choice

DEFAULT_AD=50000
BATCH_SIZE = 50
DEFAULT = 100000

ad_1=[[2], [6], [6], [6], [0], [2], [0], [1], [0], [2], [2], [6], [1], [2], [4], [2], [1], [2], [3], [2], [4], [0], [1], [1], [0], [1], [1], [5], [3], [1], [2], [0], [6], [0], [0], [6], [2], [6], [6], [2], [0], [1], [5], [1], [3], [2], [2], [0], [0], [2], [6], [0], [2], [2], [6], [1], [1], [0], [0], [6], [1], [3], [2], [2], [0], [4], [1], [4], [2], [6], [0], [6], [6], [2], [1], [6], [2], [6], [1], [2], [1], [0], [0], [6], [2], [3], [1], [1], [1], [2], [0], [1], [0], [3], [0], [0], [0], [1], [1], [1], [6], [4], [2], [6], [4], [6], [6], [1], [2], [1], [6], [2], [6], [1], [0], [0], [6], [3], [1], [6], [6], [2], [6], [0], [6], [6], [0], [2], [1], [0], [0], [0], [2], [6], [1], [2], [2], [2], [2], [3], [2], [6], [1], [6], [1], [6], [1], [1], [2], [6], [6], [0], [2], [1], [0], [6], [6], [6], [6], [1], [1], [0], [3], [6], [6], [1], [0], [2], [0], [0], [6], [3], [1], [1], [0], [0], [1], [0], [2], [2], [6], [1], [0], [2], [2], [1], [1], [6], [6], [2], [1], [2], [0], [3], [6], [6], [2], [0], [6], [3], [2], [0], [0], [6], [4], [2], [4], [2], [1], [6], [4], [2], [2], [6], [1], [6], [6], [2], [1], [2], [1], [2], [2], [1], [6], [6], [0], [2], [1], [2], [3], [2], [2], [0], [6], [6], [2], [6], [2], [0], [1], [6], [3], [0], [0], [1], [0], [6], [2], [0], [6], [0], [6], [0], [0], [1], [0], [0], [0], [4], [6], [1], [2], [2], [0], [1], [6], [2], [2], [2], [0], [2], [2], [2], [6], [6], [2], [6], [1], [2], [6], [1], [6], [0], [2], [1], [0], [0], [1], [6], [2], [6], [3], [1], [1], [6], [6], [2], [3], [2], [0], [1], [2], [1], [0], [6], [2], [0], [4], [6], [6], [1], [0], [1], [0], [4], [6], [6], [6], [2], [2], [0], [6], [1], [0], [6], [6], [0], [6], [2], [1], [2], [1], [1], [6], [6], [6], [2], [2], [2], [2], [0], [0], [6], [0], [1], [6], [0], [0], [1], [2], [6], [0], [6], [6], [1], [1], [6], [1], [4], [2], [1], [6], [6], [6], [1], [3], [1], [1], [1], [1], [3], [2], [2], [1], [2], [0], [1], [0], [1], [6], [6], [0], [6], [1], [6], [4], [2], [1], [1], [6], [6], [2], [2], [6], [1], [1], [1], [2], [1], [6], [0], [0], [6], [0], [6], [0], [2], [0], [0], [1], [1], [1], [2], [0], [2], [2], [2], [6], [6], [2], [0], [6], [6], [4], [2], [6], [6], [4], [0], [0], [2], [2], [2], [0], [2], [2], [2], [1], [6], [1], [1], [1], [6], [1], [1], [6], [1], [1], [1], [6], [6], [1], [4], [1], [1], [1], [6], [1], [2], [0], [0, 1], [0], [6], [6], [6], [0], [2], [0], [0], [0], [3], [2], [1], [1], [0], [6], [4], [6], [6], [2], [1], [0], [0], [6], [0], [2], [1], [1], [2], [1], [0], [0], [0], [0], [3], [3], [2], [1], [1], [0], [1], [0], [6], [0], [0], [2], [1], [6], [6], [0], [6], [6], [1], [0], [0], [6], [0], [1], [1], [1], [6], [1], [0], [6], [6], [0], [3], [1], [6], [1], [0], [6], [6], [4], [4], [0], [1], [2], [1], [2], [1], [1], [1], [6], [2], [1], [4], [0], [6], [4], [6], [2], [4], [2], [4], [1], [1], [6], [1], [0], [1], [1, 6], [6], [0], [4], [1], [3], [0], [2], [0], [2], [3], [1], [1], [2], [0], [1], [0], [6], [0], [4], [1], [1], [0], [2], [1], [0], [1], [1], [2], [6], [1], [2], [2], [2], [1], [1], [0], [6], [6], [3], [1], [3], [2], [6], [6], [2], [4], [0], [6], [6], [4], [1], [0], [0], [6], [2], [6], [6], [4], [3], [1], [2], [4], [6], [0], [2], [6], [2], [2], [1], [6], [6], [2], [1], [2], [2], [6], [1], [2], [6], [6], [0], [2], [1], [1], [0], [0], [6], [0], [1], [6], [4], [1], [1], [1], [6], [6], [2], [1], [2], [1], [2], [2], [1], [1], [1], [2], [2], [6], [3], [2], [0], [0], [2], [1], [4], [1], [6], [6], [0], [2], [2], [2], [6], [6], [0], [1], [1], [1], [1], [2], [2], [2], [4], [1], [1], [1], [1], [1], [1], [1], [1], [6], [1], [2], [1], [0], [2], [1], [0], [4], [1], [0], [1], [1], [1], [1], [1], [4], [6], [1], [2], [1], [6], [1], [6], [2], [6], [0], [6], [1], [1], [1], [2], [1], [1], [2], [1], [1], [1], [6], [1], [1], [2], [6], [1], [1], [1], [0], [6], [1], [0], [6], [2], [1], [6], [1], [2], [1], [0], [6], [1], [6], [4], [1], [0], [0], [6], [1], [1], [2], [3], [1], [0], [1], [6], [1], [6], [1], [1], [6], [3], [6], [0], [6], [5], [0], [1], [1], [6], [1], [6], [1], [0], [2], [1], [3], [6], [4], [1], [0], [6], [0], [1], [1], [1], [1], [0], [4], [3], [6], [0], [6], [1], [6], [1], [1], [2], [1], [6], [1], [6], [1], [6], [4], [6], [2], [6], [0], [4], [0], [1], [6], [1], [1], [1], [1], [1], [0], [6], [1], [1], [0], [1], [2], [1], [6], [0], [1], [1], [3], [2], [1], [1], [2], [1], [1], [1], [1], [0], [0], [0], [1], [2], [0], [0], [1], [2], [0], [1], [1], [0], [6], [1], [1], [0], [6], [1], [3], [1], [2], [0], [0], [1], [0], [6], [6], [1], [1], [1], [1], [6], [6], [6], [1], [0], [6], [6], [0], [1], [1], [1], [2], [2], [6], [0], [6], [4], [2], [1], [1], [6], [2], [3], [1], [3], [1], [1], [0], [3], [2], [1], [6], [1], [6], [0], [0], [6], [6], [2], [2], [1], [6], [1], [1], [1], [1], [1], [6], [1], [1], [0], [1], [0], [0], [0], [1], [1], [1], [6], [1], [0], [1]]




class Command(BaseCommand):
    help = 'Generates objects of my models'

    def handle(self, *args, **options):
        adss = []
        count = 0
        with open('/home/lidia/Documents/recycleProj/TukaTuka-ML-Ads/recycle/recycle/app/management/commands/flagma_othody-plenki-pvd.json', 'r', encoding="utf_8") as f:
            for js in f:
                tmp = json.loads(js)
                adss.append(Ad(title=tmp['header'],description =tmp['description'],category1=ad_1[count][0]))
                count+=1
        Ad.objects.bulk_create(adss, batch_size=BATCH_SIZE)
