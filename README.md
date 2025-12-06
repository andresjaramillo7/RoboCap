# RoboCap: Natural Language Scene Descriptions for Robots

System that generates natural language descriptions from images of "what a robot sees". (CV => NLP)

This idea aligns with real robotics applications such as assistance robots, autonomous navigation, and systems that need to interpret their environment in a way that is understandable to humans.

COCO dataset and a multimodal CV + NLP pipeline its used to train, validate and test the models.

## Motivation:
Robots often perceive their enviroment through cameras, but lack the ability to summarize visual information in language.

Natural-language descriptions give robots:
- Human friendly explanations of what they see.
- Context for decision making.
- Improved interpretability in assistive or domestic settings.
- A bridge between vision and communication.

The system aims to demonstrate how image captioning can serve as a foundational module for robot awareness.

## Dataset:
As it was established, the sysytem uses the COCO dataset (Common Objects in Context), which contains:
- 118k training images.
- 5k validation images.
- 5 captions per image.

Source Link: https://cocodataset.org/#download

## Expected Outcomes of the project (Before development):
By the end of the project, the system RoboCap will:
- Generate readable captions from unseen images.
- Highlight actions and objects relevant to robot navigation.

## Installation & Setup

Follow these steps to set up the environment, prepare the data, and run the **RoboCap** application.

### 1. Data Preparation
To train the model, you must download the [COCO 2017 Dataset](https://cocodataset.org/#download). Specifically, you need:
* 2017 Train images
* 2017 Val images
* 2017 Train/Val annotations

Create a directory named `raw_data` in the root of your project and structure your files exactly as shown below:

```text
/raw_data
├── /images
│   ├── /train2017       # Place training images here
│   └── /val2017         # Place validation images here
├── /annotations         # Place downloaded .json annotations here
└── /pt_files            # Create this empty folder for output tensors
```

### 2. Preprocessing & Training
*Note: We strongly recommend using a GPU with **CUDA** support for generating embeddings and training the model.*

1.  **Generate Embeddings:**
    Open `notebooks/RoboCap_Lab.ipynb`. Run all cells to process the images and captions. This will generate `.pt` files (caption embeddings and image logits) and save them into the `/raw_data/pt_files` directory you created earlier.

2.  **Train the Model:**
    Create a new directory named `/results` in your project root (this is where model checkpoints will be saved).
    Open `notebooks/RoboCap_Encoding.ipynb` and run the notebook to fine-tune the BERT model.

### 3. Backend & Environment Setup
Open a terminal in your project root. We strongly recommend using a **virtual environment**.

1.  **Create and Activate Virtual Environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\activate

    # Activate on Mac/Linux
    source venv/bin/activate
    ```

2.  **Prerequisite: Install NVIDIA CUDA Toolkit:**
    Before installing PyTorch, ensure your machine has the correct CUDA Toolkit installed to support GPU acceleration.
    * **Download Toolkit:** Visit the [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive) and install the version matching your system (e.g., 11.8).

3.  **Install PyTorch with CUDA:**
    Visit [pytorch.org](https://pytorch.org/get-started/locally/) and copy the install command for your **Compute Platform** (CUDA version). Example for CUDA 11.8:
    ```bash
    pip install torch torchvision --index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)
    ```

4.  **Install Remaining Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Backend:**
    Run the server on host `0.0.0.0` so it is accessible by your mobile device:
    ```bash
    uvicorn api.main:app --host 0.0.0.0 --port 8000
    ```

### 4. Frontend Setup
Open a new terminal window and navigate to the frontend directory:
```bash
cd frontend/RoboCapFrontend
```

1.  **Configure Network IP:**
    To allow the mobile app to communicate with your computer, you must update the API configuration.
    * Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux) in your terminal to find your computer's **IPv4 Address** (e.g., `192.168.1.87`).
    * Open the file `config.ts` and update the `API_BASE_URL`:
        ```typescript
        // config.ts
        export const API_BASE_URL = "http://<YOUR_IPV4_ADDRESS>:8000"; 
        ```

2.  **Install & Run:**
    ```bash
    npm install
    npx expo start -c
    ```

### 5. Usage
1.  **Download Expo Go:** Install the **Expo Go** app on your mobile device (Tested on iPhone 13).
2.  **Connect:** Scan the QR code displayed in your terminal with the Expo Go app.
3.  **Run RoboCap:** Take a picture using the app interface.
4.  **Wait:** The model typically takes **20 - 30 seconds** to process the image and generate a caption.

# Project developed by:
- Andrés Jaramillo Barón | A01029079
- Pedro Mauri Martínez | A01029143
