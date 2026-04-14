"""
Reusable HTML card snippets rendered via st.markdown(..., unsafe_allow_html=True).
"""


def stat_card(label: str, value: str, css_class: str, sub: str = "") -> str:
    return f"""
<div class="stat-card">
    <div class="stat-label">{label}</div>
    <div class="stat-value {css_class}">{value}</div>
    <div class="stat-sub">{sub}</div>
</div>"""


def panel(header: str, body: str) -> str:
    return f"""
<div class="panel">
    <div class="panel-header">{header}</div>
    {body}
</div>"""


def confidence_bar(label: str, pct: float, cls: str) -> str:
    return f"""
<div class="conf-bar-wrap">
    <div class="conf-bar-label">
        <span>{label}</span>
        <span>{pct:.1f}%</span>
    </div>
    <div class="conf-bar-track">
        <div class="conf-bar-fill-{cls}" style="width:{pct:.1f}%"></div>
    </div>
</div>"""


def result_card(
    label: str,
    cls: str,
    conf: float,
    raw_prob: float,
    time_str: str,
) -> str:
    color = "#ffb800" if cls == "drone" else "#00d4ff"
    tag = "UAS Detected" if cls == "drone" else "Avian Detected"
    icon = "🛸" if cls == "drone" else "🐦"

    conf_bar = confidence_bar("Confidence", conf * 100, cls)
    prob_bar = confidence_bar("Raw Probability", raw_prob * 100, cls)

    meta = f"""
<div class="meta-grid">
    <div class="meta-card">
        <div class="meta-card-label">Model</div>
        <div class="meta-card-value">CNN v2.1</div>
    </div>
    <div class="meta-card">
        <div class="meta-card-label">Input Size</div>
        <div class="meta-card-value">128×128</div>
    </div>
    <div class="meta-card">
        <div class="meta-card-label">NPERSEG</div>
        <div class="meta-card-value">64</div>
    </div>
    <div class="meta-card">
        <div class="meta-card-label">Timestamp</div>
        <div class="meta-card-value" style="font-size:12px">{time_str}</div>
    </div>
</div>"""

    return f"""
<div class="result-divider">
    <div class="result-big" style="color:{color};text-shadow:0 0 20px {color}">
        {icon} {label}
    </div>
    <span class="badge badge-{cls}">{tag}</span>
</div>
{conf_bar}
{prob_bar}
{meta}"""


def empty_state(message: str = "No data yet", icon: str = "◈") -> str:
    return f"""
<div class="empty-state">
    <div class="empty-icon">{icon}</div>
    {message}
</div>"""


def _history_row_date(h: dict) -> str:
    d = h.get("date")
    if d:
        return str(d)
    ts = h.get("timestamp")
    if isinstance(ts, str) and len(ts) >= 10:
        return ts[:10]
    return "—"


def history_table(history: list) -> str:
    if not history:
        return empty_state("No detections yet.<br>Run a scan from the Radar page.")

    rows = ""
    for i, h in enumerate(history):
        badge_cls = "badge-drone" if h.get("cls") == "drone" else "badge-bird"
        rows += f"""
<tr>
    <td class="mono">#{i + 1}</td>
    <td class="mono" style="max-width:130px;overflow:hidden;
                            text-overflow:ellipsis;white-space:nowrap">
        {h.get('file', '—')}
    </td>
    <td><span class="badge {badge_cls}">{h.get('label', '—')}</span></td>
    <td class="mono">{h.get('conf', '—')}%</td>
    <td class="mono">{_history_row_date(h)}</td>
    <td class="mono">{h.get('time', '—')}</td>
</tr>"""

    return f"""
<table class="hist-table">
    <thead>
        <tr>
            <th>#</th>
            <th>File</th>
            <th>Class</th>
            <th>Confidence</th>
            <th>Date</th>
            <th>Time</th>
        </tr>
    </thead>
    <tbody>{rows}</tbody>
</table>"""
