CLARIAH Software Quality Survey
=====================================================================
 
{% for category, categorydata in criteria.items %}
 
{{ category|safe }}
--------------------------------------------------------------------
 
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
