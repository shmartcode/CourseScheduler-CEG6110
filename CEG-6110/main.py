from flask import Flask, render_template, request, redirect, url_for, flash
import accounts, scheduling
scheduling.build_dicts()
accounts.initialize_accounts()


app = Flask(__name__)
app.secret_key = "flashkey"
authenticated_user = None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login and redirects based on account type."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        global authenticated_user
        authenticated_user = accounts.authenticate(username, password)
        # Redirects user to their respective dashboard based on account type.
        if hasattr(authenticated_user, 'type'):
            if authenticated_user.type == "student":
                return redirect(url_for("student_dashboard"))
            elif authenticated_user.type == "faculty":
                return redirect(url_for("faculty_dashboard"))
            elif authenticated_user.type == "admin":
                return redirect(url_for("admin_dashboard"))
        # This returns the failure message from authenticate function if failed login.
        flash(authenticated_user)
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route('/student_dashboard', methods=['POST', 'GET'])
def student_dashboard():
    global authenticated_user # Use the global variable to access the authenticated user 
    
    # Ensure only students can access dashboard
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'student':
        flash('Access denied.')
        return redirect(url_for('login'))
    
    # If student has an approved schedule, redirect to schedule display
    if getattr(authenticated_user, 'sched_student_approved', False):
        return redirect(url_for('schedule_display'))
        
    return render_template("student_dashboard.html", user=authenticated_user)

@app.route('/faculty_dashboard')
def faculty_dashboard():
    global authenticated_user # Use the global variable to access the authenticated user
    
    # Ensure only faculty can access dashboard
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'faculty':
        flash('Access denied.')
        return redirect(url_for('login'))
        
    return render_template("faculty_dashboard.html", user=authenticated_user)

@app.route('/admin_dashboard')
def admin_dashboard():
    global authenticated_user # Use the global variable to access the authenticated user
    
    # Ensure only admins can access dashboard
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'admin':
        flash('Access denied.')
        return redirect(url_for('login'))
        
    return render_template("admin_dashboard.html", user=authenticated_user)

@app.route('/logout', methods=['POST'])
def logout():
    global authenticated_user # Use the global variable to access the authenticated user
    authenticated_user = None # Clear the authenticated user
    return redirect(url_for('login'))

@app.route('/create_user', methods=['POST'])
def create_user():
    global authenticated_user
    # Ensure only admin can create students
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'admin':
        flash('Access denied.')
        return redirect(url_for('login'))
    # Debug print for the entire form
    print(f"DEBUG: request.form = {dict(request.form)}")
    # Get form data for new account
    account_type = request.form.get('account_type')
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    if not account_type:
        flash('Account type is missing from the form. Please select an account type.')
        return redirect(url_for('admin_dashboard'))
    # Call the appropriate method based on account type
    if account_type == 'student':
        result = accounts.Admin.create_student(authenticated_user, name, username, password)
    elif account_type == 'faculty':
        result = accounts.Admin.create_faculty(authenticated_user, name, username, password)
    elif account_type == 'admin':
        result = accounts.Admin.create_admin(authenticated_user, name, username, password)
    else:
        flash(f'Invalid account type: {account_type}')
        return redirect(url_for('admin_dashboard'))
    if result is True:
        flash(f"User '{username}' of account type '{account_type}' created successfully.")
    else:
        flash(result)
    return redirect(url_for('admin_dashboard'))

@app.route('/create_schedule', methods=['POST'])
def create_schedule():
    global authenticated_user
    # Ensure only students can create schedules
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'student':
        flash('Access denied.')
        return redirect(url_for('login'))
        
    # Reset any existing majors/minors/schedule
    scheduling.scheduling_init()
    # Use the instance method to clear this specific student's schedule/state
    authenticated_user.clear_schedule()
        
    # Get form data for schedule creation
    major_1 = request.form.get('major_1')
    major_2 = request.form.get('major_2')
    minor_1 = request.form.get('minor_1')
    minor_2 = request.form.get('minor_2')
    
    # Check that at least one major is selected
    # If default value is used (empty string), treat it as not selected
    # Add majors and minors to the student account
    if major_1 is None or major_1 == '':
        flash('At least one major must be selected to create a schedule.')
        return redirect(url_for('student_dashboard'))
    authenticated_user.add_major(major_1)
    if major_2 and major_2 != '':
        authenticated_user.add_major(major_2)
    if minor_1 and minor_1 != '':
        authenticated_user.add_minor(minor_1)
    if minor_2 and minor_2 != '':
        authenticated_user.add_minor(minor_2)
        
    # Add number of semesters
    authenticated_user.update_num_semesters(int(request.form.get('num_sem')))
    
    # Generate schedule and assign to proposed_schedule
    authenticated_user.proposed_schedule = scheduling.generate_schedule(authenticated_user)

    return redirect(url_for('schedule_display'))
    
    
@app.route('/schedule_display')
def schedule_display():
    global authenticated_user
    # Ensure only students can view schedules
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'student':
        flash('Access denied.')
        return redirect(url_for('login'))
        
    # Determine which schedule to display
    displayed_schedule = None
    approval_status = ""
    if authenticated_user.sched_student_approved == True:
        displayed_schedule = authenticated_user.schedule
        approval_status = "approved"
    else:
        displayed_schedule = authenticated_user.proposed_schedule
        approval_status = "proposed"
    return render_template("schedule_display.html", user=authenticated_user, schedule=displayed_schedule, course_catalog=scheduling.courses, approval_message=approval_status)    

@app.route('/approve_schedule', methods=['POST'])
def approve_schedule():
    global authenticated_user
    # Ensure only students can approve their own schedules
    if not hasattr(authenticated_user, 'type') or authenticated_user.type != 'student':
        flash('Access denied.')
        return redirect(url_for('login'))
        
    try_approval = authenticated_user.approve_proposed_schedule()
    if try_approval is not True:
        flash(try_approval)
    else:
        flash('Schedule approved successfully.')
    
    return redirect(url_for('schedule_display'))
        


if __name__ == "__main__":
    app.run(debug=False)
    #app.run(host="0.0.0.0", port=80)    # line for local hosting