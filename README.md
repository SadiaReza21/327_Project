# Bazar Kori – The Best E-commerce Project in CSE327 (2025)

<p align="center">
  <img src="https://github.com/SadiaReza21/327_Project/blob/emu/assests/Bazar.png" alt="Bazar Kori"/>
</p>

<p align="center">
  <strong>FastAPI • Pydantic v2 • Full Testing • Beautiful UI • Sphinx Docs </strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic"/>
  <img src="https://img.shields.io/badge/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge" alt="Ruff"/>
  <img src="https://img.shields.io/badge/tests-34%20passed-2ea44f?style=for-the-badge" alt="Tests"/>
  
</p>

<p align="center">
  <strong>Submitted: December 03, 2025</strong>
</p>

---

##  Live Demo of the features

| Search Page                                       | Filter Page                                         | Extended Filter                                       |
| ----------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| ![Home](https://github.com/SadiaReza21/327_Project/blob/emu/assests/home.png) | ![Filter](https://github.com/SadiaReza21/327_Project/blob/emu/assests/filter.png) | ![EX-Filter](https://github.com/SadiaReza21/327_Project/blob/emu/assests/search.png) |

---

##  Features used in these modules

* FastAPI backend with async support
* Full-text search (case-insensitive + partial match)
* Filtering: category, price range, stock, sorting, pagination
* Responsive HTML filter page at `/filter`
* Automatic Swagger & ReDoc (`/docs` & `/redoc`)
* Pytest Cases (all passed successfully)
* Sphinx documentation (ReadTheDocs theme)
* Clean MVC architecture
* Bugs fixed, full validation with Pydantic v2

---

## Quick Start- How to install: 

```bash
git clone https://github.com/yourusername/bazar-kori.git
cd bazar-kori

python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

Now open:

```
Home: http://127.0.0.1:8000
Filter Page: http://127.0.0.1:8000/filter
Swagger UI: http://127.0.0.1:8000/docs
```

---

## Run Tests 

```bash
python tests/run_tests.py
```

You will see:

```
ALL TESTS PASSED SUCCESSFULLY!
```

---

## View organized Documentation

```bash
cd docs && make html && open build/html/index.html
```


## Tech Stack Used

**FastAPI • Pydantic v2 • Jinja2 • Uvicorn • pytest • Sphinx • Ruff • ReadTheDocs Theme**



### Author Information

**Name:** [Yasmin Sultana Emu]
**ID:** [2212253642]

---