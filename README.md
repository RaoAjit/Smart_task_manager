git clone https://github.com/RaoAjit/Smart_task_manager.git
cd task-analyzer

Create a virtual environment:
python3 -m venv venv
source venv/bin/activate     (Mac/Linux)
venv\Scripts\activate        (Windows)
Install backend dependencies:

Copy code
pip install -r backend/requirements.txt
Apply migrations:



cd backend
python manage.py migrate

Run the server:
python manage.py runserver
The backend will run at:
http://127.0.0.1:8000

Frontend:
Open the file:
frontend/index.html


The Smart Balance algorithm is designed to simulate real-world task prioritization by evaluating each task across four major factors: urgency, importance, effort, and dependency impact. These represent the most common dimensions people consider when deciding what to work on next. The algorithm converts each factor into a score, applies appropriate weighting, and produces a final priority value.

1. Urgency
Urgency is determined by the number of days remaining before the task’s due date. Tasks that are overdue or very near their deadline receive significantly higher priority. This reflects the natural rule that time-sensitive tasks must be addressed quickly. The urgency score is computed as:

urgency = max(0, 20 - days_until_due)


If a task is overdue, the score increases more aggressively:

if days_until_due < 0:
    urgency += abs(days_until_due) * 2


This ensures late tasks move to the top automatically.

2. Importance
Importance is user-defined on a 1–10 scale, representing subjective value. To reflect the typical weight of importance in decision-making, the algorithm multiplies it by 3:

importance_score = importance * 3


This makes important tasks consistently stand out regardless of due date.

3. Effort (Quick Wins)
Lower-effort tasks are often beneficial to complete early because they provide momentum and clear small blockers. The effort score rewards tasks requiring fewer hours:

effort_score = max(1, 10 - estimated_hours)


Tasks requiring more effort are not heavily penalized; they simply don’t benefit from a “quick-win boost.”

4. Dependency Impact
Tasks that block other tasks must be prioritized. The algorithm assigns points for each task that depends on the current one:

dependency_score = 5 * num_dependents


Circular dependencies are detected using a DFS graph traversal and flagged so they cannot distort the score.

Final Scoring Formula

final_score =
 urgency_score * 0.4 +
 importance_score * 0.4 +
 effort_score * 0.1 +
 dependency_score * 0.1


Urgency and importance dominate the calculation, while effort and dependencies provide meaningful support. This produces a balanced ranking across projects with varied requirements.

Design Decisions

Separated scoring logic:
The scoring algorithm is placed in scoring.py to maintain modularity, simplify testing, and allow future extensions such as user-configurable weights or ML-based scoring.

DFS for dependency cycles:
Circular dependencies create invalid task graphs. Using depth-first search ensures these are detected reliably and flagged before scoring.

Clear API boundaries:
The backend handles all scoring and strategy logic so the frontend stays lightweight and maintainable.

Simple, functional frontend:
Focused on correctness and clarity rather than heavy styling. It validates input, sends requests, and presents results with color-coded priority indicators.

Graceful error handling:
Missing fields, invalid dates, and malformed JSON are safely managed to prevent crashes.
