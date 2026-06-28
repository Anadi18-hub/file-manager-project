"""
📁 File Manager — Streamlit UI
A polished CRUD-style file handling app: Create, Read, Update, Delete files.
Run with: streamlit run file_manager_app.py
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------- PAGE CONFIG -----------------------------
st.set_page_config(
    page_title="File Manager | Python File Handling",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------- CUSTOM STYLING -----------------------------
st.markdown("""
<style>
    .main { background-color: #0f1117; }

    .app-title {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.1rem;
        background: linear-gradient(90deg, #6C63FF, #00C9A7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .app-subtitle {
        text-align: center;
        color: #9aa0ab;
        font-size: 1rem;
        margin-bottom: 1.8rem;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.card-marker) {
        background-color: #181b24;
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        border: 1px solid #2a2e3a;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        border: none;
        background: linear-gradient(90deg, #6C63FF, #4d8aff);
        color: white;
        transition: 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.88;
        transform: translateY(-1px);
    }

    .footer-note {
        text-align: center;
        color: #5f6573;
        font-size: 0.82rem;
        margin-top: 2.5rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #181b24;
        border-radius: 10px 10px 0 0;
        padding: 8px 18px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------- HEADER -----------------------------
st.markdown('<div class="app-title">📁 File Manager</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">A simple Python file-handling app — Create, Read, Update & Delete files, '
    'wrapped in a clean Streamlit UI.</div>',
    unsafe_allow_html=True,
)

# Folder where this app's files live (keeps demo files contained & tidy)
WORKDIR = Path("file_manager_storage")
WORKDIR.mkdir(exist_ok=True)


def resolve(name: str) -> Path:
    """Keep all file operations scoped to the storage folder."""
    return WORKDIR / name


# ----------------------------- TABS -----------------------------
tab_create, tab_read, tab_update, tab_delete, tab_browse = st.tabs(
    ["🆕 Create", "📖 Read", "✏️ Update", "🗑️ Delete", "🗂️ Browse Files"]
)

# ---------- CREATE ----------
with tab_create:
    st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
    st.subheader("Create a new file")

    filename = st.text_input("File name", placeholder="e.g. notes.txt", key="create_name")
    content = st.text_area("File content", placeholder="Write something...", height=150, key="create_content")

    if st.button("Create File", key="create_btn"):
        if not filename.strip():
            st.error("⚠️ Please enter a file name.")
        else:
            path = resolve(filename.strip())
            if path.exists():
                st.error(f"❌ A file named **{filename}** already exists.")
            else:
                try:
                    path.write_text(content)
                    st.success(f"✅ File **{filename}** created successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# ---------- READ ----------
with tab_read:
    st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
    st.subheader("Read a file")

    files = sorted(p.name for p in WORKDIR.glob("*") if p.is_file())
    if files:
        chosen = st.selectbox("Select a file to read", files, key="read_select")
        if st.button("Read File", key="read_btn"):
            path = resolve(chosen)
            try:
                text = path.read_text()
                st.success(f"📄 Showing contents of **{chosen}**")
                st.code(text if text.strip() else "(file is empty)", language=None)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.info("No files yet — create one in the **Create** tab first.")

# ---------- UPDATE ----------
with tab_update:
    st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
    st.subheader("Update a file")

    files = sorted(p.name for p in WORKDIR.glob("*") if p.is_file())
    if files:
        chosen = st.selectbox("Select a file to update", files, key="update_select")
        operation = st.radio(
            "Choose an operation",
            ["Rename", "Append content", "Overwrite content"],
            horizontal=True,
            key="update_op",
        )

        path = resolve(chosen)

        if operation == "Rename":
            new_name = st.text_input("New file name", key="rename_input")
            if st.button("Rename File", key="rename_btn"):
                if not new_name.strip():
                    st.error("⚠️ Please enter a new name.")
                else:
                    new_path = resolve(new_name.strip())
                    if new_path.exists():
                        st.error(f"❌ A file named **{new_name}** already exists.")
                    else:
                        try:
                            path.rename(new_path)
                            st.success(f"✅ Renamed **{chosen}** → **{new_name}**")
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

        elif operation == "Append content":
            extra = st.text_area("Content to append", height=120, key="append_text")
            if st.button("Append", key="append_btn"):
                try:
                    with open(path, "a") as fs:
                        fs.write(f"\n{extra}")
                    st.success(f"✅ Content appended to **{chosen}**")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        else:  # Overwrite
            new_content = st.text_area("New content (replaces everything)", height=120, key="overwrite_text")
            if st.button("Overwrite", key="overwrite_btn"):
                try:
                    path.write_text(new_content)
                    st.success(f"✅ **{chosen}** overwritten successfully")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("No files yet — create one in the **Create** tab first.")

# ---------- DELETE ----------
with tab_delete:
    st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
    st.subheader("Delete a file")

    files = sorted(p.name for p in WORKDIR.glob("*") if p.is_file())
    if files:
        chosen = st.selectbox("Select a file to delete", files, key="delete_select")
        confirm = st.checkbox(f"I'm sure I want to permanently delete **{chosen}**")
        if st.button("Delete File", key="delete_btn", disabled=not confirm):
            try:
                resolve(chosen).unlink()
                st.success(f"🗑️ **{chosen}** deleted successfully.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.info("No files yet — create one in the **Create** tab first.")

# ---------- BROWSE ----------
with tab_browse:
    st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
    st.subheader("All files")

    files = sorted(WORKDIR.glob("*"))
    if files:
        rows = []
        for p in files:
            stat = p.stat()
            rows.append({
                "📄 Name": p.name,
                "Size (bytes)": stat.st_size,
                "Last Modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No files yet — create one in the **Create** tab first.")

# ----------------------------- FOOTER -----------------------------
st.markdown(
    '<div class="footer-note">Built with Python &amp; Streamlit · pathlib-based file handling demo</div>',
    unsafe_allow_html=True,
)