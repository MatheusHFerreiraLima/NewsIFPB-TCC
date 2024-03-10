# python-tccparte2
 tentando fazer uma parte 2 aqui

comandos básicos necessários para caso o clone do repositório não dê certo. aí você só copia e cola os comandos e os arquivos:

Tambem exclua o .venv dos seus arquivos se você clonou o repositório e crie um novo

no terminal do Visual Studio do Windows:

    Para criar o venv:

        cmd
        py -3 -m venv .venv
        .\.venv\Scripts\activate.bat (talvez não dê pra ver, mas existe uma contra batta antes do ".venv", o que separa os dois pontos)
        pip install django
        pip install feedparser 
        pip install pytz (eu acho)
        pip install imapclient 


    para testar o projeto (dentro do venv):

        django-admin startproject [nome do projeto] (talvez essa parte você não precise se clonou o repositório, pois ela já existe lá )
        cd [nome do projeto]
        py manage.py startapp [nome do app]
        py manage.py runserver (para testar)

Depois configura o Banco de dados no sqlite com um manage.py migrate e manage.py makemigrations



