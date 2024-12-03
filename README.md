1.elasticSearch 연결

2.해당 파이썬 파일 실행

3.api 호출
  curl -X POST http://127.0.0.1:5000/similar_articles \
  -H "Content-Type: application/json" \
  -d '{
      "summary": "테스트 기사 요약",
      "title": "테스트 제목",
      "subtitle": "테스트 소제목"
  }'
  
4.결과 확인
ex) 
[
    {
        "similarity": 0.6956583266086511,
        "subtitle": "테스트입니다.",
        "summary": "@바이라인 설정 테스트 테스트 테스트",
        "title": "기사 테스트",
        "url": "N/A"
    },
    {
        "similarity": 0.6211860693421414,
        "subtitle": "부제목",
        "summary": "221번 기사 테스트 221번 기사 테스트 @바이라인 설정",
        "title": "221번 기사 테스트",
        "url": "N/A"
    },
    {
        "similarity": 0.4968523393893519,
        "subtitle": "",
        "summary": "@바이라인 설정 테스트책ㅇㅇㅇㅇㅇ",
        "title": "테스트책2",
        "url": "N/A"
    },
    {
        "similarity": 0.4968523393893519,
        "subtitle": "",
        "summary": "@바이라인 설정 테스트책111",
        "title": "테스트책1",
        "url": "N/A"
    },
    {
        "similarity": 0.4968523393893519,
        "subtitle": "",
        "summary": "@바이라인 설정 테스트책111",
        "title": "테스트책1",
        "url": "N/A"
    }
]
