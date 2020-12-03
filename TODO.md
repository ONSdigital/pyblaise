# TODO

+ separate out `soap_utils`
    + this package sets up the jinja soap templates and populates them
      with information
    + could be standalone or submodule

+ automated testing of soap operations
    + currently, new soap operations require new tests to be written
    + much better to automatically test some aspects of the soap stuff
    + BLOCKED: soap templates need specific parameters, we can't set defaults (it seems?)

+ expose via REST API
    + `api` submodule which has a bunch of standalone flask servers
    + preparation to support the c# migration
    + understand the sequencing of calls

+ parse 500 error responses, these are sometimes useful and should be a core library feature
    + example bad xml formatting response:
```xml
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <s:Fault>
      <faultcode xmlns:a="http://schemas.microsoft.com/net/2005/12/windowscommunicationfoundation/dispatcher">a:DeserializationFailed</faultcode>
      <faultstring xml:lang="en-US">The formatter threw an exception while trying to deserialize the message: There was an error while trying to deserialize parameter http://www.blaise.com/deploy/2013/03:value. The InnerException message was 'Invalid enum value 'slave' cannot be deserialized into type 'StatNeth.Blaise.Administer.DataContract.Deploy.ServerType'. Ensure that the necessary enum values are present and are marked with EnumMemberAttribute attribute if the type has DataContractAttribute attribute.'.  Please see InnerException for more details.</faultstring>
    </s:Fault>
  </s:Body>
</s:Envelope>
```

    + example invalid token response
```xml
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <s:Fault>
      <faultcode>s:access_token_invalid</faultcode>
      <faultstring xml:lang="en-US">The provided access token is invalid.</faultstring>
    </s:Fault>
  </s:Body>
</s:Envelope>
```
