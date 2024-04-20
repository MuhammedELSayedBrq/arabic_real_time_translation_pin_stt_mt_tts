<h3>This repo is about a microphone Max9814 connected to a raspberry pi pico w acting as a sound acuire and 
transmit unit.
then running a server to concatenate, process adc values as audio
a pipeline of two models run to transcripe the audio to arabic text, then 
translate to english --whisper medium OpenAI model--
the translated text is turned into speech with --VITS facebook model--</h3>

**Laptop**
<ul><li>As a processing unit for the ADC values out of MAX9814</li>
<li>Nice to have Nividia GPU that contains cuda cores for Real time factor optimization.</li>
</ul>

**Raspberry Pi pico W**
<ul>
  <li>
interfacing unit with the microphone MAX9814 or Max4466
  </li>
  <li>
socket intiate to stream data to a near wifi point with c language for real time app
</li>

**TODO:**
  </li>
  <li>
    Fine tuning each model for better WER
  </li>
</ul>

**Main & important Scripts are:**
<ul>
  <li>
  app.bat   #run the whole pipeline
  </li>
  <li>
  streamlit_ui.py 
  </li>
  <li>
  whipser_vits_vs.ipynb
  </li>
  <li>
  get_ras_ip.py #get raspberry pi ip by arp response
  </li>
  <li>
  raspberry_python_old/laptop_server.py
  </li>
  <li>
  raspberry_python_old/main.py
  </li>
</ul>
