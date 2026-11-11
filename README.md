# CSC 309: Artificial Intelligence — course code

Programs for the **CSC 309 Artificial Intelligence** lecture note,
Department of Computer Science, Faculty of Computing, Rivers State
University, Port Harcourt.

**Authors:** Dr. Goodnews Ogboada Jaja and Professor Vincent Ike-Emeka Anireh

Every program is complete, tested and ready to run. There is one folder per
unit of the course; each folder has a README that lists its programs.
Most are in Python 3; Unit 14 also has Prolog and Lisp.

| Unit | Folder | Topic | Programs |
|---|---|---|---|
| 1 | [u01-introduction](u01-introduction) | Introduction to Artificial Intelligence | 2 |
| 2 | [u02-turing](u02-turing) | The Turing Test and the Chinese Room | 2 |
| 3 | [u03-agents](u03-agents) | Intelligent Agents and Their Environments | 1 |
| 4 | [u04-architectures](u04-architectures) | Agent Architectures, Multi-Agent Systems and Robots | 5 |
| 5 | [u05-problems](u05-problems) | Problems, Problem Solving and AI Structures | 2 |
| 6 | [u06-uninformed](u06-uninformed) | Uninformed Search | 4 |
| 7 | [u07-heuristic](u07-heuristic) | Heuristic Search, Local Search and Games | 5 |
| 8 | [u08-kr](u08-kr) | Knowledge Representation and Reasoning | 3 |
| 9 | [u09-semnet-frames](u09-semnet-frames) | Semantic Networks and Frames | 2 |
| 10 | [u10-logic](u10-logic) | Predicate Logic and Resolution | 2 |
| 11 | [u11-nlp](u11-nlp) | Natural Language Understanding | 2 |
| 12 | [u12-nlp-apps](u12-nlp-apps) | Applications of Natural Language Processing | 7 |
| 13 | [u13-expert](u13-expert) | Expert Systems | 2 |
| 14 | [u14-languages](u14-languages) | Programming Languages for AI | 3 |
| 15 | [u15-vision](u15-vision) | Introduction to Computer Image Recognition | 3 |

## 1. Get your own copy: fork, then clone

1. Sign in to GitHub (create a free account at github.com if you have none).
2. Open https://github.com/goodnewso/csc309-artificial-intelligence and click
   **Fork**, then **Create fork**. Your copy is at
   `https://github.com/YOUR-USERNAME/csc309-artificial-intelligence`.
3. Clone **your fork** to your computer:

       git clone https://github.com/YOUR-USERNAME/csc309-artificial-intelligence.git
       cd csc309-artificial-intelligence

No GitHub account? Click **Code → Download ZIP** on the repository page.

## 2. Install Python and the libraries

You need Python 3.10 or later. In the repository folder:

    python -m venv .venv
    source .venv/bin/activate          # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

For Unit 14, install SWI-Prolog (swi-prolog.org) and, optionally, SBCL
(sbcl.org), then run `swipl -q -g main -t halt courses.pl` and
`sbcl --script courses.lisp` in `u14-languages`.

## 3. Run the programs

    cd u06-uninformed
    python solve_mc.py

Check everything at once from the top folder: `python tests/run_all.py`.
Programs that use random numbers fix the seed, so you see the same results
as your classmates. Figures and animations are saved in a `figures/`
folder beside the program.

## 4. No computer? Use Kaggle or Google Colab

Open a new notebook on kaggle.com (switch **Internet** on) or
colab.research.google.com and run in a cell:

    !git clone https://github.com/goodnewso/csc309-artificial-intelligence.git
    %cd csc309-artificial-intelligence/u07-heuristic
    !python puzzle8.py

## 5. Keep your fork up to date, and save your work

New programs are added during the semester. On your fork's GitHub page click
**Sync fork → Update branch**, then `git pull` on your computer.
Do each laboratory on its own branch:

    git checkout -b lab06
    git add u06-uninformed/my_search.py
    git commit -m "Lab 6: my own search problem"
    git push -u origin lab06

Found a mistake? Open an **Issue**, or send a **Pull Request** from your fork.

## Licence

The code is released under the MIT licence (see [LICENSE](LICENSE)).
The lecture note and the textbook are not covered by this licence.
