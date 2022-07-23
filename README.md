# myinfo-connector-python

<br> 

| Start Date      | 2022-07-05                                          |
|-----------------|-----------------------------------------------------|
| End Date        | 2022-07-23                                          |
 
 <br> 
 
This is repository for Python/Django Connector for Singapore government mydata service, Singpass myinfo. 
MyInfo Connector aims to simplify consumer's integration effort with MyInfo by providing an easy to use Python library to integrate into your application.

Myinfo provide [Java](https://github.com/singpass/myinfo-connector-java), [nodejs](https://github.com/singpass/myinfo-connector-nodejs) connector. I wanted to use myinfo API in Python, so I made a myinfo connector with python.
<br> 
<br> 

## Documents 

Check Quick Start: [link](https://leelee-1.gitbook.io/myinfo-connector-python-api-doc/myinfo-connector-python-api/quick-start) <br> 
Check API Doc: [link](https://leelee-1.gitbook.io/myinfo-connector-python-api-doc/myinfo-connector-python-api/v1.0)


<br> 
<br> 

## Quick Start 

> myinfo-connector-python is built with Django to make easy-to-go application.


### Step 1: Clone the repository in your local


```
git clone git@github.com:leeleelee3264/myinfo-connector-python.git
```

### Step 2: Install Pre-requisite

#### Install Python

> You can exclude python 3 is already installed in your local.

```
brew install python@3.8 pipenv
```

#### Set Python Path in \~/.zshrc
```
export PATH="/opt/homebrew/opt/python@3.8/bin:$PATH"
```
#### Refresh \~/.zshrc&#x20;
```
source ~/.zshrc
```


### Step 3: Install python packages
```
PIPENV_VENV_IN_PROJECT=1 
cd ~/myinfo-connector-python
pipenv install 
```

### Step 4: Start server
```
pipenv run ./connector/manage.py runserver 0:3001
```
<br> 
<br> 

## Make your request
The REST API to make request is described below.

### Step 1: Get myinfo redirect login url

#### Request 
`GET /users/me/external/myinfo-redirect-login`

```
curl -i -H 'Accept: application/json' http://localhost:3001/user/me/external/myinfo-redirect-login
```

#### Response
```json
{
    "message": "OK",
    "data": {
        "url": "https://test.api.myinfo.gov.sg/com/v3/authorise?client_id=STG2-MYINFO-SELF-TEST&attributes=name,dob,birthcountry,nationality,uinfin,sex,regadd&state=eb03c000-00a3-4708-ab30-926306bfc4a8&redirect_uri=http://localhost:3001/callback&purpose=python-myinfo-connector",
        "state": "eb03c000-00a3-4708-ab30-926306bfc4a8"
    }
}
```

<br>

### Step 2: Browse myinfo redirect login

```
curl https://test.api.myinfo.gov.sg/com/v3/authorise?client_id=STG2-MYINFO-SELF-TEST&attributes=name,dob,birthcountry,nationality,uinfin,sex,regadd&state=eb03c000-00a3-4708-ab30-926306bfc4a8&redirect_uri=http://localhost:3001/callback&purpose=python-myinfo-connector
```

<br>

### Step 3: Do login and check agree terms

#### Myinfo Login Page
![Myinfo Login Page](https://3820993574-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FlInvAOhF8qXySERII8EX%2Fuploads%2FE6IjtdApO2Y4Vh0Jmv7F%2F%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-07-23%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%2010.18.51.png?alt=media&token=a5dea997-eaa6-4e97-a6d2-34d44874c174)


#### Myinfo Terms Agreement Page
![Myinfo Terms Agreement Page](https://3820993574-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FlInvAOhF8qXySERII8EX%2Fuploads%2F0Rkc1LoDTjZN6MelW1a6%2F%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-07-23%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%2010.19.35.png?alt=media&token=8a57d719-9333-40af-8fbc-af566b914471)

<br>

### (Automated) Step 4: Callback API get called by Myinfo

After login Myinfo and agree terms, Myinfo service automatically call myinfo-connector-python's callback API to pass auth code.
The authcode given by [myinfo's authorise API](https://public.cloud.myinfo.gov.sg/myinfo/api/myinfo-kyc-v3.2.2.html#operation/getauthorise)

#### callback url example

```
http://localhost:3001/callback?code=8932a98da8720a10e356bc76475d76c4c628aa7f&state=e2ad339a-337f-45ec-98fa-1672160cf463
```

#### callback response HTML example
![Response Page for callback api](https://3820993574-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FlInvAOhF8qXySERII8EX%2Fuploads%2FAR3Gcn5qGLw3XJOdDkUI%2F%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-07-23%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%2010.32.34.png?alt=media&token=88db50e3-c937-481d-93e1-0e69b4c7c16b)

<br>

### (Automated) Final Step: Get Person data from Myinfo

After callback, callback page automatically calls our api for person data. The API is final step of myinfo-connector-python.

#### Request 
`GET /users/me/external/myinfo`

```
curl -i -H 'Accept: application/json' http://localhost:3001/user/me/external/myinfo
```

#### Response 

```json
{
    "message": "OK",
    "sodata": {
        "regadd": {
            "country": {
                "code": "SG",
                "desc": "SINGAPORE"
            },
            "unit": {
                "value": "10"
            },
            "street": {
                "value": "ANCHORVALE DRIVE"
            },
            "lastupdated": "2022-07-14",
            "block": {
                "value": "319"
            },
            "source": "1",
            "postal": {
                "value": "542319"
            },
            "classification": "C",
            "floor": {
                "value": "38"
            },
            "type": "SG",
            "building": {
                "value": ""
            }
        },
        "dob": "1988-10-06",
        "sex": "M",
        "name": "ANDY LAU",
        "birthcountry": "SG",
        "nationality": "SG",
        "uinfin": "S6005048A"
    }
}
```




<br>
<hr> 


 ## Project TODO List 
- [x] 1st Implement 
- [x] Apply Pipenv for package management 
- [x] Apply python lint (flake8, pylint, mypy) 
- [x] Documentation 
- [x] 2nd Refactoring (Move DTO to domain layer)
- [x] 3th Redactoring (Entire)
