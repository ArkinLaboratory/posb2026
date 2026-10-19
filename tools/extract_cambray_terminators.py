"""Regenerate figures/data/s17_cambray_terminators.csv from the paper's SI.

The CSV is committed so the session-17 terminator figure is reproducible from
a clean clone; the SI itself is not in the repository. Run this only when the
SI changes. See the CSV's own header for provenance and licence.
"""
import io
import sys

import pandas as pd

SI = "private/readings/supp_gkt163_nar-00080-h-2013-File008.xls"
CSV = "figures/data/s17_cambray_terminators.csv"


def main():
    try:
        d = pd.read_excel(SI, sheet_name="Suppl. Table 1", header=3)
    except FileNotFoundError:
        sys.exit(f"{SI} not present; nothing to regenerate.")
    d = d.dropna(subset=["Mean TE Cell", "Predicted TE"])
    out = d[["Type", "Name", "Mean TE Cell", "Predicted TE"]].rename(
        columns={"Type": "klass", "Name": "name",
                 "Mean TE Cell": "measured_te", "Predicted TE": "predicted_te"})
    head = "".join(l for l in open(CSV) if l.startswith("#"))
    buf = io.StringIO()
    out.to_csv(buf, index=False, float_format="%.4f")
    open(CSV, "w").write(head + buf.getvalue())
    print(f"{CSV}: {len(out)} rows")


if __name__ == "__main__":
    main()
