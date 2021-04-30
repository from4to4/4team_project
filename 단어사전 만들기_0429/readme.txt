- 05.단어사전 만들기.ipynb : 모델1 감성분석 모델을 통해 => 긍정/부정 평가에 영향을 준 단어 리스트 추출하는 과정

- 단어 사전
	- adjective_list.pickle : 형용사 리스트
	- noun_list.pickle : 명사 리스트
	- verb_list.pickle : 동사 리스트
	- coef_pos_text : 모둔 단어 리스트
	
- 모델
	- sentiment_analysis_model.dat : 감성분석 모델
	- tfidf_vectorizer1.dat : tfidf 벡터라이저 
	
- 리스트 불러오기
import pickle
with open('data/adjective_list.pickle', 'rb') as f: 
	adjective_list = pickle.load(f) # 리스트 불러오기
