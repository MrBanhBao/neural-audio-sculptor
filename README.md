# Neural Audio Sculptor

The Neural Audio Sculptor (NAS) is a tool for artistic expression, designed in the context of my master's thesis. 
NAS allows you to create unique audio-visual experiences supported by an architecture that combines deep learning, 
music information retrieval, and various approaches in human-computer interaction. 
NAS transforms auditory sources into visually immersive, real-time dynamic imagery, 
synchronizing music features with visuals of the user’s choosing. 
This blend of imagery and sound creates a unified experience under the user’s artistic control.

## Prerequisite
Before you can start installing and using NAS, you need to do first.

1. Install CUDA 11.8. You can find a list of CUDA drivers and installation instructions [here](https://developer.nvidia.com/cuda-toolkit-archive).
2. Install [ffmpeg](https://ffmpeg.org/download.html).
```bash
# For Linux Ubuntu
sudo apt install ffmpeg
```
3. Install Conda. Instructions can be found [here](https://conda.io/projects/conda/en/latest/user-guide/index.html).

## Installation Process
### Step 1: clone this repository
```bash
git clone https://github.com/MrBanhBao/neural-audio-sculptor
```

### Step 2: create and activate conda environment
```bash
conda create -n nas --no-default-packages python=3.10
conda activate nas
```

### Step 3: create and activate conda environment
```bash
conda create -n nas --no-default-packages python=3.10
conda activate nas
```
### Step 4: create and activate conda environment
```bash
python install_requirements.py
```

## 