# [Docker](https://docs.docker.com/get-docker/)

## 설치
### WSL 활성화하기
```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
### WSL2 지정
```powershell
wsl --set-default-version 2
```

### [Docker Download](https://www.docker.com/products/docker-desktop)  
```powershell
https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header
```
### Docker 설치
Docker Desktop Installer.exe
```
PS C:\workspace\AWSBasic> docker version
Client:
Version:           20.10.12
API version:       1.41
Go version:        go1.16.12
Git commit:        e91ed57
Built:             Mon Dec 13 11:44:07 2021
OS/Arch:           windows/amd64dock
Context:           default
Experimental:      true
error during connect: This error may indicate that the docker daemon is not running.: Get "http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.24/version": open //./pipe/docker_engine: The system cannot find the file specified.
PS C:\workspace\AWSBasic> 
```


## Dockerfile 형식
| 항목 | 설명 |  
|:---|:---|  
| FROM | Base Image 지정(OS 및 버전 명시, Base Image에서 시작해서 커스텀 이미지를 추가) |  
| RUN | shell command를 해당 docker image에 실행시킬 때 사용함 |  
| WORKDIR | Docker File에 있는 RUN, CMD, ENTRYPOINT, COPY, ADD 등의 지시를 수행할 곳 |  
| EXPOSE | 호스트와 연결할 포트 번호를 지정 |  
| CMD | application을 실행하기 위한 명령어 |  

## Dockerfile 예
- echo
  ```
  FROM alpine:3.10

  ENTRYPOINT ["echo", "hello"]
  ```
- nginx
  ```
  FROM nginx:latest
  RUN  echo '<h1> test nginx web page </h1>'  >> index.html
  RUN cp /index.html /usr/share/nginx/html
  ```

## Docker 명령
| 항목 | 설명 |  예 |
|:---|:---|:---|    
| build | 이미지 만들기 | docker build -t test-image . |  
| images | 생성된 이미지 확인 | docker images |  
| run | 컨테이너 이미지를 실행 | docker run -p 8080:80 --name test-nginx test-image |  
| ps | 실행중인 컨테이너 확인 | docker ps |  
| logs | 컨테이너의 로그를 출력해서 상태 확인 | docker logs -f test-nginx |  
| exec | 컨네이너 내부 쉘 환경 접근 | docker exec -it test-nginx /bin/bash |  
| stop | 실행중인 컨테이너 중지 | docker stop test-nginx |  
| rm | 컨테이너 삭제 | docker rm test-nginx |  
| rmi | 컨테이너 이미지 삭제 | docker rmi test-image |  
 

## [Hyper-V에 k8s 설치](https://github.com/JINYONG-LEE/etc/blob/main/k8s/README.md) 
