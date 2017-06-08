from django.db import models

# Create your models here.

from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["127.0.0.1"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


class EnglishType(DocType):
    #chrono24 watch attr
    url = Keyword()
    url_object_id = Keyword()
    watch_name = Text(analyzer="standard")
    price = Text(analyzer="standard")
    img_url = Keyword()
    country = Text(analyzer="standard")
    city = Text(analyzer="standard")
    seller = Text(analyzer="standard")
    ship_status = Text(analyzer="standard")
    suggest = Completion()

    class Meta:
        index = "chrono24"
        doc_type = "watches"


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class ChineseType(DocType):
    # xbiao watch attr
    url = Keyword()
    url_object_id = Keyword()
    watch_name = Text(analyzer="ik_max_word")
    price = Text()
    img_url = Keyword()
    country = Text(analyzer="ik_max_word")
    city = Text(analyzer="ik_max_word")
    seller = Text(analyzer="ik_max_word")
    ship_status = Text()
    suggest = Completion(analyzer=ik_analyzer)

    class Meta:
        index = "xbiao"
        doc_type = "watches"