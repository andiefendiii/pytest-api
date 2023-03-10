import requests
import pytest
import json
import jsonpath
import random
import os
from pathlib import Path



baseUrl = "https://reqres.in/"

####################################### Register ##############################################
def test_register_success():
    path = "api/register"
    payload = json.dumps(
    {
    "email": "eve.holt@reqres.in",
    "password": "pistol"
    })

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 200
    print(response.text)


def test_register_blankEmail():
    path = "api/register"
    payload = json.dumps(
    {
    "email": "",
    "password": "pistol"
    })

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 400
    print(response.text)
    responseJson = json.loads(response.text)
    assert jsonpath.jsonpath(responseJson,'$.error')[0] == 'Missing email or username' 


def test_register_blankPassword():
    path = "api/register"
    payload = json.dumps(
    {
    "email": "eve.holt@reqres.in",
    "password": ""
    })

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 400
    print(response.text)    
    responseJson = json.loads(response.text)
    assert jsonpath.jsonpath(responseJson,'$.error')[0] == 'Missing password' 

####################################### Login ##############################################

def test_login_success():
    global tokenLogin

    path = "api/login"
    payload = json.dumps(
    {
    "email": "eve.holt@reqres.in",
    "password": "cityslicka"
    }
    )

    headers = {'Content-Type': 'application/json'}   
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 200
    print(response.text)
    jsonResponse = response.json()
    tokenLogin = jsonResponse['token']


def test_login_invalidName():
    global tokenLogin

    path = "api/login"
    payload = json.dumps(
    {
    "email": "eve.holt@reqres.i",
    "password": "cityslicka"
    }
    )

    headers = {'Content-Type': 'application/json'}   
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 400
    print(response.text)
    responseJson = json.loads(response.text)
    assert jsonpath.jsonpath(responseJson,'$.error')[0] == 'user not found' 


def test_login_blankEmail():
    global tokenLogin

    path = "api/login"
    payload = json.dumps(
    {
    "email": "",
    "password": "cityslicka"
    }
    )

    headers = {'Content-Type': 'application/json'}   
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 400
    print(response.text)
    responseJson = json.loads(response.text)
    assert jsonpath.jsonpath(responseJson,'$.error')[0] == 'Missing email or username'     
  

def test_login_blankPassword():
    global tokenLogin

    path = "api/login"
    payload = json.dumps(
    {
    "email": "eve.holt@reqres.in",
    "password": ""
    }
    )

    headers = {'Content-Type': 'application/json'}   
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 400
    print(response.text)
    responseJson = json.loads(response.text)
    assert jsonpath.jsonpath(responseJson,'$.error')[0] == 'Missing password'      

####################################### List User ##############################################

def test_list_user():
   
    path ="api/users?page=2"
    headers = {
        'Authorization':'Bearer '+tokenLogin, 'Content-Type':'application/json'
        } 
    
    response = requests.get(url=baseUrl+path, headers=headers)
    assert response.status_code == 200
    print(response.text)

####################################### List User Detail ##############################################
def test_list_detail_user():
   
    path ="api/users/2"
    headers = {
        'Authorization':'Bearer '+tokenLogin, 'Content-Type':'application/json'
        } 
    response = requests.get(url=baseUrl+path, headers=headers)
    assert response.status_code == 200
    print(response.text)   


def test_list_detail_user_invalidUserNotFound():
   
    path ="api/users/99"
    headers = {
        'Authorization':'Bearer '+tokenLogin, 'Content-Type':'application/json'
        } 
    response = requests.get(url=baseUrl+path, headers=headers)
    assert response.status_code == 404
    print(response.text)         

####################################### Create User ##############################################
def test_create_user():
    global newUserID
    randNum = random.randint(0, 1000)
    convert_randNum = str (randNum)

   
    path ="api/users"

    payload = json.dumps(
    {
    "name": "Andi"+(convert_randNum),
    "job": "SQA"
    })

    headers = {
        'Authorization':'Bearer '+tokenLogin, 'Content-Type':'application/json'
        } 
    response = requests.post(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 201
    print(response.text)   
    jsonResponse = response.json()
    newUserID = jsonResponse['id']

####################################### Update User ##############################################
def test_update_user():
    global newUserID
    randNum = random.randint(0, 1000)
    convert_randNum = str (randNum)

   
    path ="api/users/"+str(newUserID)


    payload = json.dumps(
    {
    "name": "Andi"+convert_randNum,
    "job": "SQA"
    })

    headers = {
        'Authorization':'Bearer '+tokenLogin, 'Content-Type':'application/json'
        } 
    response = requests.put(url=baseUrl+path, headers=headers, data=payload)
    assert response.status_code == 200
    print(response.text)       
  

####################################### Delete User ##############################################
def test_delete_user():
    global newUserID
    randNum = random.randint(0, 1000)
    convert_randNum = str (randNum)

   
    path ="api/users/"+str(newUserID)

    headers = {
        'Authorization':'Bearer '+tokenLogin, 'Content-Type':'application/json'
        } 
    response = requests.delete(url=baseUrl+path, headers=headers)
    assert response.status_code == 204
    print(response.text)  
