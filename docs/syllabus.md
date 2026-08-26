# Berkeley BioE 147 / BioE 247 — Principles of Synthetic Biology

**Fall 2026** · [← back to README](../README.md) · See also
[Course Map](course-map.md) · [Coverage Matrix](coverage-matrix.md) ·
[Readings](readings.md)

The dates in this document are checked against
[`course.yaml`](../course.yaml) by `tools/check_schedule.py`.

---

## Course Description

The field of synthetic biology has emerged as one of the most important and profound ways by which we can understand and manipulate our physical world for desired purposes. In this course, the field and its natural scientific and engineering basis are introduced. Relevant topics in cellular and molecular biology and biophysics, dynamical and engineering systems, and the design and operation of natural and synthetic circuits are covered in a way that allows the student to begin to design new biology-based systems.

The course deals primarily with the theoretical foundations for design, and less with practical implementation. The organizing question is a specific one: **can we specify what we want a biological system to do, and then build a cell that does it?** After thirty years the answer is *partially* — and the substance of the field lives in that word. The course is about where the specification-to-implementation pipeline works, where it breaks, and why.

The material requires a good conceptual basis in molecular biology, biochemistry, and cell biology, and some modest skill in differential equations and linear algebra. We will fill gaps where they exist, but you are expected to come in with some background in these.

### Structure

The course is organized in two halves that do different work.

**Weeks 1–7 — Design principles.** What can a circuit do, and why is it built that way? Mass action and timescale separation, regulation functions derived from equilibrium binding, phase-plane analysis, bistability, feedforward loops, oscillation, stochasticity, and the digital abstraction. The goal is that every student, whatever your background, can take a circuit diagram, write the equations, and determine its behavior quantitatively.

**Weeks 8–15 — Engineering design.** Now build one that survives in a real host. Implementation layers, resource competition and burden, retroactivity and insulation, feedback control and robustness, evolutionary stability, multicellular consortia, minimal cells, therapeutic circuits, machine-learning-based design, and biosecurity.

### What is different in 2026

This course has been team-taught with Ron Weiss (MIT) for fifteen years. In 2026 it is taught solely at Berkeley, and has been substantially rebuilt:

- **Computational work moves from MATLAB to Python**, running in your browser with nothing to install (see *Computing*, below). This directly addresses the most consistent complaint of prior years.
- **Digital logic design is compressed** from roughly seven lectures to two. The digital abstraction is a genuinely useful lens on biological circuits; Karnaugh maps and gate minimization are not the best use of your semester.
- **Every lecture includes a worked example** — a problem solved in real time using the exact technique the next problem set demands.
- **Nothing is assessed that was not demonstrated first.** If a problem set asks you to find fixed points, you will have watched fixed points be found. This is a commitment. If I violate it, tell me and I will fix the problem set.
- **The term project roughly doubles in weight**, with staged deadlines and feedback beginning in week 5 rather than being effectively a December activity.
- **The final third of the course is substantially new**, covering work published since 2020: genome-scale language models and generative design, synthetic minimal cells, logic-gated cell therapies, and biosecurity as a technical problem.

---

## Instructors

| | | |
|---|---|---|
| **Adam Arkin** (Instructor) | U.C. Berkeley | aparkin@lbl.gov |
| **Hetvi Nilay Trivedi** (Reader) | U.C. Berkeley | hetvi_trivedi@berkeley.edu |

**Lectures:** Tuesdays & Thursdays, **Dwinelle 219**. Listed as 8:00–9:29; on Berkeley Time we begin at **8:10** and finish by **9:30**.
**Units:** 4 (3 hrs instruction + 1 hr discussion per week; 8 hrs outside work expected)

**Discussion / office hours:** Tuesdays immediately following class, **Dwinelle 88**

