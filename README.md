# CXR-BDM

Chest X-ray file (DICOM)을 활용해 다양한 질병을 예측하는 AI 모델 구현을 하고 있습니다 

for now, predicting osteoporosis with chest X-ray

using Colaboratory

1차 Data preprocessing level 

> DICOM 파일의 pixel_array (metadata)를 불러와서 list에 append 하고 이를 통째로 사용하는 방법 사용

그리고 PatientID를 활용하여 osteoporosis 진단 결과가 있는 csv의 파일의 index 활용하여 label data도 list append

ipynb 파일은 google colab에서 바로 github으로 사본 저장 하니 업로드 하고 나서 계속 코드가 안 뜨는 것이다. 알고보니 병원 보안으로 인한 것이었다. 여튼 그래서 colab에서 local에 다운 받아서 py 파일로 재업로드한 것




추출한 DICOM 파일의 원본 pixel 크기가 너무 커서 pickle로 load해둔 x_train data를 불러올 때 런타임 오류가 계속 남.

그래서 일부의 data만 사용하여 일단 모델 돌려보는 것을 목표로 연구를 진행
