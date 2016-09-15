# -*- coding: utf-8 -*-
import re
from datetime import datetime

from pyjobs_crawlers.spiders import JobSpider, JobSource


class AfpyJobSpider(JobSpider):

    name = 'afpy'
    start_urls = ['http://www.afpy.org/jobs']
    label = 'AFPY'
    url = 'http://www.afpy.org'
    logo_url = 'http://www.afpy.org/logo.png'

    _crawl_parameters = {
        'from_list__jobs_lists__xpath': '//body',
        'from_list__jobs__xpath': '//div[@class="jobitem"]',
        'from_list__url__xpath': './a/@href',
        'from_list__next_page__xpath': '//div[@class="listingBar"]/span[@class="next"]/a/@href',
        'from_list__publication_datetime__css': '.discreet::text',

        'from_page__container__xpath': '//div[@id="content"]',
        'from_page__title__xpath': './h1[@id="parent-fieldname-title"]/text()',
        'from_page__company__xpath': ('.//h4/a/text()', './/h4/text()'),
        'from_page__company_url__xpath': './div[@id="content-core"]/div[@id="content-core"]/h4/a/@href',
        'from_page__address__xpath': './/h4[1]/following-sibling::div[@class="row"]/text()',
        'from_page__description__css': '#content',
        'from_page__tags__xpath': './div[@id="content-core"]/div[@id="content-core"]'
    }

    def _get_from_list__publication_datetime(self, job_container):
        try:
            publication_date_text = self._extract_first(job_container, 'from_list__publication_datetime')
            if publication_date_text:
                publication_date_text_clean = publication_date_text.replace(u'Créé le ', '').replace(u' par', '')
                return datetime.strptime(publication_date_text_clean, '%d/%m/%Y %H:%M')
            return super(AfpyJobSpider, self)._get_from_page__publication_datetime(job_container)
        except Exception, exc:
            self.get_connector().log(
                    self.name,
                    self.ACTION_CRAWL_ERROR,
                    "Error during publication date extraction: %s" % str(exc)
            )
            return super(AfpyJobSpider, self)._get_from_page__publication_datetime(job_container)

    def _get_from_page__description(self, node):
        description = super(AfpyJobSpider, self)._get_from_page__description(node)
        if description:
            return re.sub('<h1[^>]*?>.*?</h1>', '', description)
        return description

source = JobSource.from_job_spider(AfpyJobSpider)
