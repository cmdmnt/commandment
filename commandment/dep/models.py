# class DEPConfig(db.Model):
#     __tablename__ = 'dep_config'
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     # certificate for PKI of server token
#     certificate_id = db.Column(ForeignKey('certificates.id'))
#     certificate = relationship('Certificate', backref='dep_configs')
#
#     server_token = db.Column(MutableDict.as_mutable(JSONEncodedDict), nullable=True)
#     auth_session_token = db.Column(db.String, nullable=True)
#
#     initial_fetch_complete = db.Column(Boolean, nullable=False, default=False)
#     next_check = db.Column(db.DateTime(timezone=False), nullable=True)
#     device_cursor = db.Column(db.String)
#     device_cursor_recevied = db.Column(db.DateTime(timezone=False), nullable=True)  # shouldn't use if more than 7 days old
#
#     url_base = db.Column(db.String, nullable=True)  # testing server environment if used
#
#     def last_check_delta(self):
#         if self.next_check:
#             return str(self.next_check - datetime.datetime.utcnow())
#         else:
#             return ''

#
# class DEPProfile(db.Model):
#     __tablename__ = 'dep_profile'
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     mdm_config_id = db.Column(ForeignKey('mdm_config.id'), nullable=False)
#     mdm_config = relationship('MDMConfig', backref='dep_profiles')
#
#     dep_config_id = db.Column(ForeignKey('dep_config.id'), nullable=False)
#     dep_config = relationship('DEPConfig', backref='dep_profiles')
#
#     # DEP-assigned UUID for this DEP profile
#     uuid = db.Column(db.db.String(36), index=True, nullable=True)  # should be unique but it's assigned to us so can't be null
#
#     profile_data = db.Column(MutableDict.as_mutable(JSONEncodedDict), nullable=False)
#
#     def profile_name(self):
#         return self.profile_data['profile_name']

