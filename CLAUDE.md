# CLAUDE.md

The working notes for this repository are in **[AGENTS.md](AGENTS.md)**, which
is canonical and read by every coding agent. **Read it now**, before doing
anything else here.

This file is a deliberate stub. It repeats only the four rules whose violation
cannot be undone, so that an agent that reads no further still does no harm:

1. **Never run `git` in Adam's repositories.** The file bridge cannot delete
   files, so a stranded `.git/index.lock` blocks his next commit and only he
   can clear it.
2. **Confirm the mount before writing a file.** Connected-folder names can be
   rebound mid-session; eighteen files once landed in an empty directory with
   every call reporting success. Address files by full canonical path.
3. **Never report a file as written without a tool result proving it**, and
   never report a delivery without verifying it landed.
4. **A deck that has been taught from is a record, not a build artifact.** Hand
   edits live in `private/taught/`; never suggest a command that rebuilds over
   one.

Everything else — the build commands, the house rules for the material, the
voice to write in, and why each rule exists — is in
[AGENTS.md](AGENTS.md).
