# MD기반 근로자 위험도 예측 알고리즘 (MongoDB version)


## 1. MD알고리즘이란?
- 목적: 다차원 데이터 공간에서 각 근로자의 데이터 포인트를 사고 발생 집단과 비교하여 근로자의 사고 위험도를 정량적으로 평가. 
<br/> Mahalanobis Distance를 사용하여 다변량 데이터의 중심(평균)과의 거리를 측정하고, 변수들 간의 상관관계를 고려하여 
<br/> 각 데이터 포인트의 이상치 정도를 평가.

- 위험 예측: 근로자의 특성(공사규모, 사고발생시간, 나이, 경력)을 통합적으로 고려하여 사고 위험도를 예측. 
<br/> 이를 통해 특정 근로자의 위험도가 높은지를 판단할 수 있음. 

## 데이터 정의 (사고 VS 비사고 데이터)
 - 사고 데이터 : KOSHA(산업안전보건공단) 52,872건
 - 비사고 데이터 : GH(보건환경연구원) 64,743건

## MongoDB 정의
 - database명 : accident_data
 - collection명 : accidents(사고데이터), non_accidents(비사고데이터)

## 데이터 전처리 
1. 사고데이터(KOSHA 데이터)  <br/>

    |공통컬럼명|KOSHA 컬럼명|변경내역|
    |------|---|---|
    |나이|출생년도|별도 계산필요|
    |발생일자|동일|yyyy-mm-dd 형태로 변환 필요 |
    |발생시간|동일||
    |근무경력|근무일수||
    |공사규모|동일| |
    |발생요일|없음|발생일자에서 발생요일 추출|
    |발생월|없음|발생일자에서 발생월 추출|

 2. 비사고데이터(GH, 보령 데이터) <br/>
  
    |공통컬럼명|KOSHA 컬럼명|변경내역|
    |------|---|---|
    |나이|생년월일|별도 계산필요|
    |발생일자|출력일자| yyyy-mm-dd 형태로 변환 필요 |
    |발생시간|없음| 일괄적으로 8시 추가|
    |근무경력|건설업근무경력||
    |공사규모|현장규모| |
    |발생요일|출역일자|발생일자에서 발생요일 추출|
    |발생월|없음|발생일자에서 발생월 추출|

 <br/>

---

## 다변량 분석을 통한 변수 선별
  **1. Random Forest** <br/> 
      &nbsp; &nbsp; - Random Forest는 수많은 의사 결정 트리가 모여서 생성. 전체 Feature 중 랜덤으로 일부 Feature만 선택하여 하나의 결정 트리를 만들고, <br/> 
      &nbsp; &nbsp; &nbsp; 또 전체 Feature 중 램덤으로 일부 Feature를 선택해 또 다른 결정 트리를 만들며, 여러 개의 결정 트리를 만드는 방식으로 구성. <br/> &nbsp; &nbsp; &nbsp;  의사 결정 트리마다 하나의 예측값을 내놓음. <br/> 
    &nbsp; &nbsp; - 여러 결정 트리들이 내린 예측 값들 중, 가장 많이 나온 값을 최종 예측값으로 정함. 여러 가지 결과를 합치는 방식을 앙상블 <br/>
    &nbsp; &nbsp; &nbsp; 즉, 하나의 거대한 결정 트리를 만드는 것이 아니라 여러 개의 작은 결정 트리를 만드는 것 <br/>
    &nbsp; &nbsp; - 여러 개의 작은 결정 트리가 예측한 값들 중. 가장 많이 등장한 값 또는 평균값을 최종 예측값으로 정함 <br/>
  <br/>

  **2. XGBoost** <br/> 
    &nbsp; &nbsp; - 여러 개의 약한 **결정 트리(Decision Tree)**를 조합하여 강력한 예측 모델을 만드는 부스팅 앙상블 기법 중 하나 <br/>
    &nbsp; &nbsp; - 약한 예측 모델(약한 학습기)의 학습 오류에 가중치를 두고, 순차적으로 다음 학습 모델에 반영하여 예측 성능을 점진적으로 개선 <br/>
    &nbsp; &nbsp; - 데이터를 일정 간격으로 나누어 **최적의 분할(split)** 을 찾는 과정을 병렬 처리하여 학습 속도를 크게 향상 <br/>
<br/>
   * 분할방식
     
     > exact : 모든 피처의 모든 데이터값을 분할 후보군으로 고려하는 기본 방식(바닐라 Gradient Boosting).  가장 정확하지만 데이터가 많을수록 시간 많이 소요
     > approx : 데이터를 분위수(quantile)로 나누어 각 그룹별로 최적의 분할 포인트를 찾는 방식. exact보다 효율적이며, 대규모 데이터에서도 적합
     > hist : 데이터를 히스토그램(bin)으로 구분하여 최적의 분할 포인트를 찾는 방식. 메모리 사용량이 적음
     > gpu_hist : hist 방식의 GPU 구현 버전으로, GPU를 활용해 학습 속도를 더욱 높임

 <br/>
 
  **3. LightGBM** <br/> 
     - 트리 기반 학습 알고리즘으로, **틀린 부분(오류)에 가중치를 더하며 반복 학습**을 진행하는 방식입니다.

