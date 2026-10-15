import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, UserProfile, Trip
from auth import create_user, verify_user, validate_password
from travel_generator import generate_trip_plan, get_ai_assistant_response
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key-for-autonomous-travel-planner-1324')

# Support PostgreSQL (Render) or fallback to local SQLite database
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render provides postgres:// which SQLAlchemy 1.4+ requires as postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database')
    os.makedirs(db_dir, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(db_dir, 'travel.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Session Manager Setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables and seed admin user
with app.app_context():
    db.create_all()
    # Seed admin user if database is empty
    if not User.query.filter_by(username='admin').first():
        admin_pwd = "Password123"
        create_user(
            username="admin",
            email="admin@travelplanner.com",
            password=admin_pwd,
            fullname="System Administrator",
            phone="+1234567890",
            is_admin=True
        )
        print(f"[*] Default admin account seeded: admin / {admin_pwd}")

# --- Context Processors ---
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# --- ROUTES ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        fullname = request.form.get('fullname', '').strip()
        phone = request.form.get('phone', '').strip()
        
        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template('register.html')
            
        user, msg = create_user(username, email, password, fullname, phone)
        if user:
            flash(msg + " You can now log in.", "success")
            return redirect(url_for('login'))
        else:
            flash(msg, "danger")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email', '').strip()
        password = request.form.get('password')
        
        if not username_or_email or not password:
            flash("Please enter both credentials.", "danger")
            return render_template('login.html')
            
        user, msg = verify_user(username_or_email, password)
        if user:
            login_user(user)
            flash("Welcome back, " + user.username + "!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash(msg, "danger")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out.", "success")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user's trips sorted by creation date
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    
    # Simple statistics for dashboard display
    total_trips = len(trips)
    
    # Calculate total estimated cost
    total_budget_spent = 0.0
    upcoming_trips = []
    
    today = datetime.utcnow().date()
    for trip in trips:
        total_budget_spent += trip.budget
        # Categorize trip
        if trip.start_date >= today:
            upcoming_trips.append(trip)
            
    return render_template(
        'dashboard.html', 
        trips=trips[:3], # Show top 3 recent trips
        total_trips=total_trips,
        total_budget=total_budget_spent,
        upcoming_count=len(upcoming_trips),
        user_profile=current_user.profile
    )

@app.route('/planner', methods=['GET', 'POST'])
@login_required
def planner():
    if request.method == 'POST':
        current_loc = request.form.get('current_location', '').strip()
        destination = request.form.get('destination', '').strip()
        num_travelers = int(request.form.get('num_travelers', 1))
        num_days = int(request.form.get('num_days', 1))
        start_date_str = request.form.get('start_date')
        budget = float(request.form.get('budget', 0.0))
        travel_type = request.form.get('travel_type', 'Solo')
        transport_pref = request.form.get('transport_preference', 'Car')
        
        if not current_loc or not destination or not start_date_str or budget <= 0:
            flash("All fields are required and budget must be positive.", "danger")
            return render_template('planner.html')
            
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template('planner.html')
            
        # Generate complex travel details using dynamic AI generator
        itinerary_dict = generate_trip_plan(
            current_location=current_loc,
            destination=destination,
            num_travelers=num_travelers,
            num_days=num_days,
            start_date=start_date_str,
            budget=budget,
            travel_type=travel_type,
            transport_pref=transport_pref
        )
        
        # Save trip to DB
        new_trip = Trip(
            user_id=current_user.id,
            current_location=current_loc,
            destination=destination,
            num_travelers=num_travelers,
            num_days=num_days,
            start_date=start_date,
            budget=budget,
            travel_type=travel_type,
            transport_pref=transport_pref,
            itinerary_data=json.dumps(itinerary_dict)
        )
        
        db.session.add(new_trip)
        db.session.commit()
        
        flash("Trip generated successfully!", "success")
        return redirect(url_for('trip_detail', trip_id=new_trip.id))
        
    return render_template('planner.html')

@app.route('/trip/<int:trip_id>')
@login_required
def trip_detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    # Check if user owns the trip or is an admin
    if trip.user_id != current_user.id and not current_user.is_admin:
        flash("You are not authorized to view this trip plan.", "danger")
        return redirect(url_for('dashboard'))
        
    try:
        itinerary_data = json.loads(trip.itinerary_data)
    except json.JSONDecodeError:
        flash("Error reading trip plan information.", "danger")
        return redirect(url_for('dashboard'))
        
    return render_template('trip_detail.html', trip=trip, data=itinerary_data)

@app.route('/trip/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    db.session.delete(trip)
    db.session.commit()
    flash("Trip deleted.", "success")
    return jsonify({"success": True, "message": "Trip deleted successfully."})

@app.route('/trip/<int:trip_id>/update_checklist', methods=['POST'])
@login_required
def update_checklist(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    req_data = request.get_json()
    item_index = req_data.get('index')
    checked_status = req_data.get('checked', False)
    
    try:
        itinerary_dict = json.loads(trip.itinerary_data)
        if 0 <= item_index < len(itinerary_dict["packing_checklist"]):
            itinerary_dict["packing_checklist"][item_index]["checked"] = checked_status
            trip.itinerary_data = json.dumps(itinerary_dict)
            db.session.commit()
            return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
        
    return jsonify({"success": False, "message": "Index out of range"}), 400

@app.route('/trip/<int:trip_id>/chat', methods=['POST'])
@login_required
def chat_assistant(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not current_user.is_admin:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    req_data = request.get_json()
    message = req_data.get('message', '').strip()
    
    if not message:
        return jsonify({"success": False, "message": "Empty query"}), 400
        
    try:
        itinerary_dict = json.loads(trip.itinerary_data)
        
        # Call Assistant Simulator
        reply, updated_dict = get_ai_assistant_response(message, itinerary_dict)
        
        # If assistant updated the plan, commit it back to DB
        if updated_dict:
            trip.itinerary_data = json.dumps(updated_dict)
            db.session.commit()
            
        return jsonify({
            "success": True,
            "reply": reply,
            "updated": updated_dict is not None
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/history')
@login_required
def history():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    return render_template('history.html', trips=trips)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_prof = current_user.profile
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        
        # Optional password update
        new_password = request.form.get('new_password')
        
        if not email:
            flash("Email cannot be empty.", "danger")
            return render_template('profile.html', profile=user_prof)
            
        # Check email uniqueness
        existing_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if existing_email:
            flash("Email is already in use by another account.", "danger")
            return render_template('profile.html', profile=user_prof)
            
        current_user.email = email
        user_prof.fullname = fullname
        user_prof.phone = phone
        
        # Parse traveler profile preferences
        pref_climate = request.form.get('pref_climate', 'Any')
        pref_style = request.form.get('pref_style', 'Balanced')
        pref_notes = request.form.get('pref_notes', '').strip()
        
        pref_dict = {
            "preferred_climate": pref_climate,
            "travel_style": pref_style,
            "notes": pref_notes
        }
        user_prof.preferences = json.dumps(pref_dict)
        
        # If updating password
        if new_password:
            valid, msg = validate_password(new_password)
            if not valid:
                flash(msg, "danger")
                return render_template('profile.html', profile=user_prof)
            current_user.password_hash = generate_password_hash(new_password)
            
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('profile'))
        
    # Read preferences
    try:
        preferences = json.loads(user_prof.preferences or "{}")
    except json.JSONDecodeError:
        preferences = {}
        
    return render_template('profile.html', profile=user_prof, preferences=preferences)

# --- ADMIN PANEL ---

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash("Access Denied: Admin privileges required.", "danger")
        return redirect(url_for('dashboard'))
        
    users = User.query.order_by(User.created_at.desc()).all()
    trips = Trip.query.order_by(Trip.created_at.desc()).all()
    return render_template('admin.html', users=users, trips=trips)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    if user_id == current_user.id:
        return jsonify({"success": False, "message": "You cannot delete your own account."}), 400
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": "User and all associated trips deleted."})

@app.route('/admin/delete_trip/<int:trip_id>', methods=['POST'])
@login_required
def admin_delete_trip(trip_id):
    if not current_user.is_admin:
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    trip = Trip.query.get_or_404(trip_id)
    db.session.delete(trip)
    db.session.commit()
    return jsonify({"success": True, "message": "Trip plan deleted successfully."})

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_code=404, error_message="The page you requested could not be found."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('base.html', error_code=500, error_message="An internal server error occurred."), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

