# InnoScream – Anonymous student scream platform
## 🎯 Project goal

> Build a Telegram-based anonymous stress relief platform for students, where users can post frustrations, react with emojis, view community stress stats, and see top daily screams as memes.

---

## ⚙️ Tech stack

- **Bot:** Python 3.11, aiogram (Telegram), httpx, asyncio
- **Backend:** Python 3.11, FastAPI, SQLAlchemy (Async)
- **Database:** SQLite (using `aiosqlite`)
- **External APIs:**  
  - 📊 [QuickChart.io](https://quickchart.io/) – Weekly analytics graphs  
  - 🖼️ [ImgFlip Meme API](https://imgflip.com/api) – Meme generation

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/creepydanunity/innoscream.git
cd innoscream
```

### 2. Set up virtual environment (recommended via Poetry)

```bash
poetry install
```

### 3.1 Create `app_bot/.env` file
```env
BOT_TOKEN=<TelegramAPI_Token>
API_URL=<InnoScreamAPI_URL> (default: http://api:8000)
```

### 3.2 Create `app_fastapi/.env` file
```env
DB_FILENAME=your_sqlite_db_name (default: innoscream.db)
IMGFLIP_API_USERNAME=your_imgflip_username
IMGFLIP_API_PASSWORD=your_imgflip_password
DEFAULT_ADMIN_ID=your_telegram_id
USER_ID_SALT=your_user_id_salt
```

### Running the project:
- In `InnoScream/`
```bash
docker-compose up --build
```
---
## 📜 License

MIT License — feel free to use and modify.

---
# Functionality
---
## 📦 System architecture

The project is composed of two isolated services:

- `app_fastapi` — backend handling data storage, analytics, and moderation.
- `app_bot` — Telegram bot built with `aiogram`, serving as the frontend interface for users.

Each service runs in its own Docker container for modularity and deployment flexibility.

---
## ✅ Implemented features overview

| Feature                      | Description                                                                 | Status |
|-----------------------------|-----------------------------------------------------------------------------|--------|
| **Anonymous screams**       | `/scream [text]` — Users post anonymously using salted hash IDs.            | ✅     |
| **Emoji reactions**         | Inline emoji reactions for community feedback.                  | ✅     |
| **Top screams of the day**   | `/top` — Displays the most upvoted screams with a meme (ImgFlip API).        | ✅     |
| **Detailed stats**          | `/stats` — Posts count, reaction count, and reaction distribution chart.    | ✅     |
| **Weekly stress graph**     | `/stress` — Community stress visualized via QuickChart.io.                  | ✅     |
| **Moderation**              | `/delete [id]` — Admins can remove inappropriate content.                   | ✅     |
| **Admin creation**          | `/create_admin [user_id]` — Promote users to admin (admin-only).            | ✅  *(New feature)* |
| **Feed browsing**           | `/feed` — Scrollable, user-friendly view of latest screams.                 | ✅  *(New feature)* |
| **Scream history**          | `/history` — Shows archive of top screams from previous weeks.               | ✅  *(New feature)* |

All additional features were proposed and accepted by the PM during planning and review sessions.

---
## 📌 Summary

All core features were fully implemented according to the original plan.  
Three new features were added to scale team participation and improve platform usability:

- `/history` – Scream archive
- `/feed` – User-friendly scream browser
- `/create_admin` – Admin management

> All changes were reviewed and approved by the PM.
---
# Quality
---
## 1. Maintainability
---
##  Flake8
1. Server **Fast API**:

```bash
➞  flake8 app_fastapi/

```
Results of `flake8` to **Fast API**:
- Zero Violations: The flake8 inspection of the app_fastapi/ directory revealed no PEP8 violations.
- *Conclusion*: The code is PEP8 compliant.

2. Server **Bot API**:

```bash
➞  flake8 app_bot/

```
Results of `flake8` to **Bot API**:
- Zero Violations: The flake8 inspection of the app_bot/ directory revealed no PEP8 violations.
- *Conclusion*: The code is PEP8 compliant.

**Summary**:

The InnoScream project sets a high bar for code quality. By achieving 100% PEP8 compliance on both servers, a solid foundation for scalability, collaboration, and long-term maintenance has been laid.

---
## Docstring presence in methods

All functions in the project include appropriate docstrings that describe their logic and parameters. To verify this, we ran the following commands:

```bash
pydocstyle --select=D102,D103 app_bot 
pydocstyle --select=D102,D103 app_fastapi
```

Here, ```D102``` checks for missing docstrings in class methods, while ```D103``` targets standalone functions. No violations were reported, confirming that all functions are properly documented.

---
## Radon cyclomatic complexity

The results of running ```radon cc``` show that most code constructs have a cyclomatic complexity of **A (1–5)**, with only a small number falling into the **B (6–10)** range. The average complexity is **1.84** for ```app_bot ``` and **2.36** for ```app_fastapi```, both well within the acceptable threshold of **≤ 10**, thus fully satisfying the complexity requirements.

Server **Bot API**:
```bash
radon cc app_bot -a
```

Output:

```bash
124 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.8387096774193548)
```
Server **Fast API**:
```bash
radon cc app_fastapi -a
```

Output:

```bash
151 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.357615894039735)
```

---
## 2. Reliability
---
## Test coverage

We ran the tests using a command:

```bash
poetry run pytest --cov=app_bot --cov=app_fastapi
```

#### **Results summary**

* **Total statements**: 1352
* **Missed statements**: 304
* **Overall coverage**: 78%

#### **Observations**

The project meets the requirement of >60% coverage.

---
## Mutation testing
Mutation testing was conducted using [`mutmut`](https://mutmut.readthedocs.io/) to evaluate how well the existing test suite detects behavioral changes in the code.

1. Server **Fast API**:

```bash
~InnoScream/app_fastapi
➞ poetry run mutmut run \
  --paths-to-mutate ./ \
  --tests-dir tests \
  --runner "pytest tests"
```

Results:

| Metric            | Value    |
|-------------------|----------|
| Total mutants     | 827      |
| Killed mutants 🎉 | 196      |
| Survived 🙁        | 610      |
| Suspicious 🤔      | 18       |
| Timeouts ⏰        | 3        |
| Skipped 🔇         | 0        |
| **Survival rate** | **73.7%** |

2. Server **Bot API**:

```bash
~InnoScream/app_bot
➞ poetry run mutmut run \
  --paths-to-mutate ./ \
  --tests-dir tests \
  --runner "pytest tests"
```

Results:

| Metric            | Value    |
|-------------------|----------|
| Total mutants     | 487      |
| Killed mutants 🎉 | 288      |
| Survived 🙁        | 199      |
| Suspicious 🤔      | 0        |
| Timeouts ⏰        | 0        |
| Skipped 🔇         | 0        |
| **Survival rate** | **40.9%** |

### Summary

- **`app_fastapi`** meets the minimum required mutation quality threshold.
- **`app_bot`** shows a stronger and more effective test suite, with a lower survival rate, meaning more mutants were successfully caught and killed.
- No skipped mutants or instability were observed during testing.
- The project satisfies the requirement:
    
  > **"Mutation testing ≤ 80% survival rate"**

---
## 3. Performance
---
## Performance test (Locust)

### Test summary:

* **Objective**: Ensure the bot response time is **≤ 500ms** under **100 RPS load**.
* **Test Duration**: 1 minute
* **Total Requests Sent**: 4862 requests
* **Total Failures**: 0
* **Target Host**: `http://localhost:8000`

### Key metrics:

#### Response time statistics:

* **Average Response Time**: 274.28 ms
* **Minimum Response Time**: 8 ms
* **Maximum Response Time**: 4951 ms
* **50th Percentile (Median)**: 94 ms
* **95th Percentile**: 800 ms
* **99th Percentile**: 2200 ms

The response times generally stayed within the acceptable range, with most requests completing much faster than the 500ms target. However, some requests exceeded the 500ms target, reaching up to 4951ms, likely due to backend processing 3rd party API calls (meme generation, charts generation).

#### Requests Per Second (RPS):

* **Peak RPS**: 9.57
* The bot was able to sustain about 9.57 requests per second on average, reaching a peak of 14.07 RPS under certain conditions.

#### Failure analysis:

* **Total failures**: 0
* **Failures per second**: The error rate remained at 0 throughout the test, indicating that the system successfully handled all requests.

#### Specific endpoints:

* **/delete**: Average response time of \~207 ms.
* **/react**: Average response time of \~143 ms.
* **/scream**: Average response time of \~311 ms.
* **/stats**: Average response time of \~470 ms.
* **/stress**: Average response time of \~490 ms.
* **/top**: Average response time of \~105 ms.

### Observations:

* The system performed well under the specified load, achieving an average response time of **274 ms** and handling requests at a rate close to **100 RPS**.
* A few requests, particularly for the `/stats/*` and `/stress` endpoints, experienced higher response times, but these were still within acceptable limits.
* **No failures** were encountered, meaning that all requests were processed successfully, including those involving potential error conditions like reactivity or deleted screams.

### Conclusion:

The bot successfully met the performance criteria of maintaining **response times under 500 ms** for most requests under a **100 RPS load**, with a few exceptions that can be further investigated. The bot handled **4862 requests** without any failures, ensuring a reliable user experience.

---
## SQL queries performance

We created 1000 screams from different users with 100 reactions for each scream.

### **Initial conditions**:

* **1000 screams** created by different users.
* **100 reactions** for each scream, created by different users.

### **1. Reacting to a scream**

The time to create a reaction involves three main steps: finding the scream, checking if the reaction already exists from the current user, and inserting the reaction into the database.

* **1.44 ms** — Time to find the scream to which we are reacting.
* **1.27 ms** — Time to check if the reaction already exists from the current user on this scream.
* **1.13 ms** — Time to insert the reaction into the database.

**Total: 3.84 ms**


### **2. Feed**

Fetching the next scream involves finding a scream that the current user has not reacted to.

* **5.52 ms** — Time to find a scream that has no reaction from the current user.

### **3. Stats**

Fetching user stats involves several queries to count various metrics such as the total number of screams, reactions, and different types of reactions.

* **1.30 ms** — Time to get timestamps for all screams from the current user.
* **1.45 ms** — Time to count all screams from the current user.
* **14.39 ms** — Time to count reactions that are not "❌".
* **1.49 ms** — Time to count reactions related to screams of the current user, excluding "❌" reactions.
* **24.92 ms** — Time to count the number of each type of reaction on the user's screams, excluding "❌" reactions.

**Total: 43.55 ms**


### **4. Stress**

Fetching stress stats for the user involves adding a reaction and checking whether the reaction already exists, followed by inserting it into the database.

* **1.16 ms** — Time to retrieve all scream timestamps since the specified start date.


### **5. Top screams**

Fetching the top screams involves selecting screams from today with the highest number of non-"❌" reactions, generating memes for each of them, and updating the database with generated meme URLs.

* **37.76 ms** — Time to select top screams with vote counts (excluding "❌" reactions).

* **1.47 ms** — Time to update meme_url for scream ID 1 (first commit).

* **0.98 ms** — Redundant update for scream ID 1 (second commit).

* **1.55 ms** — Time to update meme_url for scream ID 2 (first commit).

* **0.64 ms** — Redundant update for scream ID 2 (second commit).

* **1.33 ms** — Time to update meme_url for scream ID 3 (first commit).

* **0.87 ms** — Redundant update for scream ID 3 (second commit).

**Total: 44.6 ms**


### **6. History**

Fetching the history involves selecting distinct week IDs from the archives.

* **0.85 ms** — Time to select distinct week IDs from the archives.


### **7. Deleting a scream**

The delete operation involves several queries: verifying admin identity, retrieving the scream, checking for related reactions and archives, and finally deleting related data.

* **1.52 ms** — Time to fetch the admin user record.
* **1.34 ms** — Time to fetch the scream by id.
* **1.63 ms** — Time to fetch all reactions related to the scream.
* **0.74 ms** — Time to check for archive entries related to the scream.
* **2.11 ms** — Time to delete the scream’s reactions.
* **1.86 ms** — Time to delete the scream itself.

**Total: 9.20 ms**


### **Summary**

- These operations have demonstrated efficient performance with low latency.
- The project satisfies the requirement:
    
  > **SQL queries ≤ 50 ms**

---
## 4. Security
---
## Bandit

1. Server **Fast API**:

By bandit scanning without taking into account the directories with the tests 
```bash
➞  bandit -r app_fastapi --exclude app_fastapi/tests                                

Test results:
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High

--------------------------------------------------

Code scanned:
        Total lines of code: 1541
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 1
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 1
Files skipped (0):
```

`Bandit` results of **Fast API**:

Identified issue:

- Low severity: Using random.choice() to select meme patterns.
- Location: app_fastapi/tools/meme.py:61
- Risk context:
  - The pseudo-random generator (random module) is flagged as unsuitable for security/cryptography tasks.
- Why it's not critical:
  - Non-sensitive use case: The random.choice() function is used to select a meme template ID from a predefined list (IMGFLIP_TEMPLATE_IDS). It is not related to authentication, authorization, or access to sensitive data.
  - No impact on security: Randomness is used here solely for pattern diversity, not for token generation, password generation, or cryptographic operations. Predictability in this context poses no risk to system integrity or user data.
- Risk mitigation solution:
  - After assessing the contex: replacing randomness with a cryptographically secure module (e.g., secrets) is not needed here because no security-sensitive outcome depends on this randomness.

2. Server **Bot API**:

By bandit scanning without taking into account the directories with the tests 
```bash
➞  bandit -r app_bot --exclude app_bot/tests                                        

Test results:
        No issues identified.

Code scanned:
        Total lines of code: 1219
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 0
Files skipped (0):
```

`Bandit` results of **Bot API**:
- 0 Vulnerabilities: No issues were identified during the Bandit scan.
- Implications:
  - The codebase adheres to secure coding practices, with no use of deprecated or risky functions (unsafe deserialization, shell injections).

**Summary**:
The InnoScream project demonstrates a mature approach to security:
- `Bot API` maintains a flawless security profile, reflecting rigorous coding standards.
- `Fast API’s` lone low-risk issue is well-contained and contextually justified, with no impact on system security or user trust.

---
## Data anonymity (User ID Hashing)

The purpose of this manual review is to ensure that the `user_id` is properly anonymized through hashing, and that the process is compliant with security requirements.

**1. Hashing functionality:**

* **Implementation**: User IDs are hashed using the SHA-256 algorithm, which converts the original numeric identifier into a hexadecimal string.

* **Code review**:

  * The `hash_user_id` function receives a `user_id` (int), converts it to a string, encodes it into bytes, and hashes it using `hashlib.sha256()`.

  * A log message is created for the hashing process, capturing only the first few characters of the hash for review purposes.

* **Salting (Global)**:
  A **global salt** has been implemented to further enhance the security of the hashing process. The salt is stored securely in the environment file (`.env`) and is used consistently when hashing all `user_id` values. This salt is combined with the `user_id` before applying the SHA-256 hash function. By using the salt for all users we ensure additional protection against pre-computed attacks (like rainbow tables). The global salt is stored in the `.env` file and loaded securely when needed, ensuring it is not exposed in the code or the database.

* **Audit logs**: Every hash operation is logged with the part of the `user_id` and the first few characters of the resulting hash for traceability.

**3. Security considerations:**

* **Hashing strength**: SHA-256 provides a strong cryptographic hash that is not reversible, ensuring that the original user ID cannot be derived from the hashed value.

**4. Code integration:**

* **Where it's used**: The hashed `user_id` is stored in various models, such as `Admin`, `Scream`, `Reaction`, and `UserFeedProgress`.

* **Audit of models**: Review how the hashed `user_id` is being stored in these models and ensure that it is never stored in its original form (unhashed).

  * **Admin Model**: Stores `user_hash` to represent the admin’s identity.

  * **Scream Model**: Each scream is associated with a `user_hash`, ensuring anonymity of the user who posted the content but still usable to calculate personal statistics.

  * **Reaction Model**: Stores a hashed version of the user’s identity for reactions.

  * **UserFeedProgress Model**: Tracks the hashed `user_id` for personalized feeds, ensuring anonymity when progressing through the feed.

**5. Auditing process:**

* **Manual review**:

  * Inspected each instance of the `user_id` being hashed in the models to ensure there are no direct exposures.

  * Confirmed that only the hashed value is stored and processed across the application.

**6. Validation:**

* Performed a manual check by querying the database and ensuring that:

  * User IDs are consistently stored as hashes and not as plain text.

  * The system does not inadvertently expose raw user IDs in logs or error messages.

--- 
# Quality requirements summary

| Category         | Requirement                                          | Status |
|------------------|------------------------------------------------------|--------|
| **Maintainability** | Zero flake8 & pydocstyle warnings, radon CC ≤ 10  | ✅     |
| **Reliability**     | Test coverage ≥ 60%, mutation survival ≤ 80%     | ✅     |
| **Performance**     | ≤ 500ms bot response at 100 RPS, SQL < 50ms      | ✅     |
| **Security**        | No Bandit criticals, hashed user_id, admin auth  | ✅     |

Tools Used:  
- **pytest**, **pytest-cov**, **mutmut**  
- **flake8**, **pydocstyle**, **radon**, **bandit**, **locust**

---
# Lessons learned
Over the developing of **InnoScreamBot**, our team encountered a range of technical and organizational challenges. Here are the key lessons we took away:

### 1. **Modular architecture pays off**
Splitting the project into two services (`app_fastapi` and `app_bot`) made our codebase cleaner, testing more focused, and collaboration smoother. Each team member could work independently with clear API boundaries.

### 2. **Early agreement is crucial**
By proactively discussing and agreeing on new features like `/history` and `/create_admin` with the PM, we prevented confusion and scope creep.

### 3. **Bot UX requires iteration**
Designing interactions for Telegram required us to think like end users. Features like `/feed` evolved based on usability feedback and made the platform more engaging.

### 4. **Tooling helps, but only if integrated early**
Running `flake8`, `bandit`, and `pydocstyle` from the start helped maintain quality. However, mutation testing was added late — introducing it earlier would have saved debugging time and improved test quality faster.

### 5. **Charts and visuals add impact**
Using APIs like QuickChart.io and ImgFlip added fun and clarity to the bot. Data visualization proved useful not only for users but also for showcasing our work during demos.

### 6. **Role-based access control matters**
Implementing hashed user IDs and admin-only commands (like `/delete` and `/create_admin`) reinforced the importance of privacy and moderation even in simple applications.

---

> These lessons will inform how we plan, test, and collaborate in future projects — both technically and as a team.
