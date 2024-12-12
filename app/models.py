from flask_login import UserMixin
from datetime import datetime
from enum import Enum
from flask_migrate import Migrate

from sqlalchemy.orm import relationship

from init import  db

"""Define data structure, tables for users, transactions, jars"""
"""Define transaction type"""
class IncomeOutcome(Enum):
	Income = "Income"
	Outcome = "Outcome"

"""Define refund status"""
class RefundStatus(Enum):
	Requested = "Requested"
	Processing = "Processing"
	Completed = "Completed"
	Failed = "Failed"

"""User table"""
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(130), nullable=False)

	transactions = db.relationship('Transactions', back_populates='user', lazy = True)
	refunds = db.relationship('Refund', back_populates='user', lazy = True)
	saving_jars = db.relationship('SavingJar', back_populates='user', lazy = True)

"""Transactions table"""
class Transactions(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	amount = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, default=datetime, nullable=False)
	category = db.Column(db.String(50), nullable=False)
	kind = db.Column(db.Enum(IncomeOutcome), nullable=False)

	user = db.relationship('User', back_populates='transactions')

"""Refunds"""
class Refund(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.DateTime, default=datetime, nullable=False)
	amount = db.Column(db.Float, nullable=False)
	status = db.Column(db.Enum(RefundStatus), nullable=False)

	user = db.relationship('User', back_populates='refunds')


"""SavingJars table"""
class SavingJar(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	name = db.Column(db.String(200), nullable=False)
	goal = db.Column(db.String(200), nullable=False)
	current_amount = db.Column(db.Float, default=0.0)

	user = db.relationship('User', back_populates='saving_jars')
