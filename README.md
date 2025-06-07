# Neural Audio Sculptor

The Neural Audio Sculptor (NAS) is a tool for artistic expression, designed in the context of my master's thesis. 
NAS allows you to create unique audio-visual experiences supported by an architecture that combines deep learning, 
music information retrieval, and various approaches in human-computer interaction. 
NAS transforms auditory sources into visually immersive, real-time dynamic imagery, 
synchronizing music features with visuals of the user’s choosing. 
This blend of imagery and sound creates a unified experience under the user’s artistic control.  

[HPI Project Side](https://hpi.de/neurodesign/projects/neural-audio-sculptor.html) 


## Videos showcasing NAS
[Video 1](https://drive.google.com/file/d/13SD0WEYPwUVpen3orci_SCpkPuPNfVLM/view)
[Video 2](https://drive.google.com/file/d/1YsU1GZTxhMj2GY_cYU2DGB8KyqLcDZsl/view)
[Video 3](https://drive.google.com/file/d/1NZjWihqOn5EUZRe49AX00lPl-ye3hsG1/view)


## Prerequisite
Before you can start installing and using NAS, you need to do first.

1. Install CUDA 11.8. You can find a list of CUDA drivers and installation instructions [here](https://developer.nvidia.com/cuda-toolkit-archive).
2. Install [ffmpeg](https://ffmpeg.org/download.html).
```bash
# For Linux Ubuntu
sudo apt install ffmpeg
```
3. Install Conda. Instructions can be found [here](https://conda.io/projects/conda/en/latest/user-guide/index.html).
4. Git clone StyleGan-Ada2 Code into [libs](backend%2Flibs)
```bash
cd libs
git clone git@github.com:NVlabs/stylegan2-ada-pytorch.git
```

## A. Installation Process
### Step 1: clone this repository
```bash
git clone https://github.com/MrBanhBao/neural-audio-sculptor
```

### Step 2: create and activate conda environment
```bash
conda create -n nas --no-default-packages python=3.10
conda activate nas
```

### Step 3: install requirements via script
```bash
python install_requirements.py
```

## B. Set config
The [config.yaml](frontend%2Fstatic%2Fconfig.yaml) must be adjusted to your needs.
Following config names must be set to you systems need:
```yaml
backend:
  ...
  cache_dir: <path> # directory where splitted files and feature calculations are stored
  music_dir: <path> # directory containing music files, so the music finder UI component can display them 
  stylegan_checkpoints: <path> # directory containing the stylegan2 checkpoints, so that Model Finder UI component can display them 

stream_diffusion:
  image_inputs: <path> # directory, containing folders with images serving as input imgs for the img2img process
  model_id: 'stabilityai/sd-turbo' # initial diffusion model
  t_index_list: [26, 38] # [6, 28] # time steps with intermediate result (the more steps -> the better the quality -> slower)
```
The rest should/can remain untouched.

## C. Start Backend
Note: This process can take a while when running for the first time.
1. open new terminal with this repo as working directory
2. change to backend directory
```bash
cd backend
```
2. start server
```bash
uvicorn main:app --host 127.0.0.1  
```
Wait till you see. This indicates that the server is running.
```
INFO:     Started server process [40450]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [40450]
```

## D. Start Frontend
1. open new terminal with this repo as working directory
2. change to frontend
```bash
cd frontend
```
3. install needed modules (only need to do once)
```bash
npm install
```

4. start frontend
```bash
npm run dev
```

### Notes:
Check if the frontend ports [main.py](backend%2Fmain.py) are the same as in the cors list.

### Troubleshooting:
In case the NAS Backend starts in CPU mode instead of CUDA mode, you can try running following commands:
```bash
sudo modprobe nvidia_uvm
sudo rmmod nvidia_uvm
sudo kill -9 (ps -A | grep python | awk '{print $1}')
```
These command will free up CUDA memory or release remaining cuda processes.

You might get GPU memory problems, when splitting music files with spleeter, while StreamDiffusion is also loaded in memory.
Best way to avoid this is to precalculate and split the music files. The script [precalculate.py](backend%2Fprecalculate.py)
will loop over you given music directory and split and calculate needed audio features and store them in the cache folder.
```bash
cd backend
python precalculate.py
```
