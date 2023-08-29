from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user,login_required, logout_user, current_user
from sqlalchemy import or_, func
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String())
    firstname = db.Column(db.String())
    maiden_name = db.Column(db.String())
    official_email = db.Column(db.String())  
    personal_email = db.Column(db.String())
    password = db.Column(db.String())
    position = db.Column(db.String())
    member_staff = db.Column(db.String())
    department_directorate_unit = db.Column(db.String())
    number = db.Column(db.String())
    gender = db.Column(db.String())
    rank = db.Column(db.String())
    grade = db.Column(db.String())
    job_title = db.Column(db.String())
    employment_status = db.Column(db.String())
    date_of_appointment = db.Column(db.Date)
    end_of_contract = db.Column(db.Date)
    ghana_card = db.Column(db.String(100))
    snit_number = db.Column(db.String(100))
    tin_number = db.Column(db.String(100))
    immigration_status = db.Column(db.String(100))
    immigration_number = db.Column(db.String(100))
    value_permit = db.Column(db.String(100))
    address = db.Column(db.String(200))
    bank_number = db.Column(db.String(100))
    admin_full_name = db.Column(db.String(255))
    admin_email = db.Column(db.String(255))
    admin_password = db.Column(db.String(255))
    bank_name = db.Column(db.String(100))
    bank_branch = db.Column(db.String(100))
    next_of_kin = db.Column(db.String(100))
    relationship = db.Column(db.String(100))
    address_kin = db.Column(db.String(100))
    gender_kin = db.Column(db.String(100))
    name_beneficiaries = db.Column(db.String(100))
    address_beneficiaries = db.Column(db.String(100))
    other_beneficiaries = db.Column(db.String(100))
    gender_beneficiaries = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Staff('{self.id}', '{self.firstname}', '{self.position}')"
    

login_manager = LoginManager(app)
    


@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))   


# @app.route ('/')
# def signup ():
#     return render_template('regform.html')

@app.route('/', methods=['GET', 'POST'])
def processor():
    if request.method == 'POST':
        surname = request.form['surname']
        firstname = request.form['firstname']
        othernames = request.form['maiden_name']
        official_email = request.form['official_email']
        personal_email = request.form['personal_email']
        password = request.form['password']
        position = request.form['position']
        member_staff = request.form['member_staff']
        department_directorate_unit = request.form['department_directorate_unit']
        number = request.form['number']
        gender = request.form['gender']
        rank = request.form['rank']
        grade = request.form['grade']
        job_title = request.form['job_title']
        employment_status = request.form['employment_status']
        date_of_appointment_str = request.form['date_of_appointment']
        end_of_contract_str = request.form['end_of_contract']

        ghana_card = request.form['ghana_card']
        snit_number = request.form['snit_number']
        tin_number = request.form['tin_number']
        bank_number = request.form['bank_number']
        bank_name = request.form['bank_name']
        bank_branch = request.form['bank_branch']
        next_of_kin = request.form['next_of_kin']
        relationship = request.form['relationship']
        address_kin = request.form['address_kin']
        gender_kin = request.form['gender_kin']
        name_beneficiaries = request.form['name_beneficiaries']
        address_beneficiaries = request.form['address_beneficiaries']
        address = request.form['address']
        value_permit = request.form['value_permit']
        immigration_status = request.form['immigration_status']
        immigration_number = request.form['immigration_number']

        date_of_appointment = datetime.strptime(date_of_appointment_str, '%Y-%m-%d').date()
        end_of_contract = datetime.strptime(end_of_contract_str, '%Y-%m-%d').date()

        new_staff = Staff(
            surname=surname,
            firstname=firstname,
            maiden_name=othernames,
            official_email=official_email,
            personal_email=personal_email,
            password=password,
            position=position,
            member_staff=member_staff,
            department_directorate_unit=department_directorate_unit,
            number=number,
            gender=gender,
            rank=rank,
            grade=grade,
            job_title=job_title,
            employment_status=employment_status,
            date_of_appointment=date_of_appointment,
            end_of_contract=end_of_contract,
            ghana_card=ghana_card,
            snit_number=snit_number,
            tin_number=tin_number,
            bank_number=bank_number,
            bank_name=bank_name,
            bank_branch=bank_branch,
            next_of_kin=next_of_kin,
            relationship=relationship,
            address_kin=address_kin,
            gender_kin=gender_kin,
            name_beneficiaries=name_beneficiaries,
            address_beneficiaries=address_beneficiaries,
            address=address,
            value_permit=value_permit,
            immigration_status=immigration_status,
            immigration_number=immigration_number
        )

        db.session.add(new_staff)
        db.session.commit()

        return "Signup Completed"

    return render_template('regform.html')


