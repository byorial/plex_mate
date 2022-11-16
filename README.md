## Plex Mate
----

#### (개발중) 메뉴는 동작하지 않습니다.

socat TCP-LISTEN:32400,reuseaddr,fork TCP:172.17.0.1:32400
----

#### Change Log
  * 2021-11-01  
    파일정리 : TV쇼 4단계 정리 추가 (매뉴얼 참조)

  * 2021-10-20  
    라이브러리 주기적 스캔 추가
    
  * 2021-08-10  
    라이브러리 복사 : 태그도 복사하도록 변경. 메타 새로고침 필요 없음.


----
#### 소개

** 이 플러그인은 Plex 서버가 실행되는 파일시스템에 접근 가능해야 한다. **

기존 Plex 플러그인은 Plex 서버에 SJVA.bundle 설치 후 그것과 통신하는 구조이다.  
Plex와 SJVA과 다른 네트워크여도 동작하는 장점이 있으나 DB사용 불가,   
Plex 서버 위에서 동작하기 때문에 제한적 코드 사용(python 2.7고정)으로 확장 및 배포의 어려움이 있다. 

이를 보완하기 위해 SJVA와 Plex가 동일 기기나 같은 네트워크 공간에서 실행되는 조건하에   
SJVA.bundle 기능 모두 대체 및 DB 직접 제어와 파일시스템 감시를 통한 스캔을 지원하기 위한 플러그인이다.

동일 네트워크가 불가능 한 경우 기존 Plex도 스캔등에 사용할 수 있으나 업데이트는 하지 않는다.

----

#### 실행환경
  
  * Linux Plex Native 서버 + SJVA 도커   
    SJVA 도커 생성시 -v /:/host 등의 명령으로 호스트 파일시스템에 접근가능하도록 설정

  * Linux Plex Docker 서버 + SJVA 도커   
    도커 볼륨을 통해 사용

  * 윈도우 Plex 서버 + 윈도우 SJVA 

----

#### 권장
  * 추후 추가될 모든 기능을 사용하려면 Plex 서버입장에서 실행파일 위치나, 데이터파일, 비디오파일 경로 값이  
    SJVA 내에서도 일치해야 함.  
    예) Plex Native 인 경우 실행파일은 /usr/lib/plexmediaserver 에 있음.  
    도커 SJVA라면 /host/usr/lib/plexmediaserver 으로 접근가능한데 도커내에서   
    ```ln -s /host/usr/lib/plexmediaserver /usr/lib/plexmediaserver```  
    와 같은 명령으로 아예 Plex Server 처럼 일치시킬 것.
  * 마운트도 host에서 /mnt/gds에 했고 Plex에서도 그대로 사용했다면  
    ```ln -s /host/mnt/gds /mnt/gds```   
    명령을 실행하여 동일 환경을 만들 것.

  
----

#### 주요기능

  * 썸네일 삭제 및 이미지 파일 저장없이 사용
  * 캐시 자동 삭제
  * 라이브러리별 스캔 스케쥴링
  * DB 제어
  * 특이 메타 검색
  * 파일시스템 탐색하여 스캔
  * 파일시스템 감시

