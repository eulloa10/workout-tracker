import requests
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app_id  = os.environ['APP_ID']
api_key = os.environ['API_KEY']
sheety_token = os.environ['SHEETY_TOKEN']

headers = {
  "x-app-id" : app_id,
  "x-app-key" :  api_key,
  "x-remote-user_id" : "0"
}

user_exercise_input = input("Tell me which exercises you did: ")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise/"

user_params = {
  "query": user_exercise_input,
  "gender":"male",
  "weight_kg":95.3,
  "height_cm":182.88,
  "age":29
}

nutritionix_response = requests.post(url=exercise_endpoint, json=user_params, headers=headers).json()
print(nutritionix_response)

sheety_update_endpoint = os.environ['SHEETY_POST_ENDPOINT']

exercise_type = nutritionix_response['exercises'][0]['name']
exercise_duration = nutritionix_response['exercises'][0]['duration_min']
exercise_calories = nutritionix_response['exercises'][0]['nf_calories']

today = datetime.now()

workout_params = {
  "workout": {
    "date": today.strftime("%m/%d/%Y"),
    "time": today.strftime("%X"),
    "exercise" : exercise_type.title(),
    "duration" : exercise_duration,
    "calories" : round(exercise_calories),
  }
}

headers = {
  "Authorization" : sheety_token
}

sheety_response = requests.post(url=sheety_update_endpoint, json=workout_params, headers=headers)

