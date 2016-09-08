from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Length

class ContactForm(Form):
  name = TextField("Name")
  email = TextField("Email")
  subject = TextField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send")

class EditForm(Form):
    username = StringField('nickname', validators=[Required()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
