from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from elasticsearch import Elasticsearch  
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json
import re

#word embedding
from konlpy.tag import Mecab
from gensim import models
import fasttext
import fasttext.util
from gensim.models import KeyedVectors
from collections import deque
from time import time

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
    
    info = getInfo2(search)
    res_list = makeGroup(jsonPaser2(info[0]))

    # number = 1
    content = {'res_list': res_list, 'word_list': info[1]}
    
    return render(request, 'res_list_page.html', content)

# 메인 검색 페이지
def getSearchPage(request):
    return render(request, 'coogle_search.html')




#######################################################################
########################## elastic search #############################
#######################################################################

# model_path = '/home/ubuntu/hot6/bh/KoSentenceBERT_SKTBERT/output/training_stsbenchmark_skt_kobert_model_-2021-03-28_05-25-43_best'
# embedder = SentenceTransformer(model_path)

# client = Elasticsearch()
# res_size = 18

# def getInfo(search):
#     query = search
#     vectors = embedder.encode(query, convert_to_tensor=True)
#     query_vector = [vector.tolist() for vector in vectors]

#     script_query = {
#         "script_score": {
#             "query": {"match_all": {}},
#             "script": {
#                 "source": "cosineSimilarity(params.query_vector, doc['comment_vector']) + 1.0",
#                 "params": {"query_vector": query_vector}
#             }
#         }
#     }

#     response = client.search(
#         index='revd',
#         body={
#             "size": res_size,
#             "query": script_query
#             # "_source": {"includes": ["res_id", "res_name", "comment", "adress", "keywords"]}
#         }
#     )

#     # data_list = response['hits']

#     return response



################################## funcs to preprocess restaurant infomation #######################


###### elastic search에서 받아온 json 정보를 html에서 보여줄 수 있도록 파싱
# def jsonPaser(info):
#     # res_info_key = info['hits']['hits'][0]['_source'].keys()
#     res_list = {}
#     number = 0
#     for i in range(len(info['hits']['hits'])):
#         # 'res_id', 'res_name', 'adress', 'comment', 'keywords'
#         number += 1
#         res_comments = []
#         res_number = number
#         res_id = info['hits']['hits'][i]['_source']['res_id']
#         res_name = info['hits']['hits'][i]['_source']['res_name']
#         res_addr = info['hits']['hits'][i]['_source']['adress']
#         res_comment = info['hits']['hits'][i]['_source']['comment']
#         res_keywords = info['hits']['hits'][i]['_source']['keywords']

#         #식당 주소 전처리 ('\n' -> '<br>')
#         res_addr = preprocessAddr(res_addr)
        
#         # 리뷰 데이터가 1개만 있어서 type이 string일 때, type을 리스트로 만들어준다.
#         # (만약, 같은 식당이 나오면 리스트들끼리 병합하기 위해)
#         if type(res_comment) != type([]):
#             res_comments.append(res_comment)
#         else:
#             res_comments = res_comment


#         # res_id를 기준으로 같은 식당이 나오는지 검사
#         if res_list.get(res_id) == None:
#             res_comments.sort()
#             res_info = {'res_name':res_name, 'res_addr':res_addr, 
#                         'res_comment':res_comments, 'res_keywords':res_keywords,
#                         'res_number': res_number,
#             }
#             res_list[res_id] = res_info
#         else:
#             comments = res_list[res_id]['res_comment'] + res_comments
#             comments.sort()
#             res_list[res_id]['res_comment'] = comments
#             number -= 1

#     # print(len(res_list))
#     return res_list


###### 식당들을 6개씩 그룹핑
def makeGroup(info):
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



def preprocessAddr(addr):
    addr2 = re.sub('\n', '<br>&nbsp;&nbsp;&nbsp;', addr)

    return addr2



############################################################################################################################################################
#################################################### model2 #################################################################################################
############################################################################################################################################################

tagger = Mecab()
review_only_model = models.fasttext.load_facebook_model("/home/ubuntu/hot6/eunjeon/final_review.bin")

# 검색어 토큰 생성 함수
stop_tags = ['JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC',
             'EP','EF','EC','ETN','ETM','XSN','XSV','XSA',
             'SF','SE','SSO','SSC','SC','SY']
