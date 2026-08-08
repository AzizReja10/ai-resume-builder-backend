from jinja2 import Template

RESUME_TEMPLATE = Template("""
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: 'Georgia', 'Times New Roman', serif; max-width: 800px; margin: 30px auto; color: #111; font-size: 13px; }
    .header { text-align: center; margin-bottom: 14px; }
    .header h1 { font-size: 22px; margin: 0 0 4px 0; letter-spacing: 1px; }
    .contact { font-size: 12px; color: #333; }
    .contact a { color: #333; text-decoration: none; margin: 0 4px; }
    h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #000; margin-top: 16px; margin-bottom: 6px; padding-bottom: 2px; }
    .entry { margin-bottom: 10px; }
    .entry-header { display: flex; justify-content: space-between; font-weight: bold; }
    .entry-sub { display: flex; justify-content: space-between; font-style: italic; font-size: 12px; color: #333; }
    ul { margin: 4px 0; padding-left: 18px; }
    li { margin-bottom: 2px; line-height: 1.4; }
    .skills-row { margin-bottom: 3px; }
    .skills-row b { display: inline; }
</style>
</head>
<body>
    <div class="header">
        <h1>{{ personal_info.get('name', '') }}</h1>
        <div class="contact">
            {{ personal_info.get('location', '') }}
            {% if personal_info.get('phone') %} | {{ personal_info.get('phone') }}{% endif %}
            {% if personal_info.get('email') %} | {{ personal_info.get('email') }}{% endif %}
            {% for link in personal_info.get('links', []) %} | <a href="{{ link.get('url', '') }}">{{ link.get('label', '') }}</a>{% endfor %}
        </div>
    </div>

    {% if education %}
    <h2>Education</h2>
    {% for item in education %}
    <div class="entry">
        <div class="entry-header"><span>{{ item.get('institution', '') }}</span><span>{{ item.get('dates', '') }}</span></div>
        <div class="entry-sub"><span>{{ item.get('degree', '') }}</span><span>{{ item.get('detail', '') }}</span></div>
    </div>
    {% endfor %}
    {% endif %}

    {% if projects %}
    <h2>Projects</h2>
    {% for item in projects %}
    <div class="entry">
        <div class="entry-header">
            <span>{{ item.get('name', '') }} {% if item.get('tags') %}| {{ item.get('tags') }}{% endif %}</span>
            <span>{{ item.get('date', '') }}</span>
        </div>
        <ul>{% for bullet in item.get('bullets', []) %}<li>{{ bullet }}</li>{% endfor %}</ul>
    </div>
    {% endfor %}
    {% endif %}

    {% if experience %}
    <h2>Experience</h2>
    {% for item in experience %}
    <div class="entry">
        <div class="entry-header"><span>{{ item.get('role', '') }} — {{ item.get('company', '') }}</span><span>{{ item.get('dates', '') }}</span></div>
        <ul>{% for bullet in item.get('bullets', []) %}<li>{{ bullet }}</li>{% endfor %}</ul>
    </div>
    {% endfor %}
    {% endif %}

    {% if skills %}
    <h2>Technical Skills</h2>
    {% for group in skills %}
    <div class="skills-row"><b>{{ group.get('category', '') }}:</b> {{ group.get('items', []) | join(', ') }}</div>
    {% endfor %}
    {% endif %}

    {% if extracurricular %}
    <h2>Extracurricular</h2>
    <ul>{% for item in extracurricular %}<li>{{ item }}</li>{% endfor %}</ul>
    {% endif %}
</body>
</html>
""")