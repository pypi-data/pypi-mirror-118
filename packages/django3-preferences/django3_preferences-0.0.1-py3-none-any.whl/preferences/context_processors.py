from preferences import preferences


def preferences_context_processor(request):
    """
    Adds preferences to template context when used
    through TEMPLATE_CONTEXT_PROCESSORS setting.
    """
    return {'preferences': preferences}
