# Volcano-Pharmacy
약품 주문 수량 계산기
## Description
오전/오후 처방 수량에 따라 필요한 주문 수량을 계산해 주는 프로그램 입니다. 
일주문 약품이 아닌 목록의 엑셀파일을 참조하여 처방 수량에서 자동 제외하여 실제 필요한 일주문 리스트 파일을 출력합니다.

주문 수량 계산은 아래와 같습니다.
   + 오전 주문 품목/수량 = 오전 처방수량 리스트에서 일주문 제외 품목를 제외한 품목의 약품 목록/수량
   + 오후 주문 품목/수량 = 오후까지의 처방 목록/수량 (오전+오후) - 오전 처방 목록/수량에서 일주문 제외 품목을 제외한 약품 목록/수량

기본 오전/오후 처방 수량 파일 포맷은 PharmIT3000의 약품별조제판매현황 출력 파일을 사용합니다.
일주문이 아닌 약품 리스트 파일 포맷은 doc\Inventory.xls를 참조합니다.
파일 출력은 src\dist\doc 경로에 생성됩니다.

## Getting Started
### Download
```sh
git clone https://github.com/idujin/Volcano-Pharmacy
cd Volcano-Pharmacy
```
### Build & Run (Optional)
```sh
python src\main.py
```
### Prerequisites (Optional) 
TODO
### Run
```
src\dist\VolcanoHelper.exe
```
