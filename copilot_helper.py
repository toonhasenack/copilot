import subprocess, shutil, textwrap, re
from IPython.display import Markdown, display, Code

def _ensure_copilot_on_path():
    if shutil.which("copilot") is None:
        raise RuntimeError(
            "The 'copilot' CLI isn't on PATH. Install with `npm i -g @github/copilot` "
            "and ensure your npm global bin is on PATH."
        )

def ask_copilot(
    question: str,
    workdir: str = None,
    timeout: int = 120,
    allow_tools: str = None,
    agent: str = "programming",
    model: str = "gpt-5"
):
    """
    Ask GitHub Copilot CLI a question using a specified agent (default: programmer).
    """
    _ensure_copilot_on_path()

    cmd = ["cmd", "/d", "/s", "/c", "copilot", "--prompt", question]

    if model:
        cmd += ["--model", model]
    if agent:
        cmd += ["--agent", agent]
    if allow_tools:
        cmd += ["--allow-tool", allow_tools]

    proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"Copilot CLI failed (exit {proc.returncode}).\n{proc.stderr.strip()}")

    return proc.stdout.strip() or proc.stderr.strip()


# --- Simple LaTeX-ish formatter for Jupyter Markdown ---
def to_markdown(ans: str):
    """
    Display Copilot's output directly as Markdown in Jupyter.
    Assumes the text already contains any LaTeX ($$...$$) or Markdown formatting.
    """
    from IPython.display import Markdown, display

    if not ans:
        display(Markdown("_No output from Copilot._"))
        return

    display(Markdown(ans))

def to_code(ans: str, language: str = "python"):
    """
    Display Copilot's entire output as a single code block in Jupyter.

    Parameters
    ----------
    ans : str
        The raw text output from Copilot.
    language : str, optional
        Programming language for syntax highlighting (default: python).
    """
    if not ans:
        print("No output from Copilot.")
        return

    display(Code(ans, language=language))

# ---- Example usage (run these cells after the definitions above) ----
# Q = "Explain the difference between precision and recall with a small numeric example."
# raw = ask_copilot(Q, workdir=".", allow_tools=None)  # deny tools (safe default)
# to_markdown_with_latex(raw)