**학습 과정**:
  1. 첫 번째 단계에서 **Tree 모델 1**을 사용해 목표값 \(Y\)를 예측합니다.
  2. 예측 오차(잔차, \(residual = true - predicted\))를 계산합니다.
  3. 이 잔차를 **Tree 모델 2의 입력 데이터**로 사용하여 학습합니다.
  4. 같은 방식으로 **Tree 모델 3**도 이전 단계의 잔차를 입력으로 학습합니다.
  5. 이러한 과정을 반복하여, **잔차가 점점 작아지면서 예측 성능이 개선**됩니다.

- Leaf-wise Tree 분할 방식
     - 트리의 균형(level)을 유지하지 않고, **최대 손실값(max data loss)을 가진 Leaf Node를 반복적으로 분할**하는 방식입니다.
     - 트리의 깊이가 깊어지고, 비대칭적인 트리가 생성됩니다.
     - 가장 중요한 노드를 우선적으로 분할하므로 **Level-wise Tree 분할 방식보다 예측 오류 손실을 최소화**할 수 있습니다.
     - 성능 면에서 효율적이며, 특히 복잡한 데이터에서 높은 성능을 보입니다.
 
 <br/>

**4. Boxplot 그리기** <br/> 
 - boxplot 분석을 통해 두집단(사고발생집단과 사고 비발생 집단)간에 분포 차이가 크게 나타난 변수들을 선별   <br/>
 
   <div style="display: flex; justify-content: space-between; align-items: center;">
       <img src="https://github.com/user-attachments/assets/c5eb1425-f1c1-48dd-b85b-5be7f03f1bf0" alt="Image 1" style="width: 300px;">
       <img src="https://github.com/user-attachments/assets/b54f6a3d-87c3-46ff-abfe-7483aab7522d" alt="Image 2" style="width: 300px;">
       <img src="https://github.com/user-attachments/assets/17d5b112-70b1-49f7-b18e-1ea07fc6b068" alt="Image 3" style="width: 300px;">
   </div> 
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <img src="https://github.com/user-attachments/assets/8e2973d3-6e60-4dd9-b301-6c7515825cbf" alt="Image 4" style="width: 300px;">
        <img src="https://github.com/user-attachments/assets/cb17c559-98eb-4126-b83d-cf0d912d564e" alt="Image 5" style="width: 300px;">
        <img src="https://github.com/user-attachments/assets/5a7aab26-02fa-4a71-8f4c-6a1c515e714a" alt="Image 6" style="width: 300px;">
    </div>

<br/> 

### ※ 종합적인 결과, '근무경력', '나이', '공사규모', '발생시간' 변수가 사고 위험도를 예측하는데 중요한 변수로 선별 ※

---
 
## 마할라노비스(Mahalanobis) 계산하기 

 **1. 공분산 행렬 계산** <br/> 
 - 사고, 비사고 데이터 각각 공분산 행렬 계산

   ```
       def robust_cov(data) :
        #2차원 행렬로 반환을 해야 공분산 계산이 가능
        #이상치를 배제한 후 데이터의 일부를 사용하여 공분산 행렬 계산
        #data = data.to_numpy()
        robust_cov = MinCovDet().fit(data)
        return robust_cov.covariance_

   ```

* 공분산 행렬이란?

  > 데이터 세트의 변수들 사이의 공분산 값을 정리한 정방 행렬(square matrix)로, 데이터의 변수 개수에 따라 행렬의 크기가 결정 <br/>
  > 행렬의 크기 : n x n (n: 변수의 개수) <br/>
  > 항목이 6개면 36개의 특성을 가짐. => 각 요소는 두 특성간의 공분산 값을 나타내며, 1296개의 공분산 값을 포함 <br/>
  > 데이터 축소나 변환 : 데이터를 변환하거 축소하는 과정에서 특성의 수가 줄어 들 수가 있음 <br/>

<br/>

 **2. MD 계산** <br/> 
 - **MD(마할라노비스 거리)** 는 개별 점과 데이터 분포 간의 거리를 측정하는 방법
 - 사고 및 비사고 데이터를 기반으로 공분산 행렬을 사용하여 MD 값을 계산
 - 계산된 MD 값을 Z-score로 변환한 뒤, Z-score의 절대값이 1.96 이하인 데이터를 선택. <br/> 이는 정규분포에서 약 95%의 데이터를 포함하는 범위  

 <br/>

  **3. 정규화(minmaxscaling)** <br/> 
  - 

## 시각화 
- MD -> logMD
- MD -> normalize
- MD -> log MD -> normalize

## 위험도 예측


