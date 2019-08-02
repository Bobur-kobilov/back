# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountVersions(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    reason = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    modifiable_id = models.IntegerField(blank=True, null=True)
    modifiable_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    fun = models.IntegerField(blank=True, null=True)
    avg_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_versions'


class Accounts(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    in_field = models.DecimalField(db_column='in', max_digits=32, decimal_places=16, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    out = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    default_withdraw_fund_source_id = models.IntegerField(blank=True, null=True)
    avg_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'


class ApiTokens(models.Model):
    member_id = models.IntegerField()
    access_key = models.CharField(unique=True, max_length=50)
    secret_key = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    trusted_ip_list = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    oauth_access_token_id = models.IntegerField(blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    scopes = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_tokens'


class Assets(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    attachable_id = models.IntegerField(blank=True, null=True)
    attachable_type = models.CharField(max_length=255, blank=True, null=True)
    file = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assets'


class AuditLogs(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    operator_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    auditable_id = models.IntegerField(blank=True, null=True)
    auditable_type = models.CharField(max_length=255, blank=True, null=True)
    source_state = models.CharField(max_length=255, blank=True, null=True)
    target_state = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_logs'


class Authentications(models.Model):
    provider = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authentications'


class Comments(models.Model):
    content = models.TextField(blank=True, null=True)
    author_id = models.IntegerField(blank=True, null=True)
    ticket_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Deposits(models.Model):
    account_id = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fund_uid = models.CharField(max_length=255, blank=True, null=True)
    fund_extra = models.CharField(max_length=255, blank=True, null=True)
    txid = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    aasm_state = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    confirmations = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    payment_transaction_id = models.IntegerField(blank=True, null=True)
    txout = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deposits'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DocumentTranslations(models.Model):
    document_id = models.IntegerField()
    locale = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document_translations'


class Documents(models.Model):
    key = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    is_auth = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'


class FundSources(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    extra = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    is_locked = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fund_sources'


class IdDocuments(models.Model):
    id_document_type = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    id_document_number = models.CharField(max_length=255, blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    id_bill_type = models.IntegerField(blank=True, null=True)
    aasm_state = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_documents'


class Identities(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    password_digest = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    retry_count = models.IntegerField(blank=True, null=True)
    is_locked = models.IntegerField(blank=True, null=True)
    locked_at = models.DateTimeField(blank=True, null=True)
    last_verify_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'identities'


class InterestCoins(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    market = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    list_order = models.IntegerField(blank=True, null=True)
    memo = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interest_coins'


class Members(models.Model):
    sn = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    identity_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    activated = models.IntegerField(blank=True, null=True)
    country_code = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.IntegerField(blank=True, null=True)
    api_disabled = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    email_allowed = models.IntegerField(blank=True, null=True, default=1)
    sms_allowed = models.IntegerField(blank=True, null=True, default=1)
    kyc_activated = models.IntegerField(blank=True, null=True)
    restricted = models.IntegerField(blank=True, null=True, default=0)
    deleted = models.IntegerField(blank=True, null=True, default=0)
    class Meta:
        managed = False
        db_table = 'members'


class NotifyLogTranslations(models.Model):
    notify_log_id = models.IntegerField()
    locale = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    msg = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notify_log_translations'


class NotifyLogs(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    kind = models.CharField(max_length=255, blank=True, null=True)
    msg = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notify_logs'


class OauthAccessGrants(models.Model):
    resource_owner_id = models.IntegerField()
    application_id = models.IntegerField()
    token = models.CharField(unique=True, max_length=255)
    expires_in = models.IntegerField()
    redirect_uri = models.TextField()
    created_at = models.DateTimeField()
    revoked_at = models.DateTimeField(blank=True, null=True)
    scopes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_access_grants'


class OauthAccessTokens(models.Model):
    resource_owner_id = models.IntegerField(blank=True, null=True)
    application_id = models.IntegerField(blank=True, null=True)
    token = models.CharField(unique=True, max_length=255)
    refresh_token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    expires_in = models.IntegerField(blank=True, null=True)
    revoked_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    scopes = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_access_tokens'


class OauthApplications(models.Model):
    name = models.CharField(max_length=255)
    uid = models.CharField(unique=True, max_length=255)
    secret = models.CharField(max_length=255)
    redirect_uri = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_applications'


class Orders(models.Model):
    bid = models.IntegerField(blank=True, null=True)
    ask = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    origin_volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=8, blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=255)
    ord_type = models.CharField(max_length=10, blank=True, null=True)
    locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    origin_locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    funds_received = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    trades_count = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    origin_id = models.IntegerField(blank=True, null=True)
    first_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class PartialTrees(models.Model):
    proof_id = models.IntegerField()
    account_id = models.IntegerField()
    json = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sum = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partial_trees'


class PaymentAddresses(models.Model):
    account_id = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_addresses'


class PaymentTransactions(models.Model):
    txid = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    confirmations = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    aasm_state = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    receive_at = models.DateTimeField(blank=True, null=True)
    dont_at = models.DateTimeField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=60, blank=True, null=True)
    txout = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payment_transactions'


class Proofs(models.Model):
    root = models.CharField(max_length=255, blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    ready = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sum = models.CharField(max_length=255, blank=True, null=True)
    addresses = models.TextField(blank=True, null=True)
    balance = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proofs'


class ReadMarks(models.Model):
    readable_id = models.IntegerField(blank=True, null=True)
    reader_id = models.IntegerField()
    readable_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(blank=True, null=True)
    reader_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'read_marks'


class ReferralFeeHistories(models.Model):
    trade_id = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16)
    fee = models.DecimalField(max_digits=32, decimal_places=16)
    referral_id = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_fee_histories'


class ReferralFriends(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_friends'


class ReferralInfos(models.Model):
    fee = models.DecimalField(max_digits=32, decimal_places=16)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'referral_infos'


class Referrals(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    referral_id = models.IntegerField(blank=True, null=True)
    fee = models.DecimalField(max_digits=32, decimal_places=16)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referrals'


class RunningAccounts(models.Model):
    category = models.IntegerField(blank=True, null=True)
    income = models.DecimalField(max_digits=32, decimal_places=16)
    expenses = models.DecimalField(max_digits=32, decimal_places=16)
    currency = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    source_type = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'running_accounts'


class SchemaMigrations(models.Model):
    version = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'schema_migrations'


class SignupHistories(models.Model):
    member_id = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    accept_language = models.CharField(max_length=255, blank=True, null=True)
    ua = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'signup_histories'


class SimpleCaptchaData(models.Model):
    key = models.CharField(max_length=40, blank=True, null=True)
    value = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simple_captcha_data'


class StopOrders(models.Model):
    bid = models.IntegerField(blank=True, null=True)
    ask = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ord_type = models.CharField(max_length=10, blank=True, null=True)
    target_price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    locked = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stop_orders'


class Taggings(models.Model):
    tag_id = models.IntegerField(blank=True, null=True)
    taggable_id = models.IntegerField(blank=True, null=True)
    taggable_type = models.CharField(max_length=255, blank=True, null=True)
    tagger_id = models.IntegerField(blank=True, null=True)
    tagger_type = models.CharField(max_length=255, blank=True, null=True)
    context = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taggings'
        unique_together = (('tag_id', 'taggable_id', 'taggable_type', 'context', 'tagger_id', 'tagger_type'),)


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    taggings_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class Tickets(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    aasm_state = models.CharField(max_length=255, blank=True, null=True)
    author_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class Tokens(models.Model):
    token = models.CharField(max_length=255, blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    is_used = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class Trades(models.Model):
    price = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    volume = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    ask_id = models.IntegerField(blank=True, null=True)
    bid_id = models.IntegerField(blank=True, null=True)
    trend = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ask_member_id = models.IntegerField(blank=True, null=True)
    bid_member_id = models.IntegerField(blank=True, null=True)
    funds = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    bid_fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    ask_fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trades'


class TwoFactors(models.Model):
    member = models.ForeignKey(Members, related_name='two_factors', on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=255, blank=True, null=True)
    last_verify_at = models.DateTimeField(blank=True, null=True)
    activated = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    refreshed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'two_factors'


class Versions(models.Model):
    item_type = models.CharField(max_length=255)
    item_id = models.IntegerField()
    event = models.CharField(max_length=255)
    whodunnit = models.CharField(max_length=255, blank=True, null=True)
    object = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versions'


class Withdraws(models.Model):
    sn = models.CharField(max_length=255, blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)
    currency = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fee = models.DecimalField(max_digits=32, decimal_places=16, blank=True, null=True)
    fund_uid = models.CharField(max_length=255, blank=True, null=True)
    fund_extra = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)
    txid = models.CharField(max_length=255, blank=True, null=True)
    aasm_state = models.CharField(max_length=255, blank=True, null=True)
    sum = models.DecimalField(max_digits=32, decimal_places=16)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'withdraws'