@app.route('/adlogin', methods=['GET', 'POST'])
def adlogin():
    if request.method == 'POST':
        ademail = request.form['ademail']
        adpassword = request.form['adpassword']
        user = Staff.query.filter_by(admin_email=ademail).first()  
        
        if user:
            if user.admin_password == adpassword:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return "Invalid email or password"
        else:
            return "User not found"  # Handle the case when user is not found
    
    return render_template("admin_login.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Staff.query.filter_by(official_email=email).first()    
        
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('user_dashboard'))
            else:
                return "Invalid email or password"
    
    return render_template("login.html")



@app.route('/user_dashboard')
@login_required  
def user_dashboard():
    return render_template('user_dashboard.html', user=current_user)



@app.route('/admin')
def admin():
    return render_template('admin_signup.html')

@app.route('/processor2', methods=['POST'])
def processor2():
    surname = request.form['surname']
    firstname = request.form['firstname']
    othernames = request.form['maiden_name']
    admin_email = request.form['admin_email']
    admin_password = request.form['admin_password']
    personal_email = request.form['personal_email']
    position = request.form['position']
    member_staff = request.form['member_staff']
    department_directorate_unit = request.form['department_directorate_unit']
    number = request.form['number']
    gender = request.form['gender']
    rank = request.form['rank']
    grade = request.form['grade']
    job_title = request.form['job_title']
    employment_status = request.form['employment_status']
    date_of_appointment_str = request.form['date_of_appointment']
    end_of_contract_str = request.form['end_of_contract']
    ghana_card = request.form['ghana_card']
    snit_number = request.form['snit_number']
    tin_number = request.form['tin_number']
    bank_number = request.form['bank_number']
    bank_name = request.form['bank_name']
    bank_branch = request.form['bank_branch']
    next_of_kin = request.form['next_of_kin']
    relationship = request.form['relationship']
    address_kin = request.form['address_kin']
    gender_kin = request.form['gender_kin']
    name_beneficiaries = request.form['name_beneficiaries']
    address_beneficiaries = request.form['address_beneficiaries']
    other_beneficiaries = request.form['other_beneficiaries']
    gender_beneficiaries = request.form['gender_beneficiaries']
    value_permit = request.form['value_permit']
    immigration_status = request.form['immigration_status']
    immigration_number = request.form['immigration_number']

  


    date_of_appointment = datetime.strptime(date_of_appointment_str, '%Y-%m-%d').date()
    end_of_contract = datetime.strptime(end_of_contract_str, '%Y-%m-%d').date()


    
    new_user = Staff(
        surname=surname,
        firstname=firstname,
        maiden_name=othernames,
        admin_email=admin_email,
        admin_password=admin_password,
        personal_email=personal_email,
       
        position=position,
        member_staff=member_staff,
        department_directorate_unit=department_directorate_unit,
        number=number,
        gender=gender,
        rank=rank,
        grade=grade,
        job_title=job_title,
        employment_status=employment_status,
        date_of_appointment=date_of_appointment,
        end_of_contract=end_of_contract,
        ghana_card=ghana_card,
        snit_number=snit_number,
        tin_number=tin_number,
        bank_number=bank_number,  
        bank_name=bank_name,      
        bank_branch=bank_branch,  
       next_of_kin=next_of_kin,  
     relationship=relationship, 
     address_kin=address_kin,  
     gender_kin=gender_kin, 
     name_beneficiaries=name_beneficiaries,  
    address_beneficiaries=address_beneficiaries,  
    other_beneficiaries=other_beneficiaries,  
    gender_beneficiaries=gender_beneficiaries, 
    value_permit=value_permit,  
    immigration_status=immigration_status,  
    immigration_number=immigration_number 
    )

    db.session.add(new_user)
    db.session.commit()

    return "Admin registration completed"




# @app.route ('/')
# def signup ():
#     return render_template('signup.html')

