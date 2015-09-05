"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)


db = SQLAlchemy()


class User(db.Model):
    """User of ratings website."""

    __tablename__ = "Users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fb_id = db.Column(db.String(64), unique=True, nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=True)
    fname = db.Column(db.String(15), nullable=False)

    @classmethod
    def add_user(cls, email, fname,  password=None, fb_id=None):
        """Insert a new user into the users table"""
        user = cls(email=email, password=password, fname=fname, fb_id=fb_id)
        db.session.add(user)
        db.session.commit()


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<user_id= %s email= %s fname = %s>" % (self.user_id, self.email, self.fname)


class Company_Post(db.Model):
    """A job Posting."""
    
    __tablename__ = "Company_Posts"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    company = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)

    notes = db.Column(db.String(200), nullable=True) 
    date_applied = db.Column(db.String(64), nullable=True)
    contact_person = db.Column(db.String(64), nullable=True)
    post_url = db.Column(db.String(200), nullable=True)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("Company_Posts"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Job Id= %s User Id= %s>" % (self.job_id, self.user_id)


    # TODO EXPAND THIS FUNCTION TO ADD MORE MEASUREMENTS
    @classmethod
    def add_job_to_db( cls, 
                        job_id,
                        user_id,
                        company,
                        title,

                        notes,
                        date_applied,
                        contact_person):

        job_to_add = cls(
                        job_id, user_id, company, title, notes, date_applied, contact_person)
        db.session.add(job_to_add)
        db.session.commit()


class Interview(db.Model):
    """An interview."""
    
    __tablename__ = "Interviews"

    interview_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('Company_Posts.job_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    company = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    date = db.Column(db.String(64), nullable=True)
    interviewer = db.Column(db.String(64), nullable=True)
    notes = db.Column(db.String(200), nullable=True) 

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("Interviews"))

    company_post = db.relationship("Company_Post",
                           backref=db.backref("Interviews"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Job Id= %s User Id= %s>" % (self.job_id, self.user_id)


    # TODO EXPAND THIS FUNCTION TO ADD MORE MEASUREMENTS
    # @classmethod
    # def add_job_to_db( cls, 
    #                     job_id,
    #                     user_id,
    #                     company,
    #                     title,

    #                     notes,
    #                     date_applied,
    #                     contact_person,
    #                     date_interview_one,
    #                     date_interview_two,
    #                     date_interview_three):

    #     job_to_add = cls(
    #                     job_id, user_id, company, title, notes, date_applied, contact_person, date_interview_one, date_interview_two, date_interview_three)
    #     db.session.add(job_to_add)
    #     db.session.commit()


# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_hunt.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."