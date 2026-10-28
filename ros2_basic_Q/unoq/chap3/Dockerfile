FROM ros:lyrical-ros-base 

RUN apt-get update && apt-get install -y \ 
tmux \ 
python3-pip \ 
curl \ 
jq \ 
&& rm -rf /var/lib/apt/lists/* 

RUN ASSET_URL=$(　\
curl -s https://api.github.com/repos/arduino/app-bricks-py/releases/latest \ 
| jq -r '.assets[] | select(.name | endswith(".whl")) | .browser_download_url') && \ 
cd /tmp && curl -L -O "$ASSET_URL" && \ 
ls -la /tmp/*.whl 

RUN pip3 install --break-system-packages --ignore-requires-python \ 
/tmp/*.whl \ 
arduino-router-bridge \ 
watchdog \ 
&& rm /tmp/*.whl 

RUN python3 -c "from arduino.app_utils import *; print('arduino.app_utils OK')" 

WORKDIR /workspace 
RUN chown -R ubuntu:ubuntu /workspace
