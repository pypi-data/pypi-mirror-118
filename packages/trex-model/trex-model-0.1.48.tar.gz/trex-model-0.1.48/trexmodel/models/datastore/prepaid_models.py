'''
Created on 24 Aug 2021

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel, FullTextSearchable
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import MerchantAcct, Outlet, MerchantUser
from trexlib.utils.string_util import is_empty, is_not_empty
import logging, json
from trexmodel import conf, program_conf
from trexlib.utils.string_util import random_string
from datetime import datetime, timedelta
from trexmodel.models.datastore.customer_models import Customer
import trexmodel.conf as model_conf
from trexmodel.models.datastore.model_decorators import model_transactional

logger = logging.getLogger('model')


class PrepaidSettings(BaseNModel,DictModel):
    '''
    Merchant acct as ancestor
    '''
    
    is_multi_tier_prepaid               = ndb.BooleanProperty(default=False)
    is_lump_sum_prepaid                 = ndb.BooleanProperty(default=True)
    
    lump_sum_settings                   = ndb.JsonProperty(required=False)
    multitier_settings                  = ndb.JsonProperty(required=False)
    
    created_datetime                    = ndb.DateTimeProperty(required=True, auto_now_add=True)
    modified_datetime                   = ndb.DateTimeProperty(required=True, auto_now=True)
    
    created_by                          = ndb.KeyProperty(name="created_by", kind=MerchantUser)
    created_by_username                 = ndb.StringProperty(required=False)
    modified_by                         = ndb.KeyProperty(name="modified_by", kind=MerchantUser)
    modified_by_username                = ndb.StringProperty(required=False)
    
    dict_properties = ["is_multi_tier_prepaid","is_lump_sum_prepaid", "lump_sum_settings", "multitier_settings"]
    
    @property
    def merchant_acct_entity(self):
        return MerchantAcct.fetch(self.key.parent().urlsafe())
    
    @staticmethod
    def get_by_merchant_acct(merchant_acct):
        return PrepaidSettings.query(ancestor=merchant_acct.create_ndb_key()).get()
    
    @staticmethod
    def create(merchant_acct, is_multi_tier_prepaid=False, is_lump_sum_prepaid=True, lump_sum_settings=None, multitier_settings=None, created_by=None):
        prepaid_settings = PrepaidSettings(
                                parent                  = merchant_acct.create_ndb_key(),
                                is_multi_tier_prepaid   = is_multi_tier_prepaid,
                                is_lump_sum_prepaid     = is_lump_sum_prepaid,
                                
                                lump_sum_settings       = lump_sum_settings,
                                multitier_settings      = multitier_settings,
                                
                                created_by              = created_by.create_ndb_key(),
                                created_by_username     = created_by.username,
                                )
        
        prepaid_settings.put()
        
        merchant_acct_prepaid_configuration = {}
        if is_lump_sum_prepaid:
            merchant_acct_prepaid_configuration['lump_sum'] = lump_sum_settings
            
        if is_multi_tier_prepaid:
            merchant_acct_prepaid_configuration['multitier'] = multitier_settings    
        
        merchant_acct.prepaid_configuration = merchant_acct_prepaid_configuration
        merchant_acct.put()
        
        return prepaid_settings
        
    @staticmethod
    def update(prepaid_settings, is_multi_tier_prepaid=False, is_lump_sum_prepaid=True, lump_sum_settings=None, multitier_settings=None, modified_by=None):
        
        prepaid_settings.is_multi_tier_prepaid  = is_multi_tier_prepaid
        prepaid_settings.is_lump_sum_prepaid    = is_lump_sum_prepaid
        prepaid_settings.lump_sum_settings      = lump_sum_settings
        prepaid_settings.multitier_settings     = multitier_settings
        prepaid_settings.modified_by            = modified_by.create_ndb_key()
        prepaid_settings.modified_by_username   = modified_by.username
        prepaid_settings.put()    
    
        merchant_acct_prepaid_configuration = {}
        if is_lump_sum_prepaid:
            merchant_acct_prepaid_configuration['lump_sum'] = lump_sum_settings
            
        if is_multi_tier_prepaid:
            merchant_acct_prepaid_configuration['multitier'] = multitier_settings    
        
        merchant_acct = prepaid_settings.merchant_acct_entity
        merchant_acct.prepaid_configuration = merchant_acct_prepaid_configuration
        merchant_acct.put()
    
    
        return prepaid_settings

