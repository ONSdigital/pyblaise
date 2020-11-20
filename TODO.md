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
