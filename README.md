# image-merge-utility

merge_test.py 코드 설명

input file
- target.txt : image파일명 목록
- target2.txt : image 좌표파일(txt) 목록
- norm_size.txt : 각 class별 표준 크기 목록

output file
- merge된 png 파일들
- 각 png파일에 들어있는 item의 좌표 목록이 포함된 txt파일들

merge 함수 parameter
- number : merge할 item 개수 (3~9)
- layer[0~2] : 총 3개의 layer, 각 layer 마다 merge할 item 개수
(지금 코드에서는 각 layer별로 item이 무조건 1개 이상 배치)
- h_overlap : height가 overlap 되는 비율 (0.1 ~ 0.5)
- v_overlap : width가 overlap 되는 비율 (0.1 ~ 0.5)
(overlap 비율은 각 item을 merge할 때마다 다시 random하게 설정)
(overlap 비율은 merge할 item기준 비율이 아닌 전에 merge된 item기준 비율에 맞춤)
(ex. 직전에 사과가 merge되었고 v_overlap = 0.4 로 파프리카를 합치는 경우 사과의 오른쪽에서 40% 되는 지점에서부터 파프리카를 merge)

merge 메커니즘(아래쪽 item 이 앞으로 겹쳐진다.)
1. 첫번째 layer
- 첫번째 item은 무조건 (0,0)(=가장 왼쪽 상단)에 위치
- item의 윗라인은 동일하고 v_overlap만큼 겹쳐지게 오른쪽으로 추가

2. 두번째 layer
- 첫번째 item은 첫번째 layer 첫번째 item 기준 h_overlap, v_overlap 비율만큼 오른쪽 아래 방향으로 merge
- 첫번째 item과 윗라인은 동일하고 v_overlap겹쳐지게 오른쪽으로 추가

3. 세번째 layer
- 첫번째 item은 두번째 layer 첫번째 item 기준 h_overlap, v_overlap 비율만큼 오른쪽 혹은 왼쪽 아래 방향으로 merge
- 첫번째 item과 윗라인은 동일하고 v_overlap겹쳐지게 오른쪽으로 추가

4. 뒤집어진 image 생성
- merge된 하나의 합성 이미지가 완성되면 좌우가 뒤바뀐 image 하나 생성하여 filename에 '_flipped' 추가하여 저장
(merge 메커니즘 특성상 오른쪽으로만 추가하여 오른쪽에 있는 물체만 앞으로 겹쳐지게 되는 image파일만 생성되기 때문에 왼쪽에 있는 물체가 앞으로 오는 경우의 image도 학습시켜주기 위함)
