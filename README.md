# GitHub Profile Analyst
A simple Python tool that fetches GitHub user statistics using the GitHub REST API and displays useful insights such as:

✔ Public repositories  
✔ Followers  
✔ Total stars  
✔ Most used programming language  
✔ Recent contributions (optional upgrade)  

This project highlights API integration, JSON handling, Python automation, and data processing.

---

## 🚀 Usage

### 1. Clone Repo
```bash
git clone https://github.com/<your-username>/github-profile-analyst
cd github-profile-analyst
```

### 2. Install required library
```bash
pip install requests
```

### 3. Run the script
```bash
python analyze_github.py
```

---

## 🔧 Configuration

Edit the username in the script:
```python
USERNAME = "your-github-username"
```

---

## 📎 File Structure
```
github-profile-analyst/
│
├── analyze_github.py
└── README.md
```

---

## 📌 Future Enhancements
- Export stats to JSON / CSV  
- Generate PDF report  
- Create GitHub profile improvements suggestions  
- Command-line arguments  

---

Built by **Shashwat Aneja**

For a machine-readable summary without progress messages, run `python analyze_github.py USERNAME --json`. Tied language counts are resolved alphabetically.

`--exclude-forks` and `--exclude-archived` filter repository aggregates. The profile’s Public Repositories field retains GitHub’s account-wide count.

Set `GITHUB_TOKEN` to authenticate public profile API requests with a higher rate limit. The token is sent only in the Authorization header and is never included in report output or URLs.

Read-only profile and repository requests retry one timeout, connection failure or HTTP 500/502/503/504 response. Authentication and rate-limit failures are returned immediately; every attempt retains the configured network timeout.

`Analyzed Repositories` identifies the scope after optional exclusions; `Language Repositories` reports a sorted count by primary language. GitHub’s `Public Repositories` profile count remains unfiltered.

`--min-stars N` restricts repository metrics to projects with at least N stars, after fork/archive exclusions. Profile-level public repository totals remain unfiltered and the analyzed count identifies the selected scope.

Repeat `--language Python --language Rust` to restrict repository metrics by primary language, case-insensitively. It combines with existing fork, archive and star filters; the profile’s public count stays unfiltered.

`--output summary.json` atomically saves the same profile metrics as the terminal report. A failed serialization or replacement preserves the previous file; it can be combined with `--json` stdout.

Repeat `--topic automation --topic python` to include repositories matching any selected primary topic tag, alongside existing language/star/archive/fork filters. Topic names are case-insensitive; repositories without topic metadata do not match.

Use `--top-repositories 5` to include a deterministic star-ranked list within the selected filters. Counts still cover all analyzed repositories; missing API URLs are null. The limit is 0–100 (0 disables ranking).

Repeat `--license MIT --license Apache-2.0` to filter analyzed repositories by any selected SPDX identifier, case-insensitively. Missing license metadata is excluded; the filter scopes aggregates and rankings. This reports GitHub metadata and is not a legal license audit.

`--max-pages N` bounds repository pagination work (1–1000, default 1000). If the last permitted page is full, completeness cannot be established and the analysis fails without partial metrics or replacing a prior export. The profile request is additional to this page budget.

`--timeout-seconds N` configures every profile and repository HTTP request, including retry attempts. The finite duration must be greater than zero and at most 120 seconds; the default remains 10. This is a per-request timeout, not a whole-analysis deadline.

Repeat `--exclude-repository "website-*"` to exclude short repository names from every metric and ranking. Matching uses case-insensitive fnmatch within the already selected repository scope. Up to 100 patterns of 200 characters each are accepted.

`--pushed-since YYYY-MM-DD` restricts all repository metrics and rankings to pushes on/after that inclusive UTC date. Null push dates are excluded; malformed or offset-free timestamps fail when this filter is enabled. Account-level counters retain their account scope.

`Language Stars` aggregates stars by primary language within the selected repository population. Unspecified-language stars and repository counts disclose coverage; these stars reconcile with Total Stars. Most Used Language continues to rank repository counts.
