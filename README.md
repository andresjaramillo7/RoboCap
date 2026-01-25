# RoboCap: Natural Language Scene Descriptions for Robots
System that generates natural language descriptions from images of "what a robot sees". (CV => NLP)

This idea aligns with real robotics applications such as assistance robots, autonomous navigation, and systems that need to interpret their environment in a way that is understandable to humans.

COCO's dataset and a multimodal CV + NLP pipeline (Conv Network + Transformer) its used to train, validate and test the deep learning algorithm's model.



## Motivation:
Robots often perceive their environment through cameras, but lack the ability to summarize visual information in language.

Natural-language descriptions give robots:
- Human friendly explanations of what they see.
- Context for decision making.
- Improved interpretability in assistive or domestic settings.
- A bridge between vision and communication.

The system aims to demonstrate how image captioning can serve as a foundational module for robot awareness.



## Expected Outcomes of the project (Before development):
Demo 1:
- Generate readable captions from unseen images. Giving the nearest (most similar) caption stored in the train dataset to the embedding given by the transformer model.

Demo 2:
- Generate readable captions from unseen images, using LLMs to create text from the final embedding given by the transformer model.
- Highlight actions and objects relevant to robot navigation.



## Dataset:
As it was established, the COCO (Common Objects in Context) dataset has been used to train, validate and test the project.

Images folders names:
- 2017 Train images [118k/18GB]
- 2017 Val images [5k/1GB]
- 2017 Test images [41k/6GB]

Annotations .json file names:
- 2017 Train/Val annotations [241MB]

Source Link: https://cocodataset.org/#download

## Data Preparation:
To train the model, you must download the [COCO 2017 Dataset](https://cocodataset.org/#download).

Ideally, the following content:
- 2017 Train images [118k/18GB]
- 2017 Val images [5k/1GB]
- 2017 Train/Val annotations [241MB]

And store it in the stablished following directories with the stablished names:

```text
/raw_data
├── /annotations        # Place downloaded .json files
├── /images
│   ├── /train2017      # Place training images
│   └── /val2017        # Place validation images
└── /pt_files
```


## Installation, Setup and Run project
Follow these steps to prepare the data, setup the environment and train the model, in order to run **RoboCap.**

#
### 1. Setup Environment
Open a terminal in your project root. Its strongly recommend using a **virtual environment**.

1. **Create and Activate Virtual Environment:**

    ```bash
    # Create the virtual environment
    python -m venv .venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on Mac/Linux
    source venv/bin/activate
    ```

2. **Pre-requisite: Install NVIDIA CUDA Toolkit:**

    Before installing PyTorch, ensure your machine has the correct CUDA Toolkit installed to support GPU acceleration.
    * **Download Toolkit:**
    
    Visit the NVIDIA CUDA Toolkit Archive: [https://developer.nvidia.com/cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive) and install the version matching your system.

3. **Install PyTorch with CUDA:**

    Visit [pytorch.org](https://pytorch.org/get-started/locally/) and copy the install command for your **Compute Platform** (CUDA version).
    
    Example for CUDA 11.8:
    ```bash
    python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    ```

4. **Install Remaining Dependencies:**

    ```bash
    python -m pip install -r requirements.txt
    ```

#
### 2. Preprocessing data & Training
*Note: Its strongly recommend using a GPU with **CUDA** support for generating embeddings and training the model.*

1. **Generate Embeddings:**
    Open `notebooks/RoboCap_Lab.ipynb` and run all cells to process the images and captions. This will generate `.pt` files (caption embeddings and image logits) and save them into the `/raw_data/pt_files` directory.

2. **Train the Model:**
    Open `notebooks/RoboCap_Encoding.ipynb` and run all cells to train the fine-tuned Transformer (BERT) model.


#
### 3. Setup and run Backend

 On the main directory; Run the server on host `0.0.0.0` so it is accessible by your mobile device:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```


# 
### 4. Setup and run Frontend
Open a new terminal window and navigate to the frontend directory:
```bash
cd frontend/RoboCapFrontend
```
And follow the next steps:

1. **Configure Network IP:**

    To allow the mobile app to communicate with your computer, you must update the API configuration.
    
    - Run `ipconfig` (Windows/Mac/Linux) in your terminal to find your computer's **IPv4 Address** (e.g., `192.168.1.87`).
    ```bash
    ipconfig
    # Output: Local Network Information
    ```
    - Open the file `config.ts` ubicated in frontend/RoboCapFrontend/scr/ 
    ```text
    /frontend
    ├── /RoboCapFrontend
        ├── ...     
        ├── /scr
            ├──...
            ├── /config.ts      # Open this file
    ```
    
    - And update the `API_BASE_URL`:
    ```typescript
    // config.ts
    export const API_BASE_URL = "http://<YOUR_IPV4_ADDRESS>:8000"; 
    ```

2. **Install & Run:**
    ```bash
    # Install dependecies
    npm install
    # Run frontend
    npx expo start -c
    ```
#
### 5. Usage
1. **Download Expo Go in your phone:**
    - Install the **Expo Go** app on your mobile device.

    *Note: (Tested on iPhone 12 and 13).*

2. **Connect phone and project:**
    - Scan the QR code displayed in your terminal with the Expo Go app.

3. **Use RoboCap:**
    - Take a picture or load one from your phone gallery.
    - Wait **20 - 30 seconds**...
    - A Caption has been generated!!



## Project developed by:
- Andrés Jaramillo Barón | A01029079
- Pedro Mauri Martínez | A01029143
