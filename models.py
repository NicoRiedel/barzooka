import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_repr import PrettyRepresentableBase

import pandas as pd

from biorxiv_scraper import baseurl

db = SQLAlchemy(model_class=PrettyRepresentableBase)

class Biorxiv(db.Model):
    source          = db.Column(db.String(10), default='biorxiv')
    id              = db.Column(db.String, primary_key=True)
    created         = db.Column(db.DateTime)
    title           = db.Column(db.String)
    parse_status    = db.Column(db.Integer, default=0, nullable=False)
    _parse_data     = db.Column('parse_data', db.String)
    _pages          = db.Column('pages', db.String, default='[]', nullable=False)
    _pages_pie      = db.Column('pages_pie', db.String, default='[]', nullable=False)
    _pages_hist     = db.Column('pages_hist', db.String, default='[]', nullable=False)
    _pages_bardot   = db.Column('pages_bardot', db.String, default='[]', nullable=False)
    _pages_box      = db.Column('pages_box', db.String, default='[]', nullable=False)
    _pages_dot      = db.Column('pages_dot', db.String, default='[]', nullable=False)
    _pages_violin   = db.Column('pages_violin', db.String, default='[]', nullable=False)
    _pages_positive = db.Column('pages_positive', db.String, default='[]', nullable=False)
    page_count      = db.Column('page_count', db.Integer, default=0, nullable=False)
    posted_date     = db.Column(db.String(10), default='')
    _author_contact = db.Column('author_contact', db.String)
    email_sent      = db.Column(db.Integer)

    @hybrid_property
    def parse_data(self):
        if self._parse_data:
            return pd.read_json(self._parse_data)
        else:
            return pd.DataFrame(columns=['fn', 'cm', 'pct_cm', 'pct_page'])

    @parse_data.setter
    def parse_data(self, df):
        self._parse_data = df.reset_index().to_json()

    @hybrid_property
    def pages(self):
        return json.loads(self._pages)

    @pages.setter
    def pages(self, lst):
        self._pages = json.dumps(lst)



    @hybrid_property
    def pages_pie(self):
        return json.loads(self._pages_pie)

    @pages_pie.setter
    def pages_pie(self, lst):
        self._pages_pie = json.dumps(lst)


    @hybrid_property
    def pages_hist(self):
        return json.loads(self._pages_hist)

    @pages_hist.setter
    def pages_hist(self, lst):
        self._pages_hist = json.dumps(lst)


    @hybrid_property
    def pages_bardot(self):
        return json.loads(self._pages_bardot)

    @pages_bardot.setter
    def pages_bardot(self, lst):
        self._pages_bardot = json.dumps(lst)


    @hybrid_property
    def pages_box(self):
        return json.loads(self._pages_box)

    @pages_box.setter
    def pages_box(self, lst):
        self._pages_box = json.dumps(lst)


    @hybrid_property
    def pages_dot(self):
        return json.loads(self._pages_dot)

    @pages_dot.setter
    def pages_dot(self, lst):
        self._pages_dot = json.dumps(lst)


    @hybrid_property
    def pages_violin(self):
        return json.loads(self._pages_violin)

    @pages_violin.setter
    def pages_violin(self, lst):
        self._pages_violin = json.dumps(lst)


    @hybrid_property
    def pages_positive(self):
        return json.loads(self._pages_positive)

    @pages_positive.setter
    def pages_positive(self, lst):
        self._pages_positive = json.dumps(lst)




    @hybrid_property
    def pages_str(self):
        if len(self.pages) == 0:
            raise ValueError("Can't pretty print if pages = []")
        if len(self.pages) == 1:
            return "page {}".format(self.pages[0])
        if len(self.pages) == 2:
            return "pages {} and {}".format(*self.pages)
        else:
            pretty = ", ".join([str(p) for p in self.pages[:-1]])
            pretty = 'pages {}, and {}'.format(pretty, self.pages[-1])
            return pretty

    @hybrid_property
    def author_contact(self):
        if self._author_contact:
            return json.loads(self._author_contact)
        return None

    @author_contact.setter
    def author_contact(self, data):
        self._author_contact = json.dumps(data)

    @hybrid_property
    def url(self):
        return baseurl(self.id)

    @hybrid_property
    def pdf_url(self):
        date = self.posted_date.replace('-', '/')
        id_no_ver = self.id.split('v')[0]
        base_url = "https://www.biorxiv.org/content/biorxiv/early/{}/{}.full.pdf"
        return base_url.format(date, id_no_ver)

class Test(Biorxiv):
    pass
