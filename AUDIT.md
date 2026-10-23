# The Peer Audit (Section 5, 12 pts)

Repositories go public by Tue 10 Nov, 11:59pm. You are assigned one classmate's repository on
Thu 12 Nov, never one replicating your own paper. File your audit as a **GitHub issue on their
repository by Mon 16 Nov, 11:59pm**, then paste the issue's URL in your Canvas submission
comment. You are graded on the audit you file, not the one you receive.

## 1. Clone it fresh

Use an empty directory, with none of your own files in it.

```bash
mkdir ~/audit && cd ~/audit
git clone https://github.com/THEIR-USERNAME/THEIR-REPO.git
cd THEIR-REPO
```

## 2. Build the environment from their `requirements.txt`

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Note anything that fails to install, and the Python version you used (`python --version`).

## 3. Run the one command their README names

Usually `python reproduce.py`. Time it. Then compare:

- Does it finish? If not, where does it stop, and with what error?
- Is the headline number it prints the number in their README and their report?
- Does it need a file that is not in the repository and not downloaded by their code?

## 4. File one GitHub issue, about 300 words

On their repository: *Issues › New issue*. Title it `Peer audit: <your name>`. It must contain
these three parts, in this order:

1. **Reproducibility:** whether it runs from a clean checkout, and what broke if not.
2. **Methodological question:** one substantive methodological question.
3. **What I will adopt:** one thing they did that you will adopt.

For part 1, give the commands you ran and the exact error text, so they can fix it. For part 2,
ask about a choice that could change the headline number: a sample restriction, a standard
error, a bandwidth, a control. A courteous audit that finds nothing scores below a rigorous one
that finds a real problem.
