CLARIAH Software Quality Survey
=====================================================================
 
General Information
--------------------------------------------------------------------
 
* **Software name**: {{name}}
* **Software version**: {{version}}
{% if supported %}
* This software is actively supported
{% else %}
* This software is **NOT** actively supported
{% endif %}
{% if experimental %}
* This software is experimental
{% else %}
* This software is ready for production use
{% endif %}
 
Quality Assessment Criteria
--------------------------------------------------------------------

{% for category, categorydata in criteria.items %}
 
### {{ category|safe }}
 
{% for code, itemdata in categorydata.items %}
* **{{code}}**: {{ itemdata.label|safe }}
{% if itemdata.response %}
    * Response: ``{{ itemdata.response }}``
{% elif not responded %}
    * Response: ``Not Applicable / No / Minimal / Adequate / Good / Perfect``
{% endif %}
{% if itemdata.comments %}
    * Comments: {{ itemdata.comments|safe }}
{% elif not responded %}
    * Comments:
{% endif %}
{% endfor %}
{% endfor %}
 
Minimal Requirements
----------------------------------------------------------------
 
This section contains a set of minimal guidelines for developers that you can
simply implement. They follow common practice where possible and take a firm
choice where interoperability benefits from one. However, depending on the
context, your peers will expect more or less from you. 
 
{% for requirementtext, secondorder, requirementconstraints, hassublist, closesublist in requirements %}
{% if secondorder %}
    * {{ requirementtext|safe }}
{% else %}
* {{ requirementtext|safe }}
{% endif %}
{% endfor %}


