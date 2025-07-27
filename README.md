# Clustra

**Clustra** is a face clustering software designed to efficiently organize and manage large collections of images. It automatically detects faces within photographs and groups them, allowing users to easily download pictures based on specific individuals.

This functionality is particularly beneficial for:

- **Photographers**: Streamlines the process of separating individuals from numerous group pictures, significantly reducing manual sorting time.
- **Friends and Casual Users**: Eliminates the tedious task of manually sorting photos after events or trips, enabling quick sharing and enjoyment of memories.

---

## ⚠️ Important Note on Compute Power

Clustra is computationally intensive. Due to the significant processing requirements, the application is split into a **frontend** and a **backend** component:

- **Frontend**: Deployed on [Vercel](https://vercel.com) for easy access and distribution.
- **Backend**: Handles the heavy-lifting computational tasks and is designed to run **locally** on your machine.

> This approach overcomes limitations of cloud platforms for a fully serverless solution.

Efforts are currently underway to integrate with **Azure API** to achieve a **fully serverless architecture**, eliminating the need for local backend hosting.

---

## 🚀 Performance and Accuracy

Clustra boasts **high accuracy** in face detection and clustering, though some **false positives** may occur.  
Each image takes approximately **0.5 to 1 second** to process, making it an efficient solution for large photo libraries that require quick grouping and sharing.

---

## 🛠️ Project Status

Clustra is currently a **work in progress**, but its core feature of easy, automated photo grouping is **fully functional**.  
Future plans include transitioning to a **fully dataless web service**, depending on:

- Improved cloud platform performance
- Availability of better free APIs for face detection

---

## 🧑‍💻 Getting Started (Backend Setup)

### ✅ Prerequisites

- **Python 3.10** is highly recommended for optimal stability and compatibility.  
  [Download Python here](https://www.python.org/downloads/)

---

### 📦 Installation and Running

#### 1. Clone the Repository

```bash
git clone https://github.com/AdityaPatel18/Clustra
cd Clustra
```
## 2. Install Dependencies using pip

Navigate to the project root directory (where requirements.txt is located) and install all necessary Python packages.
It's recommended to do this within a virtual environment:

```bash
pip install -r requirements.txt
```

## 3. Run the Backend Server

Once the dependencies are installed, you can start the backend server.
This command will make the backend accessible on your local network on port 3001.

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 3001
```

## 4. Connect Frontend to Backend

After the backend is running, ensure you reload [Clustra webpage](https://clustra.vercel.app) until the warning on top is no longer visible:

## 💡 Suggestions / Feedback

We welcome your ideas, feedback, and criticism!

* 💬 Found a bug or have a feature request? Open an issue

Thanks for checking out **Clustra**! ⭐
