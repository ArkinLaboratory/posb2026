# Classroom Demos

[← back to the repository root](../README.md)

Interactive notebooks built to be **projected and driven live during lecture**.
Nothing here is graded and nothing is submitted.

| Demo | For | What you turn |
|---|---|---|
| [Toggle Explorer](d09-toggle-explorer/) | Session 9 | α₁, α₂, and *n* — watch bistability appear and vanish |

## What makes a good demo here

A demo earns its two minutes of lecture time if **the parameter you drag
changes the answer to a question you just asked the room**. If it only makes a
pretty picture move, it belongs in a notebook, not on the projector.

The toggle explorer works because it lets you do something a static figure
cannot: set *n* = 1 and then fail, publicly and repeatedly, to produce
bistability at any α. That failure is the lesson.

## Running one in class

Open it on DataHub before lecture and run every cell — the first widget render
takes a few seconds and you do not want that pause live. Demos use `ipywidgets`,
which is installed on DataHub; in Colab, standard widgets work but you may need
`from google.colab import output; output.enable_custom_widget_manager()`.

Students can open the same link afterwards and keep playing. That is most of
the value — the lecture use is a demonstration, the after-class use is where
someone actually builds intuition.
