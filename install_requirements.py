import subprocess
from typing import Union, List


def pip_install_packages(packages: List[str], index_url: Union[str, None] = None):
    for package in packages:
        try:
            print(f"Installing {package}...")
            command = ["pip", "install"]
            # add package name
            command.append(package)

            if index_url:
                command.extend(["--extra-index-url", index_url])

            result = subprocess.run(command, capture_output=True, text=True)

            # print result
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            print(f"!!! Failed to install {package}: {e}")
    return


def install_torch():
    packages = ["torch==2.1.0", "torchvision==0.16.0", "xformers==0.0.22.post7+cu118"]
    index_url = "https://download.pytorch.org/whl/cu118"
    pip_install_packages(packages=packages, index_url=index_url)


def install_streamDiffusion():
    packages = ["streamdiffusion[tensorrt]"]
    pip_install_packages(packages=packages)

    print("Installing TensorRT extensions")
    result = subprocess.run(
        ["python", "-m", "streamdiffusion.tools.install-tensorrt"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)

def install_required_packages():
    packages = [
        "ninja==1.11.1.1",
        "spleeter==2.4.0",
        "fastapi==0.110.1",
        "websockets==12.0",
        "uvicorn == 0.29.0",
        "sounddevice==0.4.6",
        "librosa==0.10.1",
        "mediapipe==0.10.14",
        "tinytag==1.10.1",
        "PyYAML==6.0.1",
        "scikit-learn==1.4.2",
        "scipy==1.13.0",
        "uuid==1.30",
        "numpy==1.26.3",
        "numba==0.59.1",
        "opencv-contrib-python==4.9.0.80",
        "opencv-python==4.9.0.80",
        "protobuf==3.20.0"]

    pip_install_packages(packages=packages)


if __name__ == "__main__":
    install_torch()
    install_streamDiffusion()
    install_required_packages()