stop_words = ['곳','집','식당','장소','음식점']
def get_search_token(sent):
    spl_tokens = sent.split(' ')
    res = []
    for st in spl_tokens:
        pos_st = tagger.pos(st)
        mor_st = tagger.morphs(st)
        while pos_st and ( pos_st[-1][1] in stop_tags or pos_st[-1][0] in stop_words ):
            pos_st = pos_st[:-1]
            mor_st = mor_st[:-1]
        tmp = ''.join(mor_st)
        if len(tmp) > 1:
            res.append(tmp)
    return res


# ngram? 프라이?
# 검색어 토큰과 벡터 유사도 높은 단어 추출 함수
def get_vector_similar_words(keywords, many):
    result = []
    for keyword in keywords:
        similar_list = review_only_model.wv.most_similar(keyword, topn=300)
        words = deque()
        words.append([keyword, 1.000])
        res = deque()
        for item in similar_list:
            if keyword not in str(item[0]):
                res.append(item)
        while res:
            tmp_data = res.popleft()
            tmp = get_search_token(tmp_data[0])
            if tmp:
                tmp = tmp[0]
                words.append([tmp, tmp_data[1]])
                tmp_res = deque()
                for item in res:
                    if tmp not in str(item[0]) and item[1] > 0.7:
                        tmp_res.append(item)
                res = tmp_res
        words = deque(sorted(words, key=lambda x: len(x[0])))
        tem_words = deque()
        while words:
            tem_word = words.popleft()
            tem_words.append(tem_word)
            if len(tem_word[0])==1: pass
            else:
                for _ in range(len(words)):
                    word = words.popleft()
                    if tem_word[0] not in word[0]:
                        words.append(word)
        words = sorted(tem_words, key=lambda x: -x[1])
        words = [word[0] for word in words]
        result.append(words[: many])  # n개까지 가져가기
    return result
    
def get_vector_similar_words2(keywords):
    result = []
    for keyword in keywords:
        similar_list = review_only_model.wv.most_similar(keyword, topn=300)
        words = [keyword]
        res = []
        for item in similar_list:
            if keyword not in str(item[0]):
                res.append(item)
        while len(words) < 5 and res:
            tmp = get_search_token(res.pop(0)[0])
            if tmp:
                tmp = tmp[0]
                words.append(tmp)
                tmp_res = []
                for item in res:
                    if tmp not in str(item[0]) and item[1] > 0.7:
                        tmp_res.append(item)
                res = tmp_res
        result.append(words)
    return result

def make_query(word_list):
    main_form = {"query":{"bool":{"must":[]}}}
    for words in word_list:
        and_form = {"bool":{"should":[]}}
        for word in words:
            or_form = {"wildcard":{"comment": ""}}
            or_form['wildcard']['comment'] = "*"+word+"*"
            and_form['bool']['should'].append(or_form)
        main_form['query']['bool']['must'].append(and_form)
    return main_form

# model_path = '/home/ubuntu/hot6/bh/KoSentenceBERT_SKTBERT/output/training_stsbenchmark_skt_kobert_model_-2021-03-28_05-25-43_best'
# embedder = SentenceTransformer(model_path)

client = Elasticsearch()
# corpus = '관자의 쫄길함이 살아있다..'
# corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
# print(corpus_embeddings.tolist())


    
def getInfo2(search):
    search_sent = search
    # word_list = get_vector_similar_words(get_search_token(search_sent),5)
    word_list = get_vector_similar_words2(get_search_token(search_sent))
    q = make_query(word_list)
    q['_source'] = {"includes": ["res_id","res_name","adress","comment"]}
    print(q)
    response = client.search(
        index='orires',
        body=q,
    
    )


    h_words = []
    for item in word_list:
        h_words += item

    data = [response, h_words]
    return data



def jsonPaser2(info):
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
        # res_keywords = info['hits']['hits'][i]['_source']['keywords']

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
            res_comments.sort()
            res_info = {'res_name':res_name, 'res_addr':res_addr, 
                        'res_comment':res_comments,
                        'res_number': res_number,
            }
            res_list[res_id] = res_info
        else:
            comments = res_list[res_id]['res_comment'] + res_comments
            comments.sort()
            res_list[res_id]['res_comment'] = comments
            number -= 1

    # print(len(res_list))
    return res_list