# @app.route ('/processor',methods=['POST'])
# def processor():
#     fname = request.form.get('fname')
#     email = request.form.get('email')
#     password= request.form.get('password')
#     new_user = Staff(full_name=fname,email=email,password=password)
#     db.session.add(new_user)
#     db.session.commit()
#     return "Sign Completed" 


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required  
def dashboard():
    search_name = request.args.get('search_name', '').strip()
    member_staff = request.args.get('member_staff', '').strip()
    department_directorate_unit = request.args.get('department_directorate_unit', '').strip()
    number = request.args.get('number', '').strip()
    gender = request.args.get('gender', '').strip()
    rank = request.args.get('rank', '').strip()
    grade = request.args.get('grade', '').strip()
    job_title = request.args.get('job_title', '').strip()
    employment_status = request.args.get('employment_status', '').strip()
    date_of_appointment = request.args.get('date_of_appointment', '').strip()
    end_of_contract = request.args.get('end_of_contract', '').strip()

    staff_members = Staff.query.all()
    
    if search_name:
        query = Staff.query.filter(or_(
            Staff.firstname.ilike(f'%{search_name}%'),
            Staff.surname.ilike(f'%{search_name}%')
        ))
        staff_members = query.all()

   
    if member_staff:
        staff_members = [staff for staff in staff_members if staff.member_staff == member_staff]

    if department_directorate_unit:
        staff_members = [staff for staff in staff_members if staff.department_directorate_unit == department_directorate_unit]

    if number:
        staff_members = [staff for staff in staff_members if staff.number == number]

    if gender:
        staff_members = [staff for staff in staff_members if staff.gender == gender]

    if rank:
        staff_members = [staff for staff in staff_members if staff.rank == rank]

    if grade:
        staff_members = [staff for staff in staff_members if staff.grade == grade]

    if job_title:
        staff_members = [staff for staff in staff_members if staff.job_title == job_title]

    if employment_status:
        staff_members = [staff for staff in staff_members if staff.employment_status == employment_status]

   
    if date_of_appointment:
        date_of_appointment = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
        staff_members = [staff for staff in staff_members if staff.date_of_appointment == date_of_appointment]

    if end_of_contract:
        end_of_contract = datetime.strptime(end_of_contract, '%Y-%m-%d').date()
        staff_members = [staff for staff in staff_members if staff.end_of_contract == end_of_contract]

    return render_template('admin_dashboard.html', staff_members=staff_members,user=current_user)

# @app.route('/edit/<int:staff_id>', methods=['POST'])
# @login_required
# def edit_staff(staff_id):
#     new_firstname = request.form.get('new_firstname')
#     new_surname = request.form.get('new_surname')
#     new_department = request.form.get('new_department')
#     new_gender = request.form.get('new_gender')

#     staff_to_edit = Staff.query.get(staff_id)
#     if staff_to_edit:
#         staff_to_edit.firstname = new_firstname
#         staff_to_edit.surname = new_surname
#         staff_to_edit.department_directorate_unit = new_department
#         staff_to_edit.gender = new_gender

#         db.session.commit()
#         return redirect(url_for('dashboard'))
#     else:
#         return "Staff member not found"



@app.route('/edit_firstname/<int:staff_id>', methods=['POST'])
@login_required
def edit_firstname(staff_id):
    new_firstname = request.form.get('new_firstname')

    staff_to_edit = Staff.query.get(staff_id)
    if staff_to_edit:
        staff_to_edit.firstname = new_firstname
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit_surname/<int:staff_id>', methods=['POST'])
@login_required
def edit_surname(staff_id):
    staff_to_edit = Staff.query.get(staff_id)
    
    if staff_to_edit:
        new_surname = request.form.get('new_surname')
        if new_surname is not None:
            staff_to_edit.surname = new_surname
            db.session.commit()
            
    return redirect(url_for('dashboard'))


@app.route('/edit_department/<int:staff_id>', methods=['POST'])
@login_required
def edit_department(staff_id):
    new_department = request.form.get('new_department')

    staff_to_edit = Staff.query.get(staff_id)
    if staff_to_edit:
        staff_to_edit.department_directorate_unit = new_department
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit_gender/<int:staff_id>', methods=['POST'])
@login_required
def edit_gender(staff_id):
    new_gender = request.form.get('new_gender')

    staff_to_edit = Staff.query.get(staff_id)
    if staff_to_edit:
        staff_to_edit.gender = new_gender
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit_job_title/<int:staff_id>', methods=['POST'])
@login_required
def edit_job_title(staff_id):
    new_job_title = request.form.get('new_job_title')

    staff_to_edit = Staff.query.get(staff_id)
    if staff_to_edit:
        staff_to_edit.job_title = new_job_title
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/edit_employment_status/<int:staff_id>', methods=['POST'])
@login_required
def edit_employment_status(staff_id):
    new_employment_status = request.form.get('new_employment_status')

    staff_to_edit = Staff.query.get(staff_id)
    if staff_to_edit:
        staff_to_edit.employment_status = new_employment_status
        db.session.commit()
    return redirect(url_for('dashboard'))


# Edit page route
@app.route('/edit/<int:staff_id>', methods=['GET'])
@login_required
def edit_staff(staff_id):
    staff_member = Staff.query.get(staff_id)
    if staff_member:
        return render_template('edit_staff.html', staff_member=staff_member)
    else:
        return "Staff member not found."

