# SkillsBridge SA

**SkillsBridge SA** is an AI-assisted career-readiness prototype designed to help South African graduates and entry-level job seekers compare their current skills with the skills mentioned in a job description. It highlights detected overlap, points out skills to explore, and provides links to learning resources.

## Project purpose

Many early-career job seekers see job adverts asking for skills they are unsure how to interpret or prioritise. SkillsBridge SA turns a job description into a more actionable skills comparison and learning starting point.

## Features

- Responsive, dark editorial interface using a consistent forest-green, ivory, and lime palette.
- Candidate profile, target-role, current-skills, and job-description form.
- Natural-language phrase matching against a curated catalogue of common digital skills.
- Indicative skills-overlap score, matched skills, missing skills, and additional detected skills.
- Suggested learning resources for skills to explore.
- Local SQLite history of the latest 25 analyses.
- Print-friendly report layout so a user can save the report as a PDF from the browser.
- Basic form validation, error pages, and a `/health` status endpoint.
- No external AI API key required for the prototype.

## Technology stack

- Python
- Flask
- HTML5 and Jinja templates
- CSS
- JavaScript
- SQLite

## Requirements

- Python 3.10 or later recommended
- pip
- Visual Studio Code or another code editor
- A modern web browser

## Setup on Windows (PowerShell)

1. Open this project folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

4. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run the following in that terminal session and activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

6. Start the application:

   ```powershell
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

To stop the local server, return to the terminal and press **Ctrl+C**.

## How to use the application

1. Enter a name or demo name.
2. Choose a target career.
3. Optionally enter a job title.
4. List skills and experience you currently have. Include technical skills, tools, coursework, and projects in plain language.
5. Paste the requirements and responsibilities from a job advert into the job-description field.
6. Select **Analyse my skills**.
7. Review the match score, skills found in both inputs, skills to explore, and suggested learning links.
8. Open **Recent analyses** to see the latest saved reports.

For a useful result, paste a detailed job advert that explicitly mentions relevant skills. The catalogue is intentionally limited to common entry-level digital skills and can be expanded.

## How the analysis works

SkillsBridge SA uses a transparent, rule-based natural-language phrase-matching approach. It normalises text, checks for known skill names and synonyms, and compares the detected skills in the candidate input with those found in the job description.

The indicative score is:

`matched detected job skills / total detected job skills × 100`

If the pasted job description contains no recognisable catalogue skills, the app uses a starter skill profile for the selected target role and labels the report to make that fallback clear.

This is an explainable AI-assisted prototype rather than a trained machine-learning model or a generative-AI service. It does not semantically understand every sentence, evaluate proficiency, verify qualifications, or predict hiring outcomes. A future version could add a trained NLP model, semantic similarity, real opportunity feeds, user accounts, and richer learning recommendations.

## Project structure

```text
SkillsBridge-SA/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── history.html
│   └── error.html
└── static/
    ├── style.css
    └── script.js
```

The `venv/` folder and `skillsbridge.db` database are created locally and excluded from version control.

## Routes

- `/` — main form and skills analysis
- `/history` — latest local analyses
- `/health` — simple JSON health status

## Testing checklist

- [ ] Home page opens without a Flask error.
- [ ] Submitting an incomplete form displays a validation message.
- [ ] Submitting current skills and a detailed job description shows a results page.
- [ ] The report shows matched skills, missing skills, and an indicative score.
- [ ] Learning-resource links open in a new browser tab.
- [ ] The history page records completed analyses.
- [ ] `/health` returns JSON with `"status": "ok"`.
- [ ] The layout remains usable at desktop and mobile widths.

## Privacy and responsible use

This is a local demonstration application, not a production recruitment service. Analyses are stored in a local SQLite database on the machine running the app. Use demo names and avoid entering ID numbers, contact details, CVs containing sensitive personal information, or other confidential data. The prototype does not transmit the analysis to a third-party AI provider.

The score must not be used as a hiring decision. It measures catalogue overlap only; a candidate may have a skill without mentioning it, and a job advert may contain requirements not represented in the catalogue.

## Known limitations

- Skill recognition depends on the included catalogue and synonyms.
- The match score does not measure proficiency or years of experience.
- Some job descriptions use unfamiliar wording or abbreviations that may not be detected.
- Learning links are curated suggestions, not a guarantee of a particular qualification.
- The app has no authentication or multi-user separation and is intended for local demonstration.
- Flask debug mode is enabled for local development only; do not deploy this configuration publicly.

## Future improvements

- Add semantic similarity or a trained NLP model.
- Expand the South African entry-level skill and role catalogue.
- Add CV parsing with explicit user consent and privacy controls.
- Add user accounts and private progress tracking.
- Integrate verified job and learnership listings.
- Add tests for skill detection, scoring, validation, and database storage.

## Author

**Tshepo Tleane**  
Systems Development portfolio project

## Licence

This project is provided for educational and portfolio demonstration purposes. Check the terms of any third-party learning resources linked from the application before redistributing their content.
