class CustomUIComponent:
    def __init__(self, content):
        """
        Base custom UI class that takes dbc or dcc components and generate a transformed component,
        usually wrapped.

        The firs parameter is always the content.

        :param content: A Dash html component
        :type content: dcc or dcc component
        """
        self._content = content

    @property
    def content(self):
        return self._content