# AI Resume Analyzer

A privacy-conscious Streamlit app that compares a resume with a job description, explains the match score, identifies skill gaps, suggests improvements, creates interview questions, and exports a report.

The app works locally without an API key. If `OPENAI_API_KEY` is configured, it adds richer feedback through the OpenAI Responses API and falls back to deterministic local recommendations if the request fails.

## Features

- Parse text-based PDF, DOCX, and TXT resumes
- Load a sample job or paste a custom job description
- Extract skills through an editable, explainable catalog
- Score skills, keywords, experience, education, and resume structure
- Show matched, missing, and additional skills
- Generate resume recommendations and interview questions
- Optionally enhance feedback with OpenAI
- Export PDF and JSON reports
- Run a focused automated test suite

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Optional AI feedback

Set your key and preferred model in `.env`:

```dotenv
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5-mini
```

Keep `.env` private; it is ignored by Git. The integration uses the official Python SDK and `client.responses.create(...)`, following the [OpenAI API quickstart](https://developers.openai.com/api/docs/quickstart). Requests set `store=False`.

## Run tests

```bash
pytest -q
```

## Scoring model

| Signal | Weight | Method |
|---|---:|---|
| Skills | 45% | Canonical skill coverage |
| Keywords | 20% | Keyword coverage plus cosine similarity |
| Experience | 20% | Detected years compared with the requirement |
| Education | 10% | Detected degree level compared with the requirement |
| Completeness | 5% | Presence of common resume sections |

Scores are coaching signals, not hiring decisions. The parser is intentionally explainable and cannot judge candidate quality, career potential, truthfulness, or context.

## Project structure

```text
app.py                    Streamlit entry point
config/                   Environment settings
components/               Reusable user-interface sections
services/                 Parsing, analysis, scoring, AI, and reporting
prompts/                  Prompt builders for optional AI features
utils/                    Constants, helpers, and validators
data/                     Skill catalog and sample job descriptions
outputs/                  Generated-report and temporary-file locations
tests/                    Unit tests
assets/                   Logo and application styles
```

## Customize

- Add or rename skills and aliases in `data/skills.json`.
- Add sample descriptions under `data/sample_jobs/`, then register them in `data/job_roles.json`.
- Adjust score weights in `utils/constants.py`; keep them totaling `1.0`.
- Change the maximum upload size or AI model in `.env`.
- Update colors and layout rules in `assets/styles.css`.

## Limitations

- Scanned/image-only PDFs need OCR before upload.
- Experience and education extraction use simple patterns and should be treated as estimates.
- The local similarity engine is lexical; it does not use embeddings.
- AI output may be imperfect. Review suggestions and never add unsupported claims to a resume.

## License

MIT — see [LICENSE](LICENSE).

