# Interview Desk

A small hiring tool for a clinic: positions, candidates, interviews, feedback, CVs and joining — with Google Calendar invites sent to candidates automatically.

It's a **single static web page** (`index.html`). There is no server and no database: everything is stored in your own Google account — a Google Sheet for records, Google Calendar for interviews and Google Drive for CVs. That means it can be hosted for free on GitHub Pages, and **this repository never contains candidate data**.

## Features

- **Dashboard** — open positions, pipeline counts, interviews this week, interviews waiting for an outcome, offers out, who's joining soon, pipeline by position.
- **Candidates** — contact details, position, stage (Applied → Screening → Interviewing → Shortlisted → Offered → Hired → Joined, or Rejected / Withdrawn), salary (current / expected / offered), notice period, availability, joining date, rating, tags, CV, notes and an automatic history.
- **Positions** — title, department, location, type, openings, salary range, status.
- **Interview tracker** — schedule from any candidate (date, time, length, mode, interviewers); a Google Calendar invite goes to the candidate. See who accepted / declined, the address each invite went to, and the Google Meet link (Join / Copy / Add). Invites sent outside the desk are found and linked automatically.
- **Scheduled in Google Calendar** — live list of invites created from the desk, with response, Meet link and Cancel & notify.
- **CVs** — attach a PDF / Word / image to a candidate; stored in a "CVs" folder in Google Drive and previewed in place.
- **Bulk import** — schedule interviews from an Excel sheet (invites sent), with an **Interview Status** column / dropdown per row: *Completed*, *No-show* and *Cancelled* rows are recorded or update the existing interview without sending anything, so re-importing keeps the lists current. Or import existing candidate lists from a sheet tab or Excel/CSV without sending anything.
- **Stays signed in** across page refreshes; one click to continue after Google's hourly session limit.

Calendar events are titled `[Interview] <position> - <candidate>/<organisation>` (editable in Settings).

---

## Publish on GitHub Pages (free)

GitHub Pages is free for **public** repositories. That's safe here: the code holds no secrets and no candidate data — only people who can open your hiring sheet can see any records.

### Option A — upload in the browser (no tools needed)
1. On GitHub, click **New repository** → name it (e.g. `interview-desk`) → **Public** → **Create repository**.
2. Click **uploading an existing file**, drag in **all files from this folder** (`index.html`, `interview-import-template.xlsx`, `serve.py`, `README.md`, `.gitignore`, `.nojekyll`) → **Commit changes**.
   *Files starting with a dot are hidden in Finder — press **Cmd+Shift+.** to show them.*
3. **Settings → Pages** → *Source*: **Deploy from a branch** → Branch **main**, folder **/ (root)** → **Save**.
4. After a minute the site is live at `https://<your-username>.github.io/interview-desk/`.

### Option B — with git
```bash
cd zen-interview-desk
git init -b main
git add .
git commit -m "Interview Desk"
git remote add origin https://github.com/<your-username>/interview-desk.git
git push -u origin main
```
Then turn on Pages as in step 3 above.

### Then allow the new address in Google
In **Google Cloud Console → APIs & Services → Credentials**, open your OAuth client and add to **Authorized JavaScript origins**:
```
https://<your-username>.github.io
```
(origin only — no `/interview-desk/` path, no trailing slash). Keep `http://localhost:8080` too if you also run it locally. Changes can take a few minutes.

---

## One-time Google setup (≈10 minutes)

1. **Project** — <https://console.cloud.google.com/> → create a project.
2. **APIs** — *APIs & Services → Library* → enable **Google Calendar API**, **Google Sheets API** and **Google Drive API**.
3. **OAuth consent screen** (*Google Auth Platform*):
   - **Internal** if everyone is in your Google Workspace domain — no review needed.
   - Otherwise **External** and leave it in **Testing**, adding each colleague under **Test users** (up to 100). They'll see a one-time "unverified app" notice. Opening it to anyone requires Google's verification (Calendar and Sheets are sensitive scopes).
   - Scopes:
     - `https://www.googleapis.com/auth/calendar.events`
     - `https://www.googleapis.com/auth/calendar.calendarlist.readonly`
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/drive.file` (only files the desk itself creates)
4. **OAuth client ID** — *Credentials → Create credentials → OAuth client ID* → **Web application** → add your site under *Authorized JavaScript origins* (see above). No redirect URI is needed. Copy the client ID.

### Skip the setup for your team (optional)
Edit the top of the script in `index.html`:
```js
const DEFAULT_CLIENT_ID = "1234567890-abc.apps.googleusercontent.com"; // your OAuth client ID (not a secret)
const DEFAULT_SHEET_ID  = "";  // the long ID in your hiring sheet's URL: /spreadsheets/d/<this part>/edit
```
The client ID isn't secret — Google only accepts it from the origins you listed. The sheet ID is only usable by people the sheet is shared with; leave it empty if you'd rather each person pastes the link once in **Settings**.

## First run
1. Open the site → **Connect Google** → pick the clinic account.
2. **Settings → Create a new hiring sheet** (or paste the link to an existing one).
3. In Google Sheets, **Share** the hiring sheet with colleagues as **Editor**. Under **Settings → Share uploaded CVs with**, list the colleagues who should see CVs.
4. Add positions and candidates, or bring in an existing list with **Bulk import → Import existing records**.

## Run it on your own computer
```bash
python3 serve.py
```
Then open <http://localhost:8080>. (`serve.py` serves this folder to your computer only and tells the browser not to keep stale copies.)

## Where the data lives
| What | Where |
|---|---|
| Positions, candidates, interviews, notes | Your Google Sheet — tabs `Positions`, `Candidates`, `Interviews`, `Notes` (created automatically). You can add or reorder columns; don't rename the `ID` columns. |
| Interview invites, replies, Meet links | Google Calendar (the calendar chosen in Settings) |
| CVs | Google Drive — a "CVs" folder in the uploader's Drive, private unless shared |
| Settings (calendar, templates, time zone) | Each person's browser |

**Never commit candidate spreadsheets or CVs to this repository** — it's public. `.gitignore` blocks `.xlsx`/`.csv`/`.pdf`/`.doc(x)` files (except the blank import template) as a safety net.

## Troubleshooting
| Message | Fix |
|---|---|
| *origin_mismatch* / *idpiframe_initialization_failed* | Add the site's exact origin to Authorized JavaScript origins, wait a few minutes. |
| *Google sign-in is still loading* / *script was blocked* | An ad/tracker blocker is blocking `accounts.google.com` — allow it for this site. |
| *The Google … API isn't enabled* | Enable it under APIs & Services → Library. |
| *Hasn't granted every permission* | Sign out, Connect Google again and tick every box. |
| *Access blocked: app has not completed verification* | Add the person as a Test user, or make the consent screen Internal. |
| *Can't edit that sheet* | Ask the sheet's owner to share it with you as Editor. |
| Old version still showing after an update | Reload with Cmd+Shift+R (GitHub Pages caches for up to 10 minutes). |
