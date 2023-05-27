# Tracking the weather in your city (update in progress)
<p align='center'>
  <img src = "https://github.com/SwamiKannan/Revisiting-Python/blob/main/Weather_tracking/cover.png" width=30%><br>
  <sub><a href="https://www.flaticon.com/free-icons/weather" title="weather icons">Weather icons created by Freepik - Flaticon</a></sub>
  </p>

This is an exercise to understand the SMPP protocol using Twilio. The project takes in a <city, country> name and sends you an SMS greeting consisting of the following:
<ul>
  <li> The temperature in your city in ℃ </li>
  <li> Current weather </li>
  <li> Custom text based on whether the temperature is above or below 30℃ </li>
  <li> Motivational quote of the day </li>
  </ul>

## Key instructions:
<ol>
  <li> <b>Twilio</b> </li>
  <ul>
    <li> Create a <a href="https://www.twilio.com/en-us">Twilio account </a> (free).</li>
    <li> Grab the Twilio SID and save it in the environment as the variable "twilio_SID". This is described <a href="https://www.twilio.com/blog/environment-variables-python">here</a></li>
    <li> Grab the Twilio auth token and save it in the environment as the variable "twilio_SID". This is described <a href="https://www.twilio.com/blog/environment-variables-python">here</a></li>
    <li> Make sure the destination number to where the SMS is to be sent is registered in <b>Console -> Phone Numbers -> Verified Caller IDs </b><br></li>
  </ul>
  <br>
  <li><b>OpenWeather</b> </li>
  <ul>
    <li> Register an account at <a href="https://home.openweathermap.org/users/sign_up">OpenWeather</a></li>
    <li> Extract the API from Username (second from right at the top) -> "My API keys" and copy the text under the Key field</li>
    <li> Extract the API from Username -> "My API keys" and copy the text under the Key field</li>
    <li> Save this text as an environment variable called OWM_KEY. This is described <a href="https://www.twilio.com/blog/environment-variables-python">here</a></li>
  </ul><br>
  <li><b>Code run</b></li>
  </ul>
  </ol>
  
    python main.py

  
