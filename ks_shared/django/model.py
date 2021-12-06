from datetime import datetime

from django.db import models
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from model_utils import Choices, FieldTracker
from model_utils.fields import StatusField

from ks_shared.django.model_utils import BaseModelSoftDeletable, upload_to_without_rename, load_image_from_url


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

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		abstract = True

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

	@classmethod
	def save_from_wxa(cls, wxa_data: dict):
		if 'openid' not in wxa_data or not wxa_data['openid']:
			raise ValueError('missing openid')

		user_db, _ = cls.objects.get_or_create(openid=wxa_data['openid'])
		user_db.unionid = wxa_data['unionid']
		user_db.name = wxa_data['nickName']
		user_db.gender = cls.gender_format(wxa_data['gender'])
		user_db.country = wxa_data['country']
		user_db.province = wxa_data['province']
		user_db.city = wxa_data['city']
		user_db.language = wxa_data['language']
		if wxa_data['avatarUrl'] != user_db.avatar_url:
			user_db.avatar_url = wxa_data['avatarUrl']
			user_db.avatar = load_image_from_url(user_db.avatar_url, f'{user_db.openid}.jpg')
		user_db.wxa_json = wxa_data
		user_db.last_update_wxa_at = make_aware(datetime.now())
		user_db.save()
		return user_db

	def __str__(self):
		return '{} - {}'.format(self.name, self.openid)
