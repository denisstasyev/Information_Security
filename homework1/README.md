# Homework 1

## Task
Написать эксплойт (скрипт), который бы мог залогиниться в DVWA и выполнить команду, используя RCE уязвимость (ping).

## Execution of ping in DVWA
- Скрипт логинится в DVWA
- Выполняет ping на адрес, указанный пользователем при запуске

## Environment
Чтобы запустить скрипт необходимо наличие DVWA, например, через Docker:

1. docker pull citizenstig/dvwa
2. docker run -d -p 8080:80 citizenstig/dvwa

3. docker container ls
4. docker stop {CONTAINER ID}

5. docker images
6. docker image rm -f {IMAGE ID} 
