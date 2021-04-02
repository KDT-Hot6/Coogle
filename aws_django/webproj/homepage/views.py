from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from elasticsearch import Elasticsearch  
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json
import re

# Create your views here.


######################################## return html page ##########################################
# def main(request):
#     return render(request, 'main.html', {})

# 식당 리스트를 보여주는 페이지
def getResListpage(request):
    print(request.GET)
    search = request.GET.get('q', '')
    if 'search_key' in request.GET:
        search = request.GET.get('search_key')
    
    info = getInfo(search)
    res_list = groupingBoard((jsonPaser(info)))
    content = {'res_list': res_list,}

    return render(request, 'res_list_page.html', content)

# 메인 검색 페이지
def getSearchPage(request):
    return render(request, 'coogle_search.html')




#######################################################################
########################## elastic search #############################
#######################################################################

model_path = '/home/ubuntu/hot6/bh/KoSentenceBERT_SKTBERT/output/training_stsbenchmark_skt_kobert_model_-2021-03-28_05-25-43_best'
embedder = SentenceTransformer(model_path)

client = Elasticsearch()
res_size = 18  #120

def getInfo(search):
    query = search
    vectors = embedder.encode(query, convert_to_tensor=True)
    query_vector = [vector.tolist() for vector in vectors]

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['comment_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index='revd',
        body={
            "size": res_size,
            "query": script_query
            # "_source": {"includes": ["res_id", "res_name", "comment", "adress", "keywords"]}
        }
    )

    # data_list = response['hits']

    return response



################################## funcs to preprocess restaurant infomation #######################


###### elastic search에서 받아온 json 정보를 html에서 보여줄 수 있도록 파싱
def jsonPaser(info):
    # res_info_key = info['hits']['hits'][0]['_source'].keys()
    res_list = {}
    number = 0
    for i in range(len(info['hits']['hits'])):
        # 'res_id', 'res_name', 'adress', 'comment', 'keywords'
        number += 1
        res_comments = []
        res_number = number
        res_id = info['hits']['hits'][i]['_source']['res_id']
        res_name = info['hits']['hits'][i]['_source']['res_name']
        res_addr = info['hits']['hits'][i]['_source']['adress']
        res_comment = info['hits']['hits'][i]['_source']['comment']
        res_keywords = info['hits']['hits'][i]['_source']['keywords']

        #식당 주소 전처리 ('\n' -> '<br>')
        res_addr = preprocessAddr(res_addr)
        
        # 리뷰 데이터가 1개만 있어서 type이 string일 때, type을 리스트로 만들어준다.
        # (만약, 같은 식당이 나오면 리스트들끼리 병합하기 위해)
        if type(res_comment) != type([]):
            res_comments.append(res_comment)
        else:
            res_comments = res_comment


        # res_id를 기준으로 같은 식당이 나오는지 검사
        if res_list.get(res_id) == None:
            res_comments.sort(reverse=True)
            res_info = {'res_name':res_name, 'res_addr':res_addr, 
                        'res_comment':res_comments, 'res_keywords':res_keywords,
                        'res_number': res_number,
            }
            res_list[res_id] = res_info
        else:
            comments = res_list[res_id]['res_comment'] + res_comments
            comments.sort(reverse=True)
            res_list[res_id]['res_comment'] = comments
            number -= 1

    
    return res_list


###### 식당들을 6개씩 그룹핑
def groupingBoard(info):
    res_list = []
    group = []
    count = 0

    for v in info.values():
        if count == 0:
            group = []
        group.append(v)
        count += 1
        if count == 6:
            res_list.append(group)
            count = 0

    return  res_list


def groupingPage(info):
    res_list = []
    group = []
    count = 0

    for res_board in info:
        if count == 0:
            group = []
        group.append(res_board)
        count += 1
        if count == 2:
            res_list.append(group)
            count = 0

    return res_list


def preprocessAddr(addr):
    addr2 = re.sub('\n', '<br>&nbsp;&nbsp;&nbsp;', addr)

    return addr2