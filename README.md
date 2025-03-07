# Backend-Exercise
# 📄 PubMed Research Paper Fetcher  

## 🚀 Overview  
This fetches research papers from **PubMed**, filters authors based on **company affiliations**, and exports the results as a **CSV file** or prints them to the console.  

## 🛠️ Features  
✅ Fetches research papers from **PubMed** using a search query.  
✅ Identifies **non-academic authors** affiliated with **pharma/biotech** companies.  
✅ Extracts **title, author affiliations, corresponding email, and PubMed ID**.  
✅ Saves results as a **CSV file** or prints them in the **console**.  
✅ Includes **debug mode (`--debug`)** for troubleshooting.  
✅ **Poetry-based dependency management** and an **executable command** (`get-papers-list`).  

---

## ⚙️ Installation  

### **1️. Clone the Repository**
```sh
git clone https://github.com/yourusername/backend-exercise.git
cd backend-exercise

## **2. Run the command**

pip install poetry

poetry install

poetry env use python3
poetry env activate

poetry run get-papers-list "biotechnology" -> prints the output in the console

poetry run get-papers-list "biotechnology" --file "path/to/your/file" -> Saves the content in the csv file

