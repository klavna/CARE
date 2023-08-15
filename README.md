<h1 align="center"> 
요리 선택이 어려운 사용자를 위한 재료 인식<br/>
레시피 추천 어플
<br> 
<img src="https://img.shields.io/badge/Python-3776A?style=flat&logo=Python&logoColor=white" width="100">
<img src="https://img.shields.io/badge/YOLO-00FFFF?style=flat&logo=SVG&logoColor=white" width="90">
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=SVG&logoColor=white" width="90">
</h1>

# 목차
1. 문제인식
2. 데이터 출처, 규모, 전처리 방식
3. 어플 구현 과정
4. 한계점과 확장방안

# 1. 문제인식
## 음식 선택과 장보기에 어려움
* 자취생활 중 비슷한 요리만 먹게되고, 시장에 가서 비슷한 재료만 구매하게 되었다.
  
## 시중에 너무 많은 레시피가 있다.
* 레시피 어플과 블로그에 너무 많은 정보가 존재한다.

## 조사결과
![image](https://github.com/klavna/CARE/assets/100742454/8acff2e8-541d-4f4a-8fb2-233736c3a985)


# CARE(Camera Recipe) 어플소개
사진
### 재료 인식

### 사용자 조작

### 레시피 추천

## 데이터 출처, 규모, 전처
### 이미지 데이터
* 크롤링을 통하여 3100장을 모았습니다.
* [Roboflow](https://app.roboflow.com/mainproject)를 사용하여 각 라벨에 대한 라벨링을 수월하게 하였다.
* 토마토, 감자, 새우, 햄 등 31개의 식재료에 대해 정답을 부여하여 인식 가능하게 하였다.

![image](https://github.com/klavna/CARE/assets/100742454/9d8ea001-d4cb-47ee-84cc-29e0d128d8c2)
<p><hr><p>

### 레시피 데이터
* 농식품 빅데이터 거래소 제공해주는 무료 레시피 데이터를 사용하였습니다.
* 컬럼에 레시피 id, 블로그 제목, 레시피 이름, 사용자 id, 사용자 이름, 조회수,추천수,즐겨찾기 수, 요리 방법 등 18개중 사용자 id, 사용자 이름, 블로그 내용 컬럼은 사용하지 않아 삭제하여 15개 컬럼만 사용합니다.
* 총 128,401개의 레시피 중 데이터가 누락되어 있는 경우에 삭제하여, 114,931개 레시피 사용
![image](https://github.com/klavna/CARE/assets/100742454/210beb26-7948-4003-8af8-8249ce38c422)

## CARE의 효과
* 냉장고 속 재료로 만들 수 있는 음식을 고르는데 편의성을 높입니다.
* 입맛이 비슷한 사용자 정보로 다양한 요리를 추천 받을 수 있습니다.
* 기존 재료와 자신의 입맛을 조합하여 레시피를 추천하기 때문에, 필요한 재료를 쉽게 고를 수 있습니다.

## 한계와 발전 방향
- 한계점
  - 레시피간의 유사도를 구하지 못해 추천시스템의 성능이 떨어진다.
  - 재료 이미지 데이터가 부족하여 재료인식 기능이 떨어진다.
  - 비슷한 모양의 포장된 물체를 인식하지 못한다.
 
- 발전 방향
  -  레시피간의 유사도를  [Food2Vec](https://www.cjolivenetworks.co.kr/data/document/%ED%95%9C%EA%B5%ADIT%EC%84%9C%EB%B9%84%EC%8A%A4%ED%95%99%ED%9A%8C_Food2Vec%EC%9D%84%20%EC%9D%B4%EC%9A%A9%ED%95%9C%20%EA%B0%9C%EC%9D%B8%ED%99%94%EB%90%9C%20%EB%A0%88%EC%8B%9C%ED%94%BC%20%EC%B6%94%EC%B2%9C%20%EC%84%9C%EB%B9%84%EC%8A%A4.pdf)방법을 통하여 구한다.
  -  데이터양을 늘려서 재료인식 기능을 높인다.
  -  글자 인식 기술을 통해서 다양한 제품을 인식할수 있게 한다.
         


  

  
