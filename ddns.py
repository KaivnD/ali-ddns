#!/usr/bin/env python
#coding=utf-8
import json
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

info = ''
RecordId = ''#Store RecordID

init_path = os.path.dirname(os.path.realpath(__file__)) + "/init"
with open(init_path, 'r') as f:
    info = json.loads(f.read())

client = AcsClient(info['AcessKeyID'], info['AccessKeySecret'],'cn-hangzhou')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('alidns.aliyuncs.com')
request.set_method('POST')
request.set_version('2015-01-09')
request.set_action_name('DescribeDomainRecords')

request.add_query_param('DomainName', info['Domain'])

response = client.do_action_with_exception(request)
data = json.loads(response)#str to json

#Find RecordId where RR equle to RR in init file
for i in data['DomainRecords']['Record']:
    if i['RR'] == info['RR']:
        RecordId = i['RecordId']

update_request = CommonRequest()
update_request.set_accept_format('json')
update_request.set_domain('alidns.aliyuncs.com')
update_request.set_method('POST')
update_request.set_version('2015-01-09')
update_request.set_action_name('UpdateDomainRecord')

from json import load
from urllib2 import urlopen

my_ip = load(urlopen('http://jsonip.com'))['ip']

update_request.add_query_param('RecordId', RecordId)
update_request.add_query_param('RR', info['RR'])
update_request.add_query_param('Type', info['Type'])
update_request.add_query_param('Value', my_ip)

update_dns = json.loads(client.do_action(update_request))

if(update_dns['Code'] == 'DomainRecordDuplicate'):
    print 'Domain Record is already exist!'
else:
    print 'Domain Record update sucessefuly!'
