# K-Pg Impact Winter Model

This is a coupled climate model in Python that compares to Bardeen et al. 2017 and Brugger et al. 2017. It strives to answer the question, to what extent did the asteroid impact from the Cretaceous-Paleogene boundary event (K-Pg event) impact ecosystems? 

Link to app: https://02120-project-project.vercel.app/ 

## Organization
- simulation/ holds the code for the model
- website/ holds the code for the website 
- data/ holds the PDFS of the research papers
- misc/ holds other stuff pertaining to this assignment, like the proposal

## How to run this model
- cd project/simulation and run "python main.py"
- then cd project/website and run "python export_data.py" and "python -m http.server 8000" and open with http://localhost:8000