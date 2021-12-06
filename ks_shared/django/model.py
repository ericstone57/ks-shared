from django.db import models
from ks_shared.django.model_utils import BaseModelSoftDeletable, upload_to_without_rename
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField
from django.utils.translation import gettext_lazy as _


class AbstractWXMPUser(BaseModelSoftDeletable):
	GENDER_CHOICES = Choices(
		('male', 'Male'),
		('female', 'Female'),
		('unknown', 'Unknown')
	)

	name = models.CharField(blank=True, max_length=255, default='', db_index=True)
	openid = models.CharField(blank=True, max_length=30, db_index=True)
	unionid = models.CharField(blank=True, max_length=30, null=True, default=None, db_index=True)
	cellphone = models.CharField(blank=True, max_length=20, null=True, default=None)
	email = models.CharField(blank=True, max_length=255, null=True, default=None)
	birthday = models.DateField(blank=True, null=True, default=None)
	gender = StatusField(choices_name='GENDER_CHOICES', default='unknown')
	avatar = models.ImageField(blank=True, upload_to=upload_to_without_rename, null=True, default=None)
	city = models.CharField(blank=True, null=True, max_length=100, default=None)
	province = models.CharField(blank=True, null=True, max_length=100, default=None)
	country = models.CharField(blank=True, null=True, max_length=100, default=None)
	language = models.CharField(blank=True, null=True, max_length=100, default=None)
	avatar_url = models.CharField(blank=True, null=True, max_length=255, default=None, help_text='wxa avatar url')

	last_update_wxa_at = models.DateTimeField(blank=True, null=True, default=None)
	wxa_json = models.JSONField(blank=True, default=dict)

	# utm tracking
	utm_campaign = models.CharField(blank=True, null=True, max_length=255, default=None)
	utm_source = models.CharField(blank=True, null=True, max_length=255, default=None)

	# the tracker
	tracker = FieldTracker()

	@property
	def avatar_link(self):
		return str(self.avatar.url) if self.avatar else ''

	@classmethod
	def gender_format(cls, value):
		if value == '男' or value == 'male' or value == 1:
			return cls.GENDER_CHOICES.male
		if value == '女' or value == 'female' or value == 2:
			return cls.GENDER_CHOICES.female
		return cls.GENDER_CHOICES.unknown

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		abstract = True