This is the course's scheduled discussion hour and it doubles as my open office hours. Attendance is not required and no new material is introduced there — it is for computational help, working problems, and project consultation. Historically it is the most useful hour in the course for the students who use it. Additional office hours by appointment are scheduled through Gwyneth.

Class material is available on **bCourses**.

**A note on the hour.** We start at 8:10, which is early for material that asks you to think. The format is built around that: roughly 45 minutes of concept followed by ~30 minutes of a problem worked in real time, with the room doing a good deal of the work. Coffee is entirely reasonable. You will not usually need a laptop in lecture — the computing is done at home and in the discussion hour, and I would rather have your attention.

---

## Learning Outcomes

Students will learn how to:

- Analyze and model relevant biological systems for their logical and dynamical function.
- Understand the underlying conceptual foundations of parts and circuit design, from elements through modules.
- Design advanced biological circuits with several levels of control, from gene expression through signaling networks and cell–cell communication.
- Identify and address challenges and irreducible error states in design — load and fitness effects, resource competition, evolutionary instability, and failure modes.

More concretely, by December you should be able to:

1. Translate a circuit diagram into a system of differential equations, stating which assumptions are load-bearing.
2. Derive regulation functions from equilibrium binding rather than asserting Hill functions.
3. Analyze a two-dimensional system in the phase plane: nullclines, fixed points, Jacobian, linear stability, bifurcation.
4. Predict when a circuit will be bistable, oscillate, or adapt — and say what would destroy each behavior.
5. Simulate a stochastic circuit and quantify its noise.
6. Use the same stoichiometric description in two different ways — integrated forward as dynamics, and solved as a constrained optimization — and know which question each answers.
7. Quantify the cost a circuit imposes on its host, and the cost the host imposes on the circuit.
8. Explain why a circuit that works on a plasmid in *E. coli* may fail in a chassis, in a consortium, or after 200 generations.
9. Read a current primary paper and distinguish what was demonstrated from what was claimed.
10. Design a circuit for a specified function, defend it quantitatively, and articulate its failure modes and risks.

---

## Prerequisites

Students interested in taking the class should have a basic understanding of:

- **cell biology** (e.g. internal structure of cells)
- **molecular biology** (e.g. enzymatic catalysis)
- **genetics** (e.g. structure of genes, transcription and translation)
- **basic chemistry** (e.g. writing reaction rates)
- **basic college mathematics** through elementary differential equations, calculus, and linear algebra

**Programming:** prior Python experience is *not* assumed. You should be able to write a loop and a function in some language. The tooling is taught in week 2 and used every week thereafter.

*Note:* Boolean algebra was previously listed as a prerequisite. With logic design compressed to two lectures, it is no longer required.

This cohort reliably spans biology to physics to EECS. The first lecture includes an **ungraded diagnostic** whose only purpose is to tell me where the room actually is, so I can set the pace honestly. It is not graded and affects nothing.

If your background is light on differential equations, weeks 1–4 are the demanding stretch. If it is light on molecular biology, weeks 8–10 are. Both are survivable. Neither is if you wait until the midterm to say something.

---

## Computing

All computational work is in **Python**, in Jupyter notebooks. **You do not need to install anything.**

### Primary path: UC Berkeley DataHub

Berkeley operates a free JupyterHub for course use. You already have an account; it authenticates through bCourses.

1. Go to **https://datahub.berkeley.edu**
2. Sign in with your CalNet credentials.
3. That's it — JupyterLab opens in your browser.

**To open an assignment**, click the link posted on bCourses. It pulls the notebook into your account and opens it. Use the link every time; do not download and re-upload notebooks.

Everything the course needs is already installed. If you find you need to `pip install` something, post on the bCourses forum so everyone gets the fix.

**Four things that will otherwise surprise you:**

- **Sessions shut down after ~30 minutes of inactivity.** Files on disk are safe; anything held only in memory is not. Save intermediate results before walking away from a long simulation.
- **Your home directory is not backed up.** Download anything you care about, at minimum your completed problem sets.
- **Access ends roughly nine months after you graduate.** Download your project before then.
- **Every assignment has a reset link.** If you corrupt a notebook beyond repair, it renames your copy with a timestamp and gives you a clean one. Nothing is deleted.

