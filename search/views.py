import json
from django.shortcuts import render
from django.views.generic.base import View
from search.models import EnglishType, ChineseType
from django.http import HttpResponse
from elasticsearch import Elasticsearch

client = Elasticsearch(hosts=["127.0.0.1"])
# Create your views here.
class SearchSuggest(View):
    def get(self,request):
        key_words = request.GET.get('s')
        s_type = request.GET.get("s_type", "watches")

        re_datas = []
        if key_words:
            if s_type == "chrono24":
                s = EnglishType.search()
            else:
                s = ChineseType.search()
            s.suggest('my_suggest',key_words, completion={
                "field": "suggest", "fuzzy":{
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match.source
                re_datas.append(source["title"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")

class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q", "")
        s_type = request.GET.get("s_type", "watches")
        page = request.GET.get("p", "1")
        if s_type == "chrono24":


            try:
                page = int(page)
            except:
                page = 1

            response = client.search(
                index="chrono24",
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["watch_name"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                }
            )
        else:
            page = request.GET.get("p", "1")
            try:
                page = int(page)
            except:
                page = 1

            response = client.search(
                index="xbiao",
                body={
                    "query": {
                        "multi_match": {
                            "query": key_words,
                            "fields": ["watch_name"]
                        }
                    },
                    "from": (page - 1) * 10,
                    "size": 10,
                }
            )

        total_nums = response["hits"]["total"]
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            hit_dict["watch_name"] = hit["_source"]["watch_name"]
            if s_type == "chrono24":
                hit_dict["price"] = "$ "+ hit["_source"]["price"]
            else :
                hit_dict["price"] = "￥ " + str(hit["_source"]["price"])
            hit_dict["country"] = hit["_source"]["country"]
            hit_dict["city"] = hit["_source"]["city"]
            hit_dict["seller"] = hit["_source"]["seller"]
            hit_dict["ship_status"] = hit["_source"]["ship_status"]
            hit_dict["img_url"] = hit["_source"]["img_url"]
            hit_dict["url"] = hit["_source"]["url"]

            hit_list.append(hit_dict)

        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums})