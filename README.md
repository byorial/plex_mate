### Plex Mate

** 이 플러그인은 Plex 서버가 실행되는 파일시스템에 접근 가능해야 한다. **

#### 주요기능

  * 썸네일 삭제 및 이미지 파일 저장없이 사용
  * 캐시 자동 삭제
  * 라이브러리별 스캔 스케쥴링
  * DB 제어
  * 특이 메타 검색
  * 스캔

## Changelog
- 1.1.15 (2024.09.02)   
  복사용 DB 생성 관련 수정.   

- 1.1.14 (2024.08.22)   
  DB툴 버그픽스.   

- 1.1.13 (2024.08.19)   
  버그 수정: 웹 스캔시 강제로 새로고침 수정   

- 1.1.12 (2024.08.15)   
  플렉스 휴지통 스캔 추가   

- 1.1.11 (2024.08.14)   
  스캔 재시도 버튼 추가   
- 1.1.10 (2024.08.14)
    - 설정
        - 프로그램 경로, 데이터 경로 오류 메시지 수정
    - vfs/refresh 규칙
        - 규칙이 여러 개일 경우 발생하는 오류 수정
        - 규칙에 리모트 이름 설정 추가
            - 하나의 RC 서버에 여러 리모트를 마운트한 경우 사용
            - 구분자로 #도 사용하기 때문에 규칙에 코멘트 사용 불가
    - 주기적 스캔
        - 스캔모드 "웹" 실행시 "폴더"를 지정하면 부분 스캔 실행
        - 새로고침(vfs/refresh) 추가
    - 스캔
        - 탐색 페이지 추가
        - 타임오버 항목 재설정 추가
        - 최대 스캔 시간 설정, FINISH_SCANNING 상태 추가
            - 테스트 후 둘 중 하나를 제거
        - REMOVE 모드시 vfs/forget 실행

- 1.1.9 (2024.08.13)   
  DB 툴: 메타만 지우기, yaml 가사정보 Fix 추가.   

- 1.1.8 (2024.08.12)   
  라이브러리 복사2 추가.   

- 1.1.6 (2024.06.26)   
  rclone vfs/refresh OK 받을 때까지 상위폴더 refresh.   

- 1.1.4 (2024.06.18) by ocelot   
  rclone vfs/refresh rc 인증정보 추가.   

- 1.1.3 (2024.06.13)   
  스캔시 rclone vfs/refresh 호출 기능 추가   

- 1.1.2 (2024.06.11)   
  스캔, 파일정리 점검   

- 2024.05.29 (by 한시오분)   
  변경된 Plex DB의 extra_data 컬럼 내 쌍따옴표 데이터 처리 추가   