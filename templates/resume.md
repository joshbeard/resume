# {{ resume['name'] }}

## {{ resume['headline'] }}

## Contact Details

* Email: [{{ resume['contact']['email'] }}](mailto:{{ resume['contact']['email'] }})
* Web: [{{ resume['contact']['web']['title'] }}]({{ resume['contact']['web']['url'] }})
* GitHub: [github.com/{{ resume['contact']['github'] }}](https://github.com/{{ resume['contact']['github'] }})
* Location: [{{ resume['contact']['location']['title'] }}]({{ resume['contact']['location']['url'] }})

## Other Formats

* Web/HTML: <{{ resume['url'] }}>
* [PDF]({{ resume['pdf'] }})
* [Word]({{ resume['word'] }})
* [Text]({{ resume['txt'] }}) | [Narrow Text]({{ resume['txt_narrow'] }})
* `{{ resume['gemini'] }}`
* `{{ resume['gopher'] }}`
* `finger resume@jbeard.co`

## Summary

{{ resume['summary'] }}

## Experience
{% for job in resume['experience'] %}
### {{ job['title'] }} with {{ job['org'] }}

{{ job['start'] }} - {{ job['end'] }} - {{ job['location'] }}
{% for item in job['details'] %}
* {{ item }}
{%- endfor %}
{%- if 'tech' in job %}

    _Key technology and skills: {% for skill in job['tech'] -%}
    {{ skill }}
    {%- if not loop.last %}, {% endif %}
{%- endfor %}_
{%- endif %}
{% endfor %}
## Skills

{% for skill in resume['skills']['products'] -%}
{{ skill }}
{%- if not loop.last %}, {% endif %}
{%- endfor %}

