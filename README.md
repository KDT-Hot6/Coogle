# Coogle

![Coogle](https://user-images.githubusercontent.com/23492454/114344653-2f41a700-9b9b-11eb-8bb3-c2113474a4e1.png)

## Intro

Coogle은 KoSentenceBERT를 이용한 문장 임베딩 모델 및 fast-text 모델을 기반으로한 단어 임베딩 모델을 활용해 사용자 맞춤형 검색 플랫폼을 제공합니다.  

![content](https://user-images.githubusercontent.com/23492454/114344794-6ca63480-9b9b-11eb-89e9-f86b187c63bd.png)

사용자가 입력한 쿼리는 학습된 임베더 혹은 주어진 단어들의 조합에서 나온 쿼리들에 의해 벡터로 변환됩니다.  

## 서비스 화면 

![Coogle1](https://user-images.githubusercontent.com/23492454/114345053-f524d500-9b9b-11eb-9aec-3f8d53a7f825.png)

## 서비스 아키텍처 구조

모든 리뷰들은 각각의 전처리 과정을 거쳐 raw data와 키워드, 임베딩 벡터 순으로 엘라스틱 서치에 적재되게 됩니다.

![arch1](https://user-images.githubusercontent.com/23492454/114344813-77f96000-9b9b-11eb-9b8f-6d0f981cf91b.png)

사용자 쿼리가 발생하면 Django에 적재된 임베더에 의해 쿼리가 768차원의 벡터로 변환됩니다.    
엘라스틱 서치에 있는 벡터들과 비교해서 가장 유사한 가게를 추천해줍니다. 

![arch2](https://user-images.githubusercontent.com/23492454/114344821-792a8d00-9b9b-11eb-91f5-b1899313e51c.png)

전체적인 로직은 비슷하지만 aws\_django2에 있는 프로젝트는 문장 임베딩을 사용하지 않고 단어 임베딩을 활용합니다.  
검색에 사용된 특징 단어들은 하이라이팅 되어 표현 됩니다.  

서비스의 로직은 다음 코드들을 통해 비교해 보실 수 있습니다.  

### Ver1. 문장 임베딩을 활용한 로직

[문장 임베딩 버전 view.py](https://github.com/KDT-Hot6/Coogle/blob/main/aws\_django/webproj/homepage/views.py)

사용된 모델은 다음 링크에 pt파일로 저장되어 있습니다. 

[학습된 KoSentenceBERT 모델](https://github.com/KDT-Hot6/final\_project/tree/main/model/training\_stsbenchmark\_skt\_kobert\_model\_-2021-03-28\_05-25-43\_best)

### Ver2. 단어 임베딩을 활용한 로직

[단어 임베딩 버전 view.py](https://github.com/KDT-Hot6/Coogle/blob/main/aws\_django2/webproj/homepage/views.py)





