import os
import csv
import io
import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response,
    g
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pavan-aishwarya-wedding-secret-key-2026")

DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "wedding_rsvp.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "wedding2026")


# ==============================================================================
# Database Configuration & Context Management
# ==============================================================================

def get_db():
    """Opens a SQLite database connection for the current request context."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Closes the SQLite database connection at the end of each request."""
    if hasattr(g, "db"):
        g.db.close()


def init_db():
    """Initializes the database schema if not already created."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rsvps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                side TEXT NOT NULL,
                attending_events TEXT NOT NULL,
                guest_count INTEGER NOT NULL DEFAULT 1,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()


# ==============================================================================
# Wedding Frontend Routes
# ==============================================================================

@app.route("/")
def index():
    """Renders the single-page wedding invitation and guestbook."""
    db = get_db()
    # Fetch latest blessings for the live guestbook
    blessings = db.execute(
        """
        SELECT full_name, side, message, created_at 
        FROM rsvps 
        WHERE message IS NOT NULL AND TRIM(message) != '' 
        ORDER BY id DESC LIMIT 20
        """
    ).fetchall()
    return render_template("index.html", blessings=blessings)


@app.route("/rsvp", methods=["POST"])
def rsvp():
    """Processes interactive RSVP form submissions."""
    full_name = request.form.get("full_name", "").strip()
    phone = request.form.get("phone", "").strip()
    side = request.form.get("side", "Common / Friends").strip()
    
    # Checkboxes for events
    events_list = request.form.getlist("attending_events")
    message = request.form.get("message", "").strip()

    try:
        guest_count = int(request.form.get("guest_count", 1))
        if guest_count < 1:
            guest_count = 1
    except (ValueError, TypeError):
        guest_count = 1

    # Form Validations
    if not full_name:
        flash("Please enter your full name.", "error")
        return redirect(url_for("index", _anchor="rsvp"))

    if not phone:
        flash("Please enter your phone number.", "error")
        return redirect(url_for("index", _anchor="rsvp"))

    if not events_list:
        flash("Please select at least one wedding event you plan to attend.", "error")
        return redirect(url_for("index", _anchor="rsvp"))

    attending_events = ", ".join(events_list)

    # Insert into database
    db = get_db()
    db.execute(
        """
        INSERT INTO rsvps (full_name, phone, side, attending_events, guest_count, message)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (full_name, phone, side, attending_events, guest_count, message)
    )
    db.commit()

    flash(
        f"Thank you, {full_name}! Your RSVP has been lovingly received. We cannot wait to celebrate with you!",
        "success"
    )
    return redirect(url_for("index", _anchor="rsvp"))


# ==============================================================================
# Host Admin Dashboard & Authentication
# ==============================================================================

@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    """Host admin dashboard protected by password."""
    # Process login if submitted on /admin
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("Welcome to the Wedding Host Dashboard!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect admin password. Please try again.", "error")
            return redirect(url_for("admin_dashboard"))

    # Check authentication
    if not session.get("admin_logged_in"):
        return render_template("admin.html", logged_in=False)

    db = get_db()
    rsvps = db.execute("SELECT * FROM rsvps ORDER BY id DESC").fetchall()

    # Headcount & Summary calculations
    total_responses = len(rsvps)
    total_headcount = sum(r["guest_count"] for r in rsvps)
    
    # Reception headcount (Dec 13)
    reception_headcount = sum(
        r["guest_count"] for r in rsvps if "Reception" in r["attending_events"]
    )
    
    # Marriage Ceremony / Muhurtham headcount (Dec 14)
    marriage_headcount = sum(
        r["guest_count"] for r in rsvps 
        if "Marriage" in r["attending_events"] or "Muhurtham" in r["attending_events"]
    )

    # Side distributions
    groom_headcount = sum(r["guest_count"] for r in rsvps if "Groom" in r["side"])
    bride_headcount = sum(r["guest_count"] for r in rsvps if "Bride" in r["side"])
    common_headcount = sum(
        r["guest_count"] for r in rsvps 
        if "Common" in r["side"] or "Friend" in r["side"]
    )

    return render_template(
        "admin.html",
        logged_in=True,
        rsvps=rsvps,
        total_responses=total_responses,
        total_headcount=total_headcount,
        reception_headcount=reception_headcount,
        marriage_headcount=marriage_headcount,
        groom_headcount=groom_headcount,
        bride_headcount=bride_headcount,
        common_headcount=common_headcount,
    )


@app.route("/admin/login", methods=["POST"])
def admin_login():
    """Alternative login endpoint for direct post."""
    password = request.form.get("password", "")
    if password == ADMIN_PASSWORD:
        session["admin_logged_in"] = True
        flash("Welcome to the Wedding Host Dashboard!", "success")
    else:
        flash("Incorrect admin password. Please try again.", "error")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/logout")
def admin_logout():
    """Logs out of the admin panel."""
    session.pop("admin_logged_in", None)
    flash("You have been signed out.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/export")
def export_csv():
    """Exports all RSVP records as a downloadable CSV spreadsheet."""
    if not session.get("admin_logged_in"):
        flash("Please log in to export the guest list.", "error")
        return redirect(url_for("admin_dashboard"))

    db = get_db()
    rsvps = db.execute("SELECT * FROM rsvps ORDER BY id ASC").fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Headers
    writer.writerow([
        "ID",
        "Full Name",
        "Phone Number",
        "Side",
        "Total Guests",
        "Attending Events",
        "Blessings / Message",
        "Submission Time",
    ])

    for r in rsvps:
        writer.writerow([
            r["id"],
            r["full_name"],
            r["phone"],
            r["side"],
            r["guest_count"],
            r["attending_events"],
            r["message"],
            r["created_at"],
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=Pavan_Kumar_Aishwarya_Wedding_RSVPs.csv"}
    )


@app.route("/admin/delete/<int:rsvp_id>", methods=["POST"])
def delete_rsvp(rsvp_id):
    """Deletes an RSVP entry from the database."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    db = get_db()
    db.execute("DELETE FROM rsvps WHERE id = ?", (rsvp_id,))
    db.commit()
    flash("RSVP entry removed.", "info")
    return redirect(url_for("admin_dashboard"))


# ==============================================================================
# Initialization & Dynamic Port Execution
# ==============================================================================

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    print(f" * Wedding Database: {DATABASE}")
    print(f" * Admin Password: {ADMIN_PASSWORD}")
    print(f" * Wedding Website running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