@app.route('/update/<int:staff_id>', methods=['POST'])
@login_required
def update_staff(staff_id):
    staff_member = Staff.query.get(staff_id)
    if staff_member:
        new_firstname = request.form.get('new_firstname')
        new_surname = request.form.get('new_surname')
        new_department = request.form.get('new_department')
        new_job_title = request.form.get('new_job_title')
        new_employment_status = request.form.get('new_employment_status')
        new_grade = request.form.get('new_grade')
        new_staff_number = request.form.get('new_staff_number')
        new_rank = request.form.get('new_rank')
        new_member_staff = request.form.get('new_member_staff')
        new_ghana_card = request.form.get('new_ghana_card')
        new_snit_number = request.form.get('new_snit_number')  # New SNIT Number
        new_tin_number = request.form.get('new_tin_number')  # New TIN Number
        new_bank_number = request.form.get('new_bank_number')  # New Bank Number
        new_bank_name = request.form.get('new_bank_name')  # New Bank Name
        new_bank_branch = request.form.get('new_bank_branch')  # New Bank Branch
        new_next_of_kin = request.form.get('new_next_of_kin')  # New Next of Kin
        new_relationship = request.form.get('new_relationship')  # New Relationship
        new_address_kin = request.form.get('new_address_kin')  # New Address (Kin)
        new_gender_kin = request.form.get('new_gender_kin')  # New Gender (Kin)
        new_name_beneficiaries = request.form.get('new_name_beneficiaries')  # New Name (Beneficiaries)
        new_address_beneficiaries = request.form.get('new_address_beneficiaries')  # New Address (Beneficiaries)
        new_address = request.form.get('new_address')  # New Address
        new_value_permit = request.form.get('new_value_permit')  # New Value Permit
        new_immigration_status = request.form.get('new_immigration_status')  # New Immigration Status
        new_immigration_number = request.form.get('new_immigration_number')  # New Immigration Number
        
        staff_member.firstname = new_firstname
        staff_member.surname = new_surname
        staff_member.department_directorate_unit = new_department
        staff_member.job_title = new_job_title
        staff_member.employment_status = new_employment_status
        staff_member.grade = new_grade
        staff_member.staff_number = new_staff_number
        staff_member.rank = new_rank
        staff_member.member_staff = new_member_staff
        staff_member.ghana_card = new_ghana_card
        staff_member.snit_number = new_snit_number  # Update SNIT Number
        staff_member.tin_number = new_tin_number  # Update TIN Number
        staff_member.bank_number = new_bank_number  # Update Bank Number
        staff_member.bank_name = new_bank_name  # Update Bank Name
        staff_member.bank_branch = new_bank_branch  # Update Bank Branch
        staff_member.next_of_kin = new_next_of_kin  # Update Next of Kin
        staff_member.relationship = new_relationship  # Update Relationship
        staff_member.address_kin = new_address_kin  # Update Address (Kin)
        staff_member.gender_kin = new_gender_kin  # Update Gender (Kin)
        staff_member.name_beneficiaries = new_name_beneficiaries  # Update Name (Beneficiaries)
        staff_member.address_beneficiaries = new_address_beneficiaries  # Update Address (Beneficiaries)
        staff_member.address = new_address  # Update Address
        staff_member.value_permit = new_value_permit  # Update Value Permit
        staff_member.immigration_status = new_immigration_status  # Update Immigration Status
        staff_member.immigration_number = new_immigration_number  # Update Immigration Number
        
        # Update other attributes here
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return "Staff member not found."




@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    user = current_user  
    
    new_firstname = request.form.get('new_firstname')
    new_surname = request.form.get('new_surname')
    new_department = request.form.get('new_department')
    
    if new_firstname:
        user.firstname = new_firstname
    if new_surname:
        user.lastname = new_surname
    if new_department:
        user.department_directorate_unit = new_department
    
    db.session.commit()  
    
    return redirect(url_for('user_dashboard')) 

@app.route('/edit_profile_page')
@login_required
def edit_profile_page():
    return render_template('edit_profile.html', user=current_user)

@app.route('/search_users', methods=['GET'])
@login_required
def search_users():
    search_name = request.args.get('search_name', '')
    found_users = Staff.query.filter(
        (Staff.firstname.contains(search_name)) | (Staff.surname.contains(search_name))
    ).all()
    return render_template('user_dashboard.html', user=current_user, found_users=found_users)


@app.route('/view_user_profile/<int:user_id>', methods=['GET'])
@login_required
def view_user_profile(user_id):
    user = Staff.query.get(user_id)
    if user:
        return render_template('view_user_profile.html', user=user)
    else:
        return "User not found."

@app.route('/logout', methods=['POST'])
@login_required  
def logout():
    logout_user() 
    return redirect(url_for('login'))  


if __name__ == '__main__':
    app.run(port=5000, debug=True)
