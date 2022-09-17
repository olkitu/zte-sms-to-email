# ZTE API Docs

## /goform/goform_get_cmd_process?isTest=false&cmd=sms_data_total&page=0&data_per_page=1&mem_store=1&tags=10&order_by=order+by+id+desc

This will response all messages in array:

```json
{
   "messages":[
      {
         "id":"164",
         "number":"+358124534",
         "content":"00540065007300740069007600690065007300740069",
         "tag":"0",
         "date":"22,09,17,18,33,25,+12",
         "draft_group_id":"",
         "received_all_concat_sms":"1",
         "concat_sms_total":"0",
         "concat_sms_received":"0",
         "sms_class":"4",
         "sms_mem":"nv",
         "sms_submit_msg_ref":""
      }
   ]
}
```