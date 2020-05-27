from py4web import action, URL, request
from yatl.helpers import XML
from py4web.utils.url_signer import URLSigner
from py4web.core import Fixture

class StarRater(Fixture):

    STARRATER = '<starrater starrater_id="{id}"></starrater>'

    def __init__(self, url, session, signer=None, db=None, auth=None):
        self.get_url = url + '/get'
        self.set_url = url + '/set'
        self.signer = signer or URLSigner(session)
        # Creates an action (an entry point for URL calls),
        # mapped to the api method, that can be used to request pages
        # for the table.
        self.__prerequisites__ = [session]
        args = list(filter(None, [session, db, auth, self.signer.verify()]))
        f = action.uses(*args)(self.get_stars)
        action(self.get_url, method=["GET"])(f)
        f = action.uses(*args)(self.set_stars)
        action(self.set_url, method=["GET"])(f)

    def __call__(self, id=None):
        """This method returns the element that can be included in the page.
        @param id: id of the file uploaded.  This can be useful if there are
        multiple instances of this form on the page."""
        return XML(StarRater.STARRATER.format(id=id))

    def transform(self, output, shared_data=None):
        if not isinstance(output, dict):
            return output
        urls = {
            'get_url': URL(self.get_url, signer=self.signer),
            'set_url': URL(self.set_url, signer=self.signer),
        }
        script_block = '<script>\n'
        script_block += '  let starrater_urls = {\n'
        for url_name, url_value in urls.items():
            script_block += '    {}: "{}",\n'.format(url_name, url_value)
        script_block += '  };\n</script>\n'
        output['starrater_urls'] = script_block
        return output

    def get_stars(self):
        """Gets the number of stars for a given id. """
        # This is a test implementation; it should be over-ridden.
        # 0 means no stars set.
        id = request.params.get('id')
        return dict(num_stars=0)

    def set_stars(self, id=None):
        """Sets the number of stars."""
        # This is a test implementation that should be over-ridden.
        print("Number of stars set to:", request.params.get('id'),
              int(request.params.num_stars))
        return "ok"
