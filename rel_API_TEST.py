from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
from konlpy.tag import Kkma, Okt  # Okt로 수정
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

app = Flask(__name__)

# Elasticsearch 설정
ES_URL = "http://192.168.0.207.es.gobgnews.sslip.io:80/ALIAS_article_1/_search"
ES_AUTH = HTTPBasicAuth("elastic", "mediahub")
ES_HEADERS = {"Content-Type": "application/json"}

# 쿼리 DSL
QUERY = {
    "query": {
        "match_all": {}
    },
    "size": 10000,
    "_source": ["summary", "subTitle", "title" ,"id"]  # 추출할 필드 지정
}

# 데이터 조회 함수
def search_data():
    response = requests.post(ES_URL, json=QUERY, auth=ES_AUTH, headers=ES_HEADERS)
    response.raise_for_status()  # 요청이 실패하면 예외를 발생시킴
    return response.json()["hits"]["hits"]

@app.route('/similar_articles', methods=['POST'])
def similar_articles():
    data = request.json
    input_summary = data.get('summary', '')
    input_title = data.get('title', '')
    input_subtitle = data.get('subtitle', '')

    twitter = Okt()
    
    # Elasticsearch에서 데이터 조회
    results = search_data()

    mydoclist_twitter = []

    for result in results:
        article_text = result['_source'].get('summary', '') + ' ' + result['_source'].get('subTitle', '') + ' ' + result['_source'].get('title', '')
        twitter_nouns = ' '.join(twitter.nouns(article_text))
        mydoclist_twitter.append(twitter_nouns)

    # 입력된 텍스트를 명사 리스트로 변환
    input_text = input_summary + " " + input_title + " " + input_subtitle
    input_nouns = ' '.join(twitter.nouns(input_text))

    # TF-IDF 벡터화
    tfidf_vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix_twitter = tfidf_vectorizer.fit_transform(mydoclist_twitter + [input_nouns])

    # 입력된 텍스트와 각 문서 간의 유사도 계산
    input_vector = tfidf_matrix_twitter[-1]
    document_vectors = tfidf_matrix_twitter[:-1]

    similarities = (document_vectors * input_vector.T).toarray().flatten()

    # 유사도 상위 5개 기사 인덱스 추출
    top_indices = similarities.argsort()[-5:][::-1]

    # 유사도 상위 5개 기사 결과 생성
    top_articles = []
    for idx in top_indices:
        top_articles.append({
            "url": results[idx]['_source'].get('url', 'N/A'),
            "similarity": similarities[idx],
            "title": results[idx]['_source'].get('title', 'N/A'),
            "summary": results[idx]['_source'].get('summary', 'N/A'),
            "subtitle": results[idx]['_source'].get('subTitle', 'N/A')
        })

    return jsonify(top_articles)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
