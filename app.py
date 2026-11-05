from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Project, Blog, ContactMessage, SiteConfig, SiteSetting, UploadedFile
import os, time

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- Global Settings Injection ----------
@app.context_processor
def inject_global_settings():
    settings = {s.key: s.value for s in SiteSetting.query.all()}
    files = {f.file_type: f.filename for f in UploadedFile.query.all()}
    return dict(settings=settings, files=files)

# ---------- Public Routes ----------

@app.route('/')
def index():
    projects = Project.query.filter_by(featured=True).order_by(Project.created_at.desc()).limit(4).all()
    return render_template('index.html', projects=projects)

@app.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=all_projects)

@app.route('/project/<int:id>')
def project_detail(id):
    p = Project.query.get_or_404(id)
    return render_template('project_detail.html', p=p)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    posts = Blog.query.filter_by(is_published=True).order_by(Blog.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:id>')
def blog_detail(id):
    post = Blog.query.get_or_404(id)
    if not post.is_published and not (current_user.is_authenticated and current_user.is_admin):
        abort(404)
    return render_template('blog_detail.html', post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        db.session.add(msg)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ---------- Auth ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            remember = request.form.get('remember') == 'on'
            login_user(user, remember=remember)
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ---------- Admin ----------

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    projects = Project.query.order_by(Project.created_at.desc()).all()
    posts = Blog.query.order_by(Blog.date_posted.desc()).all()
    unread = ContactMessage.query.filter_by(is_read=False).count()
    return render_template('admin/dashboard.html', projects=projects, posts=posts, unread=unread)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        text_keys = ['email', 'phone', 'github_url', 'linkedin_url']
        for key in text_keys:
            val = request.form.get(key, '')
            setting = SiteSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = val
            else:
                db.session.add(SiteSetting(key=key, value=val))
        
        profile_file = request.files.get('profile_img')
        if profile_file and profile_file.filename:
            filename = f"profile_{secure_filename(profile_file.filename)}"
            # USE ABSOLUTE PATH
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profile_file.save(filepath)
            
            existing = UploadedFile.query.filter_by(file_type='profile_img').first()
            if existing: existing.filename = filename
            else: db.session.add(UploadedFile(file_type='profile_img', filename=filename))

        resume_file = request.files.get('resume')
        if resume_file and resume_file.filename:
            filename = f"resume_{secure_filename(resume_file.filename)}"
            # USE ABSOLUTE PATH
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)
            
            existing = UploadedFile.query.filter_by(file_type='resume').first()
            if existing: existing.filename = filename
            else: db.session.add(UploadedFile(file_type='resume', filename=filename))

        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))

    return render_template('admin/settings.html')

@app.route('/admin/project/new', methods=['GET', 'POST'])
@app.route('/admin/project/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def project_form(id=None):
    if not current_user.is_admin:
        abort(403)
    p = Project.query.get_or_404(id) if id else Project()
    if request.method == 'POST':
        p.title = request.form['title']
        p.short_desc = request.form['short_desc']
        p.problem = request.form['problem']
        p.built = request.form['built']
        p.stack = request.form['stack']
        p.metrics = request.form['metrics']
        p.icon = request.form['icon']
        p.tags = request.form['tags']
        p.result = request.form['result']
        p.featured = 'featured' in request.form

        # --- MULTI-IMAGE HANDLING ---
        remove_img = request.form.get('remove_image')
        if remove_img and p.images:
            current_imgs = p.images.split(',')
            if remove_img in current_imgs:
                current_imgs.remove(remove_img)
                p.images = ','.join(current_imgs)

        files = request.files.getlist('images')
        if files:
            current_imgs = [img for img in p.images.split(',') if img] if p.images else []
            
            for file in files:
                if file and file.filename:
                    if len(current_imgs) >= 4:
                        flash('Maximum 4 images allowed. Extra images were ignored.', 'error')
                        break
                    
                    filename = f"proj_{int(time.time())}_{len(current_imgs)}_{secure_filename(file.filename)}"
                    # USE ABSOLUTE PATH
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    current_imgs.append(filename)
            
            p.images = ','.join(current_imgs)
        # --- END MULTI-IMAGE HANDLING ---

        if not id:
            db.session.add(p)
        db.session.commit()
        flash('Project saved', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/project_form.html', p=p)

@app.route('/admin/project/<int:id>/delete', methods=['POST'])
@login_required
def project_delete(id):
    if not current_user.is_admin:
        abort(403)
    p = Project.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Project deleted', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@app.route('/admin/blog/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def blog_form(id=None):
    if not current_user.is_admin:
        abort(403)
    post = Blog.query.get_or_404(id) if id else Blog()
    if request.method == 'POST':
        post.title = request.form['title']
        post.summary = request.form['summary']
        post.content = request.form['content']
        post.is_published = 'is_published' in request.form
        if not id:
            db.session.add(post)
        db.session.commit()
        flash('Blog post saved', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/blog_form.html', post=post)

@app.route('/admin/blog/<int:id>/delete', methods=['POST'])
@login_required
def blog_delete(id):
    if not current_user.is_admin:
        abort(403)
    post = Blog.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/messages')
@login_required
def admin_messages():
    if not current_user.is_admin:
        abort(403)
    msgs = ContactMessage.query.order_by(ContactMessage.received_at.desc()).all()
    for m in msgs:
        m.is_read = True
    db.session.commit()
    return render_template('admin/messages.html', messages=msgs)

@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        current = request.form['current_password']
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        if not check_password_hash(current_user.password_hash, current):
            flash('Current password is wrong', 'error')
        elif new != confirm:
            flash('New passwords do not match', 'error')
        elif len(new) < 6:
            flash('Password must be at least 6 characters', 'error')
        else:
            current_user.password_hash = generate_password_hash(new)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/change_password.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin / admin123")
    app.run(debug=True)