### Backup path: Google Colab

Every course notebook carries an **"Open in Colab"** badge. Colab requires a Google account; your @berkeley.edu account works, as does a personal one.

Colab is a genuine fallback but not an equal alternative, for one specific reason: **opening a notebook from GitHub in Colab brings only that notebook**, without the course's shared helper code. Every notebook therefore begins with a clearly marked setup cell that clones the repository. **In Colab you must run that cell first.** Skipping it produces import errors that look like bugs and are not.

Colab also discards everything when a session ends — installed packages, files, all of it — and saves your notebook to your *personal* Google Drive, where I cannot see it. Use it when DataHub is down. Do not let your graded work live there.

The two environments run slightly different library versions. All course code is written to work in both; if you write your own and it works in one but not the other, that is usually the reason.

### Course repository

**[github.com/ArkinLaboratory/posb2026](https://github.com/ArkinLaboratory/posb2026)** — public. You are welcome to clone and run locally. If you do, you own your environment: I will help with the science, but neither I nor the reader can debug your conda installation. This was a real and repeated failure mode in previous years and it is why DataHub is the supported path.

### Submitting

Problem sets are submitted through **Gradescope**, linked from bCourses.

**Before submitting: `Kernel → Restart Kernel and Run All Cells`,** then confirm it runs top to bottom without error. A notebook that only works because of state left over from cells run in a different order is not a working notebook, and it is the most common way to lose points on something you actually understood.

### Getting your environment working — week one

You do not need a laptop on day one. The first lecture closes with three minutes showing you where the links live and what to do when something breaks, and that is all.

**The real environment session is the discussion hour on Tuesday, September 1** — immediately after class, in Dwinelle 88, so you do not have to make a separate trip. Bring a laptop to that one. We will get everyone into DataHub, run a five-line check, and fix whatever does not work while I am standing there. **PS0 is due the following day**, Wednesday September 2, deliberately: the help comes before the deadline, and the deadline comes before Session 3, which is where the notebooks actually start.

If you would rather not wait, open PS0 in Colab today and run the first cell. If it prints a table of version numbers you are already set. This matters most if you are **on the waitlist**, since DataHub needs you to be enrolled and Colab does not.

---

## Grading

| Component | Weight |
|---|---|
| Problem sets (9, lowest two dropped) | **30%** |
| Midterm — Thursday, October 15, in class | **15%** |
| Final exam — finals week, in person | **25%** |
| Term project | **30%** |

Compared with previous years, exams fall from 60% to 40% and the project doubles from 15% to 30%.

### Problem sets

Nine sets, roughly weekly, **2–4 problems each**. These are deliberately short — a weekly check that you can execute the technique from that week's worked example, not a weekend-consuming exercise. If a set takes you more than a few hours, that is information; tell me.

**Your two lowest scores are dropped.** The drops exist so a bad week costs you nothing and you do not have to explain yourself. Because worked solutions are published immediately after each deadline, routine extensions are not possible. For genuine extenuating circumstances, reach out — see *Absences* below.

| Set | Out | Due | Covers |
|---|---|---|---|
| PS0 | Aug 27 | **Sep 2** | Environment check — **ungraded** |
| PS1 | Sep 3 | Sep 10 | Mass action, timescale separation, Michaelis–Menten, Hill |
| PS2 | Sep 10 | Sep 17 | Expression dynamics, response time, promoter occupancy |
| PS3 | Sep 17 | Sep 24 | Autoregulation, phase plane, stability |
| PS4 | Sep 24 | Oct 1 | Bistability, the toggle, hysteresis |
| PS5 | Oct 1 | Oct 8 | Feedforward loops, oscillation criteria |
| — | — | — | *Midterm Oct 15 — no set* |
| PS6 | Oct 20 | Oct 29 | Digital abstraction, signal matching, hazards, assembly design |
| PS7 | Oct 29 | Nov 5 | Implementation layers, resource competition, burden, flux balance analysis |
| PS8 | Nov 5 | Nov 19 | Retroactivity, feedback control, evolutionary stability |
| PS9 | Nov 19 | Dec 3 | Communities, minimal cells, therapeutic and generative design |

### Midterm — Thursday, October 15

In class, covering sessions 1–13 (everything through the digital abstraction). The preceding session, Tuesday October 13, is a review and worked-problem session, and **a written scope document listing every examinable technique is published that day.** The practice exam is built from *this semester's* worked examples.

### Final exam

In person during the finals block, cumulative but weighted toward the second half.

Both exams are in person, and it is worth saying why. Problem sets are open-book, open-collaboration, and open-tool. That is the right policy for learning, but it makes them a weak signal of individual understanding. Two proctored exams at a combined 40% — down from 60% — is the trade: substantially less exam pressure than this course has carried, while preserving a real measure of what you personally can do.

---

## Final Project

The final project showcases your understanding of the course material — or at least its spirit — by demonstrating your ability to formulate a new idea in synthetic biology and to set up and at least partially execute a model or data analysis of a biological problem.

The final deliverable takes the form of the **'front-end' of a research proposal**, plus a data/software package: a well-documented set of code and data used to create the results presented, where relevant (in the past, some projects have been pure mathematics). This is a 'paper' of a sort, with three sections, total length **under 10 pages**.

### 1. Background and Significance

This sets up the problem you will solve by explaining its larger context in the field and narrowing down to what you have chosen to approach.

I often describe a good grant as an **hourglass-shaped story**. At the top you tell the broad story of the field and the challenges it faces. You then narrow to the subarea in which your problem is a critical piece. At the neck of the hourglass you describe your specific problem and why cracking it matters. The rest of the proposal then describes your technical approach, the impact on the subarea if you solve it, and the impact on the entire field.

You will really only be doing the first part of this — down to the neck — in this section. The idea is to read enough literature to understand the problem you are trying to solve, and then bring your readers to understand what you are trying to do and why. Include citations and, where useful, explanatory figures.

### 2. Specific Aims

Two to three short bullet points summarizing what you propose to do. Each bullet should represent a *unit deliverable* in solving the problem. They often look like: (1) obtain, quality control, and perform preliminary analysis of the gene expression dataset from XYZ; (2) using analysis X, retrieve the subset of data most relevant to the phenotypes under study; (3) train and test a model on this data with these particular outcomes of success.

Each bullet is followed by a paragraph — two at most — summarizing your approach to meeting that aim.

### 3. Preliminary Results

This is the actual meat of the proposal. It demonstrates that what you propose in your Specific Aims is feasible and that there is likely something interesting there. You might have actually accomplished Aim 1, and shown preliminary work on Aims 2 and 3 — initial clustering and cluster selection, an initial model fit. These might not be what you would ultimately do, but they demonstrate that you can find and master the data and that you have the skills to do more complex things.

### How it is judged

On **intellectual coherence and the strength of the arguments** for importance and approach, *and* on the **demonstrated ability to actually accomplish and document an analysis**. In general, students do best when choosing to extend an analysis well presented by another researcher — that is, from an excellent paper.

You are allowed to work together on obtaining and cleaning target datasets, and I encourage you to hone your ideas by talking to each other and to us. However, the bulk of the aims and analysis must be your own unique work product, and Section 1 must be wholly written by you, oriented toward the problem you choose. Where you leverage a peer's work, acknowledge it and give proper credit.

### Milestones

New this year: the project is staged, with feedback at each stage. In previous years it was effectively a December activity, and students said so.

| Milestone | Due | What you get back |
|---|---|---|
| **Project description** (1–2 pp): the system, the objective, why it is interesting | Thu Sep 24 | Written comments within one week |
| **Model description + preliminary results** (2–3 pp) | Thu Oct 22 | Written comments |
| **Draft write-up** | Thu Nov 12 | Peer review plus my comments |
| **Final write-up + code + 10-minute video** | Fri Dec 11 **[to confirm — RRR week]** | Grade and comments |

### BioE 147 versus BioE 247

The two course numbers have not been meaningfully differentiated in past years. This year:

- **Problem sets:** 247 students complete one additional problem per set, requiring either a derivation or an extension to a result from the primary literature.
- **Project:** 247 projects must include a critical analysis of the primary literature the design draws on, and the model must go beyond reproducing a published result.
- **Final exam:** 247 students answer one additional open-ended design question, graded on the quality of the argument rather than on reaching a particular answer.

---

## Reading

**There is no required textbook.** Readings are primary literature, posted on bCourses, and short — typically one paper per week, with a specific figure to focus on.

The rule is fixed, and it is a promise in both directions: **a paper discussed in
class is assigned at the end of the previous class**, with a named figure or
section to focus on. You will always have had a full class period's notice, and
the discussion segments assume you used it.

The running list lives at
[docs/readings.md](https://github.com/ArkinLaboratory/posb2026/blob/main/docs/readings.md)
and fills in as the term proceeds — later sessions are deliberately not fixed
yet, because what is worth reading depends on where the class actually is.

**Strongly recommended as companions:**

- **Elowitz & Bois, *Biological Circuit Design* — https://biocircuits.github.io** — free and online, covering much of the first half of this course with a complementary framing. Every chapter has an executable Python appendix that regenerates its figures from scratch, in the same NumPy/SciPy stack we use. If a lecture in weeks 1–7 does not land, read the corresponding chapter there.
- **Alon, *An Introduction to Systems Biology*, 2nd ed.** — the standard reference for network motifs.
- **Del Vecchio & Murray, *Biomolecular Feedback Systems*** — free online; the reference for retroactivity and control.

---

## Schedule

Instruction begins Wednesday, August 26. Classes end Friday, December 4. RRR week December 7–11. Finals December 14–18.
**No class Thursday, November 26 (Thanksgiving).**

### Part I — Design Principles

| # | Date | Week | Lecture content | Worked example | Assignments |
|---|---|---|---|---|---|
| 1 | Thu 8/27 | W1 | What synthetic biology is in 2026; the specification problem; course mechanics | Diagnostic; DataHub setup | PS0 posted |
| 2 | Tue 9/1 | W2 | The cell as a physical substrate: crowding, copy number, timescales | Order-of-magnitude estimation; diffusion times | PS0 due |
| 3 | Thu 9/3 | W2 | Modeling I: mass action, stoichiometry, d**X**/d*t* = **S·v** | Build and integrate a three-species system from scratch | PS1 posted |
| 4 | Tue 9/8 | W3 | Modeling II: separation of timescales, quasi-steady state and its limits | Derive Michaelis–Menten; derive Hill from cooperative binding | |
| 5 | Thu 9/10 | W3 | Gene expression dynamics; response time; dilution versus degradation | Response-time calculation; effect of degradation tags | PS1 due · PS2 posted |
| 6 | Tue 9/15 | W4 | Promoter occupancy from statistical thermodynamics; regulation functions | Derive activator, repressor, and AND-like rate laws | |
| 7 | Thu 9/17 | W4 | Autoregulation: negative (speed, variance) and positive (bistability) | Derive the negative-autoregulation speed-up | PS2 due · PS3 posted |
| 8 | Tue 9/22 | W5 | The phase plane: nullclines, fixed points, the Jacobian, linear stability | Complete two-dimensional stability analysis | |
| 9 | Thu 9/24 | W5 | Bistability and the toggle switch: bifurcation, hysteresis, failure modes | Fixed points for *n* = 4 and *n* = 1 | PS3 due · PS4 posted · **Project description due** |
| 10 | Tue 9/29 | W6 | Feedforward loops: persistence detection, pulse generation, adaptation | FFL timing analysis; numerical IFFL adaptation | |
| 11 | Thu 10/1 | W6 | Oscillators: the repressilator, delayed negative feedback, conditions for oscillation | State and apply the oscillation criterion; locate the Hopf boundary | PS4 due · PS5 posted |
| 12 | Tue 10/6 | W7 | Noise: intrinsic versus extrinsic, CV, bursting, the master equation | Write a Gillespie simulator from scratch | |
| 13 | Thu 10/8 | W7 | The digital abstraction: transfer curves, gain, thresholds, noise margins | Full numeric signal matching between two measured gates | PS5 due |
| 14 | Tue 10/13 | W8 | **Review and worked problems** | Open problem session | Midterm scope published |
| 15 | **Thu 10/15** | W8 | **MIDTERM** — sessions 1–13 | | |

### Part II — Engineering Design

| # | Date | Week | Lecture content | Worked example | Assignments |
|---|---|---|---|---|---|
| 16 | Tue 10/20 | W9 | Combinational logic in cells; hazards; Cello, and why design automation plateaued | Hazard timing table, end to end | PS6 posted |
| 17 | Thu 10/22 | W9 | Building it physically: parts, compositors, context dependence, and DNA assembly (Golden Gate/MoClo, Gibson, enzymatic synthesis) | Compose a two-part system in code; design overhangs for a three-part assembly | **Model description due** |
| 18 | Tue 10/27 | W10 | Implementation layers: CRISPRi/a, recombinase memory, bridge RNAs, protein circuits | Compare gate families on orthogonality, speed, and load | |
| 19 | Thu 10/29 | W10 | Resource sharing, cellular economy, growth laws, burden | Shared-resource simulation | PS6 due · PS7 posted |
| 20 | Tue 11/3 | W11 | **Metabolic engineering and constraint-based design:** flux balance analysis, the stoichiometric matrix as a design object, knockout and coupling strategies | Solve an FBA problem as a linear program with `scipy.optimize.linprog` on a hand-written **S** — the same matrix from session 3, asked a different question | |
| 21 | Thu 11/5 | W11 | Retroactivity, impedance, insulation, load drivers | Retroactivity calculation for a loaded module | PS7 due · PS8 posted |
| 22 | Tue 11/10 | W12 | Robustness and control: integral feedback, antithetic control, exact adaptation | Simulate an antithetic controller; quantify what it costs | |
| 23 | Thu 11/12 | W12 | Evolutionary failure: mutation, burden, circuit loss; design for stability; containment | Time-to-circuit-failure from mutation rate and fitness cost | **Draft write-up due** |
| 24 | Tue 11/17 | W13 | Communities: cell–cell communication, quorum sensing, patterning, division of labor | Sender/receiver band-detection analysis | |
| 25 | Thu 11/19 | W13 | Minimal and synthetic cells: syn3A and bottom-up construction | Genome-partitioning fidelity: why most daughters are incomplete | PS8 due · PS9 posted |
| 26 | Tue 11/24 | W14 | Therapeutic circuits: logic-gated cell therapies, synNotch, in vivo delivery | Design a multi-input classifier to a false-positive budget | |
| — | Thu 11/26 | W14 | **Thanksgiving — no instruction** | | |
| 27 | Tue 12/1 | W15 | Machine learning as the specification layer: structure prediction, protein design, genome language models | Design–filter–validate arithmetic: what hit rate beats directed evolution? | |
| 28 | Thu 12/3 | W15 | Biosecurity and governance as technical problems; what actually limits synthetic biology | Why sequence-similarity screening fails on generated sequences | PS9 due |

**Final project due:** Friday, December 11 **[to confirm]**
**Final exam:** finals block, December 14–18 — **exam group to confirm with the registrar**

---

## Course Policies

### Class Participation

This class can be highly interactive and engagement is a critical part of the activity. While attendance isn't mandatory, you will learn a great deal more, and help your colleagues, if you are present and engaged. I also use this opportunity to understand and evaluate students' understanding, which helps put quantitative progress in better context.

### Collaboration

You are encouraged to form study groups and work together to understand course material, but **all written work, code, and responses to in-class questions should be your own.** There are ways to make your work personal and unique even when it seems there is only one way to correctly answer a question, and the instructors will support you in learning these methods.

Note at the top of each submission who you worked with. This is bookkeeping, not a penalty, and it has never cost anyone a point.

**Exams:** no collaboration. Both are proctored.

### Language Models and AI Tools

**Permitted on problem sets, with two conditions.**

Use an LLM to explain a concept you are stuck on, debug code, check algebra, or find the name of a technique you half-remember. Note briefly where you used one — a sentence is enough.

The two conditions: **you must be able to explain anything you submit**, and **the code you submit must run**, which means understanding it well enough to fix it when it doesn't.

The honest reasoning: every technique in this course is examined in a proctored room. If you outsource the problem sets you will discover the gap in October and again in December, at 40% of your grade, having spent the semester earning 30% for work that taught you nothing. These tools are genuinely useful for learning and genuinely destructive as a substitute for it, and that distinction is not something I can police. It is yours to manage. I would rather tell you plainly how the incentives work than pretend a prohibition would hold.

**Exams:** prohibited, as with any outside assistance.

**Project:** permitted and disclosed. Include a short methods note describing what you used and for what. Using an LLM to help write code, survey literature, or draft prose is fine. Submitting a design you cannot defend is not — and the video is where that becomes obvious.

### Absences and Extenuating Circumstances

Two dropped problem sets and reduced exam weight are the built-in slack. If something larger happens — illness, family emergency, anything — tell me while it is happening, not in December. There is almost always a reasonable arrangement available at the time and almost never one available retroactively.

### Health

If you are contagious, please do not attend in-person activities. Keep up by following lecture and discussion recordings, and let me know if you need accommodation or help.

### Study Groups and the Course Forum

The official online forum for this course is available through bCourses, where the instructors periodically monitor questions. Please use it whenever possible instead of informal tools such as group chats; this increases transparency and inclusion. It is especially important in these venues to choose your words carefully so that you are supportive of your classmates and the instructional team. Of course, use email or direct communication for specific problems or activities.

### Inclusion

We are committed to creating an environment welcoming of all students where everyone can fulfill their potential for learning. To do so, we intend to support a diversity of perspectives and experiences and respect each others' identities and backgrounds (including race/ethnicity, nationality, gender identity, socioeconomic class, sexual orientation, language, religion, ability, etc.). To help accomplish this:

- If you feel your performance in the class is being impacted by a lack of inclusion, please contact the instructors, an academic advisor, or the departmental Faculty Equity Advisor (https://engineering.berkeley.edu/about/equity-and-inclusion/faculty-equity-advisers/). An anonymous feedback form is available at https://engineering.berkeley.edu/about/equity-and-inclusion/feedback/.
- If you feel your performance is being impacted by experiences outside of class (family matters, current events), please don't hesitate to talk with the instructors or academic advisors in Engineering Student Services. We want to be a resource for you.
- There is no tolerance for sexual harassment or violence. If your behavior harms another person in this class, you may be removed from the class or the University either temporarily or permanently.
- If you have a name and/or pronouns that differ from your legal name, designate a preferred name for use in the classroom at https://registrar.berkeley.edu/academic-records/your-name-records-rosters.
- As a participant in this class, recognize that you can be proactive about making other students feel included and respected.

### Berkeley Honor Code

Everyone in this class is expected to adhere to this code: *"As a member of the UC Berkeley community, I act with honesty, integrity, and respect for others."*

### Student Conduct

Ethical conduct is of utmost importance in your education and career. The instructors, the College of Engineering, and U.C. Berkeley are responsible for supporting you by enforcing all students' compliance with the Code of Student Conduct (https://sa.berkeley.edu/code-of-conduct) and the policies in the CoE Student Guide (https://engineering.berkeley.edu/students/undergraduate-guide/policies-procedures/). The Center for Student Conduct is your central source for guidance (https://sa.berkeley.edu/conduct).

### Accommodation Policy

We honor and respect the diversity in our student body and are committed to ensuring you have the resources you need to succeed. If you need accommodations that provide equitable access (religious observance, physical or mental health concerns, insufficient resources, etc.), please check https://diversity.berkeley.edu/ and, if needed, discuss your specific case with Prof. Arkin. We will do our best to ensure all accommodations are respected, but we ask your collaboration in reminding us what you might need for an assignment, exam, or project in a timely manner. **Exam accommodations in particular need lead time to arrange properly.**

---

## Resources

**For academic performance.** The Center for Access to Engineering Excellence (CAEE, 227 Bechtel Engineering Center; https://engineering.berkeley.edu/student-services/academic-support) is an inclusive center offering study spaces, nutritious snacks, and tutoring in more than 50 courses for Berkeley engineers and other majors across campus. The Center also offers professional development, leadership, and wellness programs, and loans laptops and professional attire for interviews.

**For disability accommodations.** The Disabled Students' Program (DSP, 260 César Chávez Student Center #4250; 510-642-0518; http://dsp.berkeley.edu) serves students with disabilities of all kinds, including temporary disabilities. Services are individually designed based on the specific needs of each student as identified by DSP's Specialists. If you have already been approved for accommodations through DSP, know that DSP can quickly adjust your accommodations if your situation changes.

**For mental wellbeing.** Counseling and Psychological Services (CAPS, https://uhs.berkeley.edu/caps) is available as part of University Health Services (the Tang Center), including on-site in the College of Engineering (https://engineering.berkeley.edu/students/advising-counseling/counseling/). CAPS services are available to all students regardless of insurance, and initial visits do not cost anything. Same-day counseling is available at 510-642-9494, with a 24/7 counseling line at (855) 817-5667. Short-term help is also available from the Alameda County Crisis hotline: 800-309-2131. If you, or someone you know, is experiencing an emergency that puts their health at risk, please call 911.

**For recovery from sexual harassment or sexual assault.** The Care Line at the PATH to Care Center (510-643-2005; https://care.berkeley.edu/care-line/) is a 24/7, confidential, free, campus-based resource for urgent support around sexual assault, sexual harassment, interpersonal violence, stalking, and invasion of sexual privacy. The Care Line connects you with a confidential advocate for trauma-informed crisis support, including time-sensitive information, securing urgent safety resources, and accompaniment to medical care or reporting.

**For solving a dispute.** The Ombudsperson for Students (102 Sproul Hall; 510-642-5754; http://students.berkeley.edu/Ombuds) provides a confidential service for students needing a neutral party to resolve University-related disputes, academic or administrative. All matters referred to this office are held in strict confidence.

**For basic needs (food, shelter, etc.).** The Basic Needs Center (https://basicneeds.berkeley.edu/) provides housing, food, and transportation support. The UC Berkeley Food Pantry (#68 Martin Luther King Student Union; https://pantry.berkeley.edu) aims to reduce food insecurity among students. Students can visit as many times as needed and take as much as needed, while being mindful that it is a shared resource. The pantry operates on a self-assessed need basis; there are no eligibility requirements. It is intended for core food support rather than supplemental snacking.

---

*This syllabus is a plan, not a contract. If something is not working I will change it and tell you why. The reverse also holds: if something is not working, tell me while there is still time to fix it.*
