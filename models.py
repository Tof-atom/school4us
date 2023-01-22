from app import db


class DBUser(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    firstName = db.Column(db.Text())
    lastName = db.Column(db.Text())
    motherName = db.Column(db.Text())
    fatherName = db.Column(db.Text())
    gender = db.Column(db.Text())
    username = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<DBUser {}: {} {}>".format(self.id, self.username, self.email)
# in a terminal, in the project folder, give the command
# flask shell

# then in this special flask shell, give the commands
# db.create_all()
# db.session.commit()
