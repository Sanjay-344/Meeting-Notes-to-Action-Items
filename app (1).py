import streamlit as st
from chain import extract_action_items

# ── Page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Meeting Notes → Action Items",
    page_icon="📝",
    layout="centered",
)

# ── Header ─────────────────────────────────────────────────────────────────────

st.title("📝 Meeting Notes → Action Items")
st.markdown(
    "Paste your meeting notes below and get a clean, structured list "
    "of action items — with owner, deadline, and priority — powered by **Llama 3.3 70B** via Groq."
)

st.divider()

# ── Input ──────────────────────────────────────────────────────────────────────

meeting_notes = st.text_area(
    label="Meeting Notes",
    placeholder="e.g. Alice will prepare the Q3 report by Friday. Bob to follow up with the client next week…",
    height=260,
)

extract_btn = st.button("Extract Action Items", type="primary", use_container_width=True)

# ── Processing ─────────────────────────────────────────────────────────────────

if extract_btn:
    if not meeting_notes.strip():
        st.warning("Please enter some meeting notes before extracting.")
    else:
        with st.spinner("Analysing notes…"):
            result = extract_action_items(meeting_notes)

        st.divider()

        # ── Error state ────────────────────────────────────────────────────────
        if "error" in result:
            st.error("Something went wrong while parsing the response.")
            with st.expander("Details"):
                st.write("**Error:**", result["error"])
                st.write("**Raw LLM output:**")
                st.code(result.get("raw_output", ""), language="json")

        # ── Success state ──────────────────────────────────────────────────────
        else:
            actions = result.get("actions", [])
            st.subheader(f"✅ {len(actions)} Action Item{'s' if len(actions) != 1 else ''} Found")

            # Priority colour badges
            PRIORITY_COLOR = {
                "High":   "🔴",
                "Medium": "🟡",
                "Low":    "🟢",
            }

            for i, item in enumerate(actions, start=1):
                priority = item.get("priority", "Medium")
                badge = PRIORITY_COLOR.get(priority, "⚪")

                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{i}. {item['task']}**")
                    with col2:
                        st.markdown(f"{badge} **{priority}**")

                    col_a, col_b = st.columns(2)
                    col_a.markdown(f"👤 **Owner:** {item['owner']}")
                    col_b.markdown(f"📅 **Deadline:** {item['deadline']}")

            st.divider()

            # Raw JSON toggle
            with st.expander("View raw JSON"):
                st.json(result)
