# add (or keep) these imports at the top
import os, gzip, urllib.request
import streamlit as st

def fetch_pdb_text(pdb_id_or_path: str) -> str:
    s = (pdb_id_or_path or "").strip()
    is_path = (os.sep in s) or s.endswith((".pdb", ".ent", ".pdb.gz", ".ent.gz"))

    if is_path:
        if not os.path.exists(s):
            st.error(f"File not found: {s}")
            raise FileNotFoundError(s)
        try:
            if s.endswith(".gz"):
                with gzip.open(s, "rt", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
            else:
                with open(s, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
        except Exception as e:
            st.error(f"Could not read file '{s}': {e}")
            raise
        if not txt.strip():
            st.error(f"File '{s}' is empty.")
            raise ValueError("Empty PDB text")
        return txt

    pdb_id = s.upper()
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            txt = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        st.error(f"Could not download PDB {pdb_id} from RCSB: {e}")
        raise
    if not txt.strip():
        st.error(f"Downloaded PDB {pdb_id} is empty.")
        raise ValueError("Empty PDB text")
    return txt
